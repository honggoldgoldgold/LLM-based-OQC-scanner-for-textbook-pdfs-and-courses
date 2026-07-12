import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";

import { WorkerJsonlHarness } from "./worker_jsonl_harness.mjs";

const CAPABILITY_ID = "11111111-1111-4111-8111-111111111111";
const RECOGNITION_ID = "22222222-2222-4222-8222-222222222222";

function recognizeCommand(sourceUri, options = {}) {
  return {
    protocol_version: "ocrllm.v1alpha1",
    command: "recognize",
    request_id: RECOGNITION_ID,
    sources: [{ media_type: "image", uri: sourceUri }],
    provider: "dashscope",
    model: null,
    input_languages: ["zh-Hans", "en"],
    output_language: "zh-Hans",
    profile: "board",
    options,
  };
}

function capabilitiesCommand() {
  return {
    protocol_version: "ocrllm.v1alpha1",
    command: "capabilities",
    request_id: CAPABILITY_ID,
  };
}

async function waitUntil(predicate, timeoutMilliseconds = 10000) {
  const deadline = Date.now() + timeoutMilliseconds;
  while (Date.now() < deadline) {
    if (await predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 20));
  }
  throw new Error("condition did not become true before timeout");
}

async function fileExists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

function pidExists(pid) {
  if (process.platform === "win32") {
    const completed = spawnSync("tasklist", ["/FI", `PID eq ${pid}`, "/FO", "CSV", "/NH"], {
      encoding: "utf8",
      shell: false,
      windowsHide: true,
    });
    return completed.stdout.includes(`"${pid}"`);
  }
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    if (error.code === "ESRCH") return false;
    if (error.code === "EPERM") return true;
    throw error;
  }
}

function killPidIfAlive(pid) {
  if (!pidExists(pid)) return;
  if (process.platform === "win32") {
    spawnSync("taskkill", ["/PID", String(pid), "/T", "/F"], {
      shell: false,
      windowsHide: true,
      stdio: "ignore",
    });
  } else {
    process.kill(pid, "SIGKILL");
  }
}

async function verifyFixture(python, entrypoint, temporaryRoot) {
  const sourcePath = path.join(temporaryRoot, "Very Long Course Folder", "课程 📚", "board image.png");
  const sourceUri = pathToFileURL(sourcePath).href;
  const harness = new WorkerJsonlHarness(python, ["-I", entrypoint], { cwd: temporaryRoot });
  try {
    harness.sendRaw("not-json\n");
    harness.send(capabilitiesCommand());
    harness.send(recognizeCommand(sourceUri));
    const result = await harness.waitForEvent((event) => event.event === "result");
    const exit = await harness.closeAndWait();
    if (exit.code !== 0 || exit.signal !== null) throw new Error(`fixture exited ${exit.code}/${exit.signal}`);
    if (harness.stderr !== "") throw new Error("fixture wrote stderr");
    const kinds = harness.events.map((event) => event.event);
    if (JSON.stringify(kinds) !== JSON.stringify(["error", "capabilities", "accepted", "result"])) {
      throw new Error(`unexpected fixture events: ${kinds.join(",")}`);
    }
    if (result.result.metadata.source_uris[0] !== sourceUri) throw new Error("source URI did not round trip");
    return { scenario: "fixture", lines_validated: harness.events.length, source_uri: sourceUri };
  } finally {
    await harness.terminateTree();
  }
}

async function verifyCancellation(python, entrypoint, temporaryRoot) {
  const sourcePath = path.join(temporaryRoot, "取消 测试 🧪", "board image.png");
  await mkdir(path.dirname(sourcePath), { recursive: true });
  await writeFile(sourcePath, "fixture", "utf8");
  const pidPath = `${sourcePath}.grandchild.pid`;
  const harness = new WorkerJsonlHarness(python, ["-I", entrypoint], { cwd: temporaryRoot });
  let grandchildPid = null;
  try {
    harness.send(recognizeCommand(pathToFileURL(sourcePath).href));
    await harness.waitForEvent((event) => event.event === "accepted");
    await waitUntil(() => fileExists(pidPath));
    grandchildPid = Number.parseInt(await readFile(pidPath, "utf8"), 10);
    if (!Number.isInteger(grandchildPid) || !pidExists(grandchildPid)) throw new Error("grandchild did not start");
    const started = performance.now();
    harness.send({
      protocol_version: "ocrllm.v1alpha1",
      command: "cancel",
      request_id: RECOGNITION_ID,
    });
    const cancelled = await harness.waitForEvent((event) => event.event === "error" && event.code === "CANCELLED");
    const elapsedMilliseconds = performance.now() - started;
    if (cancelled.request_id !== RECOGNITION_ID) throw new Error("cancel request identity changed");
    if (elapsedMilliseconds > 5000) throw new Error(`cancellation exceeded five seconds: ${elapsedMilliseconds}`);
    await waitUntil(() => !pidExists(grandchildPid), 2000);
    const exit = await harness.closeAndWait();
    if (exit.code !== 0 || exit.signal !== null) throw new Error(`cancellation fixture exited ${exit.code}/${exit.signal}`);
    if (harness.stderr !== "") throw new Error(`cancellation fixture wrote stderr: ${harness.stderr}`);
    return { scenario: "cancellation", lines_validated: harness.events.length, elapsed_milliseconds: elapsedMilliseconds };
  } finally {
    await harness.terminateTree();
    if (grandchildPid !== null) killPidIfAlive(grandchildPid);
  }
}

