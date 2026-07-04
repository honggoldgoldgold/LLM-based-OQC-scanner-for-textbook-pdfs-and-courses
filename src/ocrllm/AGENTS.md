# Active Library Boundary

This directory is the active `ocrllm` package for downstream imports.

## Keep

- A small public facade in `__init__.py`.
- Import-time dependencies minimal.
- Tests in the root `tests/` directory.
- File output optional.
- Provider behavior injected or isolated behind explicit adapters.

## Avoid

- Importing from `legacy_app` or uppercase `OCRLLM`.
- Pulling GUI, FastAPI, social downloader, browser automation, or heavy media
  packages during `import ocrllm`.
- Copying whole legacy modules into the new package.
- Exposing legacy processor classes as public API without a tested facade.

## When Porting Legacy Behavior

Port one vertical slice at a time:

1. Define the public behavior in root tests.
2. Extract only the needed logic.
3. Keep dependencies optional when they are not required for `import ocrllm`.
4. Update `MIGRATION_STATUS.md` if the active boundary changes.
