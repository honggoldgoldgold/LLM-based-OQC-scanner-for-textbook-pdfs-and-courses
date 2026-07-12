import { spawn, spawnSync } from "node:child_process";

import { validateWorkerEvent } from "./validate_worker_event.mjs";

function withTimeout(promise, timeoutMilliseconds, message) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error(message)), timeoutMilliseconds);
    promise.then(
      (value) => {
        clearTimeout(timeout);
        resolve(value);
      },
      (error) => {
        clearTimeout(timeout);
        reject(error);
      },
    );
  });
}

export class WorkerJsonlHarness {
  constructor(executable, args, { cwd, env = process.env } = {}) {
    this.events = [];
    this.waiters = [];
    this.stderr = "";
    this.stdoutBuffer = "";
    this.failure = null;
    this.child = spawn(executable, args, {
      cwd,
      env,
      shell: false,
      windowsHide: true,
      stdio: ["pipe", "pipe", "pipe"],
    });
    this.child.stdout.setEncoding("utf8");
    this.child.stderr.setEncoding("utf8");
    this.child.stdout.on("data", (chunk) => this.consumeStdout(chunk));
    this.child.stderr.on("data", (chunk) => { this.stderr += chunk; });
    this.exitPromise = new Promise((resolve, reject) => {
      this.child.once("error", reject);
      this.child.once("exit", (code, signal) => resolve({ code, signal }));
    });
  }

  consumeStdout(chunk) {
    this.stdoutBuffer += chunk;
    while (this.stdoutBuffer.includes("\n")) {
      const newline = this.stdoutBuffer.indexOf("\n");
      const line = this.stdoutBuffer.slice(0, newline);
      this.stdoutBuffer = this.stdoutBuffer.slice(newline + 1);
      if (line.length === 0) {
        this.fail(new Error("worker emitted a blank stdout line"));
        continue;
      }
      try {
        const event = validateWorkerEvent(JSON.parse(line));
        this.events.push(event);
        this.resolveWaiters(event);
      } catch (error) {
        this.fail(error);
      }
    }
  }

  fail(error) {
    if (this.failure === null) this.failure = error;
    for (const waiter of this.waiters.splice(0)) waiter.reject(error);
  }

  resolveWaiters(event) {
    for (const waiter of [...this.waiters]) {
      if (!waiter.predicate(event)) continue;
      clearTimeout(waiter.timeout);
      this.waiters.splice(this.waiters.indexOf(waiter), 1);
      waiter.resolve(event);
    }
  }

  send(command) {
    if (this.failure !== null) throw this.failure;
    this.child.stdin.write(`${JSON.stringify(command)}\n`, "utf8");
  }

  sendRaw(line) {
    if (this.failure !== null) throw this.failure;
    this.child.stdin.write(line, "utf8");
  }

  waitForEvent(predicate, timeoutMilliseconds = 15000) {
    const existing = this.events.find(predicate);
    if (existing !== undefined) return Promise.resolve(existing);
    if (this.failure !== null) return Promise.reject(this.failure);
    return new Promise((resolve, reject) => {
      const waiter = { predicate, resolve, reject, timeout: null };
      waiter.timeout = setTimeout(() => {
        this.waiters.splice(this.waiters.indexOf(waiter), 1);
        reject(new Error("timed out waiting for worker event"));
      }, timeoutMilliseconds);
      this.waiters.push(waiter);
    });
  }

  async closeAndWait(timeoutMilliseconds = 15000) {
    this.child.stdin.end();
    const result = await withTimeout(
      this.exitPromise,
      timeoutMilliseconds,
      "worker exit timed out",
    );
    if (this.stdoutBuffer.length !== 0) throw new Error("worker ended with an incomplete stdout line");
    if (this.failure !== null) throw this.failure;
    return result;
  }

  async terminateTree() {
    if (this.child.exitCode !== null) return;
    if (process.platform === "win32") {
      spawnSync("taskkill", ["/PID", String(this.child.pid), "/T", "/F"], {
        shell: false,
        windowsHide: true,
        stdio: "ignore",
      });
    } else {
      this.child.kill("SIGKILL");
    }
    await withTimeout(this.exitPromise, 5000, "terminated worker did not exit");
  }
}
