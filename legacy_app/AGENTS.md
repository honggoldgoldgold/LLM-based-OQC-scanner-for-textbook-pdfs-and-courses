# Legacy App Boundary

This directory contains the old OCRLLM application and compatibility surface.

## Allowed Work Here

- Fixing old GUI behavior.
- Fixing `launch_gui.bat` and legacy launch flow.
- Maintaining old Codex, Google, DashScope, and OpenAI-compatible mode routing.
- Reading old processors as behavior references.
- Running or updating legacy tests when maintaining the old app.

## Not Allowed As A New Direction

- Do not make new downstream projects import from this directory.
- Do not treat `legacy_app.OCRLLM` as the future public API.
- Do not move large files wholesale into `src/ocrllm`.
- Do not solve new library packaging by adding more behavior to the old app.

## Porting Rule

When behavior needs to become part of the new library, port a tested vertical
slice into `src/ocrllm/` and keep this directory as reference or compatibility
code.
