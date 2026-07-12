const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

function requireRecord(value, label) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
}

function requireExactKeys(value, keys, label) {
  const actual = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) {
    throw new Error(`${label} fields are not exact: ${actual.join(",")}`);
  }
}

function requireText(value, label) {
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`${label} must be nonempty text`);
  }
}

function requireRequestId(value, { nullable = false } = {}) {
  if (nullable && value === null) return;
  if (typeof value !== "string" || !UUID.test(value)) {
    throw new Error("request_id must be a canonical UUIDv4");
  }
}

function requireJsonValue(value, label) {
  if (value === null || typeof value === "string" || typeof value === "boolean") return;
  if (typeof value === "number" && Number.isFinite(value)) return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => requireJsonValue(item, `${label}[${index}]`));
    return;
  }
  requireRecord(value, label);
  for (const [key, item] of Object.entries(value)) {
    requireJsonValue(item, `${label}.${key}`);
  }
}

function validateCapabilities(event) {
  requireExactKeys(event, ["protocol_version", "event", "request_id", "capabilities"], "capabilities event");
  if (!Array.isArray(event.capabilities)) throw new Error("capabilities must be an array");
  for (const report of event.capabilities) {
    requireRecord(report, "capability report");
    requireExactKeys(report, ["name", "status", "reason"], "capability report");
    requireText(report.name, "capability name");
    requireText(report.reason, "capability reason");
    if (!["available", "experimental", "unavailable", "deferred"].includes(report.status)) {
      throw new Error("capability status is not canonical");
    }
  }
}

function validateProgress(event) {
  requireExactKeys(event, ["protocol_version", "event", "request_id", "stage", "completed", "total", "unit"], "progress event");
  requireText(event.stage, "progress stage");
  requireText(event.unit, "progress unit");
  if (!Number.isInteger(event.completed) || event.completed < 0) throw new Error("completed is invalid");
  if (event.total !== null && (!Number.isInteger(event.total) || event.total < event.completed)) {
    throw new Error("total is invalid");
  }
}

function validateError(event) {
  requireExactKeys(event, ["protocol_version", "event", "request_id", "code", "message", "retryable", "details"], "error event");
  requireRequestId(event.request_id, { nullable: true });
  requireText(event.code, "error code");
  requireText(event.message, "error message");
  if (typeof event.retryable !== "boolean") throw new Error("retryable must be boolean");
  requireRecord(event.details, "error details");
  requireJsonValue(event.details, "error details");
}

function validateWarning(event) {
  requireExactKeys(event, ["protocol_version", "event", "request_id", "code", "message", "details"], "warning event");
  requireText(event.code, "warning code");
  requireText(event.message, "warning message");
  requireRecord(event.details, "warning details");
  requireJsonValue(event.details, "warning details");
}

function validateResultPayload(result) {
  requireRecord(result, "result");
  requireExactKeys(result, ["markdown", "source_type", "profile", "status", "output_uri", "artifacts", "hotwords", "warnings", "metadata"], "result");
  requireText(result.markdown, "result markdown");
  if (!["image", "pdf", "audio", "video"].includes(result.source_type)) throw new Error("source_type is invalid");
  if (result.profile !== null) requireText(result.profile, "result profile");
  if (!["complete", "partial"].includes(result.status)) throw new Error("result status is invalid");
  if (result.output_uri !== null) requireText(result.output_uri, "result output_uri");
  for (const field of ["artifacts", "hotwords", "warnings"]) {
    if (!Array.isArray(result[field])) throw new Error(`result ${field} must be an array`);
  }
  for (const artifact of result.artifacts) {
    requireRecord(artifact, "artifact");
    requireExactKeys(artifact, ["kind", "uri", "media_type"], "artifact");
    requireText(artifact.kind, "artifact kind");
    requireText(artifact.uri, "artifact uri");
    requireText(artifact.media_type, "artifact media_type");
  }
  result.hotwords.forEach((item) => requireText(item, "hotword"));
  result.warnings.forEach((item) => requireText(item, "result warning"));
  requireRecord(result.metadata, "result metadata");
  requireJsonValue(result.metadata, "result metadata");
}

export function validateWorkerEvent(event) {
  requireRecord(event, "worker event");
  if (event.protocol_version !== "ocrllm.v1alpha1") throw new Error("protocol_version is unsupported");
  requireRequestId(event.request_id, { nullable: event.event === "error" });
  switch (event.event) {
    case "accepted":
      requireExactKeys(event, ["protocol_version", "event", "request_id"], "accepted event");
      break;
    case "progress":
      validateProgress(event);
      break;
    case "warning":
      validateWarning(event);
      break;
    case "error":
      validateError(event);
      break;
    case "capabilities":
      validateCapabilities(event);
      break;
    case "result":
      requireExactKeys(event, ["protocol_version", "event", "request_id", "result"], "result event");
      validateResultPayload(event.result);
      break;
    default:
      throw new Error(`unknown worker event: ${String(event.event)}`);
  }
  return event;
}
