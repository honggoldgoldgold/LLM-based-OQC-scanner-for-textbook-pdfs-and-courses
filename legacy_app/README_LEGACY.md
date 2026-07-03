# Legacy App Notice

This folder contains the old OCRLLM application code.

It is preserved for reference, comparison, and gradual porting. It is not the
active library package and should not be imported by new downstream projects.

Use the root package instead:

```python
import ocrllm
```

Do not use this as a new dependency boundary:

```python
import legacy_app.OCRLLM
```

When porting from this folder:

- Port one vertical slice at a time.
- Keep public APIs in `src/ocrllm`.
- Add tests against fake providers before wiring real providers.
- Avoid dragging GUI, FastAPI, social download, or package-relative path
  behavior into the new library.