async function verifyLive(python, sourceRoot, temporaryRoot, sourcePath) {
  if (!process.env.DASHSCOPE_API_KEY) throw new Error("DASHSCOPE_API_KEY is required for the opt-in live gate");
  if (!sourcePath || !(await fileExists(sourcePath))) throw new Error("live source image does not exist");
  const environment = { ...process.env, PYTHONPATH: sourceRoot };
  const harness = new WorkerJsonlHarness(python, ["-m", "ocrllm.worker"], {
    cwd: temporaryRoot,
    env: environment,
  });
  try {
    harness.send(recognizeCommand(pathToFileURL(sourcePath).href, { timeout_seconds: 180 }));
    const terminal = await harness.waitForEvent(
      (event) => event.event === "result" || event.event === "error",
      600000,
    );
    if (terminal.event === "error") {
      throw new Error(`live worker returned ${terminal.code}: ${JSON.stringify(terminal.details)}`);
    }
    const exit = await harness.closeAndWait(30000);
    if (exit.code !== 0 || exit.signal !== null) throw new Error(`live worker exited ${exit.code}/${exit.signal}`);
    if (harness.stderr !== "") throw new Error(`live worker wrote stderr: ${harness.stderr}`);
    const kinds = harness.events.map((event) => event.event);
    if (JSON.stringify(kinds) !== JSON.stringify(["accepted", "progress", "progress", "result"])) {
      throw new Error(`unexpected live events: ${kinds.join(",")}`);
    }
    const { result } = terminal;
    if (result.source_type !== "image" || result.profile !== "board" || result.status !== "complete") {
      throw new Error("live worker result identity is not the unified image/board contract");
    }
    const expectedMetadata = {
      provider: "dashscope",
      provider_region: "cn-beijing",
      model: "qwen3.7-plus-2026-05-26",
      profile: "board",
      provider_call_count: 4,
      standalone_sign_scout_count: 3,
      enable_thinking: true,
      vl_high_resolution_images: true,
    };
    for (const [key, value] of Object.entries(expectedMetadata)) {
      if (result.metadata[key] !== value) throw new Error(`live metadata mismatch: ${key}`);
    }
    return {
      scenario: "live",
      lines_validated: harness.events.length,
      markdown_utf8_bytes: Buffer.byteLength(result.markdown, "utf8"),
      markdown_sha256: createHash("sha256").update(result.markdown, "utf8").digest("hex"),
      provider_call_count: result.metadata.provider_call_count,
      standalone_signs_restored: result.metadata.standalone_signs_restored,
      standalone_sign_scout_abstention_count: result.metadata.standalone_sign_scout_abstention_count,
      model: result.metadata.model,
      provider_region: result.metadata.provider_region,
    };
  } finally {
    await harness.terminateTree();
  }
}

async function main() {
  const [scenario, python, target, temporaryRoot, liveSourcePath] = process.argv.slice(2);
  if (!["fixture", "cancellation", "live"].includes(scenario) || !python || !target || !temporaryRoot) {
    throw new Error("usage: verify_worker_protocol.mjs <fixture|cancellation|live> <python> <entrypoint|source-root> <temporary-root> [live-source]");
  }
  await mkdir(temporaryRoot, { recursive: true });
  let result;
  if (scenario === "fixture") result = await verifyFixture(python, target, temporaryRoot);
  else if (scenario === "cancellation") result = await verifyCancellation(python, target, temporaryRoot);
  else result = await verifyLive(python, target, temporaryRoot, liveSourcePath);
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

await main();
