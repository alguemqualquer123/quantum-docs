---
description: Safe mode, layout recovery, crash sidecars, and diagnostics for the Quantum editor.
---

# Editor stability and recovery

Quantum keeps editor recovery state separate from project scenes. The active
session marker is cleared only after normal initialization and startup project
loading complete.

## Recovery options

```text
quantum-editor.exe --safe-mode
quantum-editor.exe --reset-layout
quantum-editor-cmd doctor --project <project>
```

Safe mode disables risky editor extensions and layout-dependent startup paths.
`--reset-layout` creates a clean dock arrangement without rewriting the scene.
The project doctor and asset verifier are preferred for CI because they never
open the GUI.

## Crash diagnostics

Fatal editor diagnostics are written to a separate `editor.log.crash` sidecar.
Five bounded reports are rotated, and each report records the Quantum version,
platform, architecture, compiler/configuration, PID/TID, timestamp, and the last
startup phase. The fatal path avoids allocating through the normal editor log.

Generated C++ script DLLs also carry an ABI fingerprint. The editor rejects a
DLL built for the wrong compiler, CRT, architecture, configuration, editor
layout, or shared-library mode before calling its initialization hook.

## Headless recovery smoke

The repository includes a GUI-free contract check for the recovery path:

```powershell
python scripts/editor_stability_smoke.py --editor-cmd build/Release/quantum-editor-cmd.exe
```

It checks the active-session marker, automatic and explicit safe mode, layout
reset, malformed settings isolation, recent-project bounds, log rotation, and
the console editor help path. The fixture is created under the OS temporary
directory and is verified unchanged; the GUI is never launched.

