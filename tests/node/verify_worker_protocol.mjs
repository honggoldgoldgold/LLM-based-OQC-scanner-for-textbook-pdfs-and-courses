import { spawnSync } from "node:child_process";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";

import { WorkerJsonlHarness } from "./worker_jsonl_harness.mjs";

const CAPABILITY_ID = "11111111-1111-4111-8111-111111111111";
const RECOGNITION_ID = "22222222-2222-4222-8222-222222222222";

function recognizeCommand(sourceUri) {
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
    options: {},
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

async function main() {
  const [scenario, python, entrypoint, temporaryRoot] = process.argv.slice(2);
  if (!["fixture", "cancellation"].includes(scenario) || !python || !entrypoint || !temporaryRoot) {
    throw new Error("usage: verify_worker_protocol.mjs <fixture|cancellation> <python> <entrypoint> <temporary-root>");
  }
  await mkdir(temporaryRoot, { recursive: true });
  const result = scenario === "fixture"
    ? await verifyFixture(python, entrypoint, temporaryRoot)
    : await verifyCancellation(python, entrypoint, temporaryRoot);
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

await main();
