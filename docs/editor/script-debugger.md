---
description: Use the live Lua debugger attached to a Quantum Play session.
---

# Script Debugger

The editor's live debugger is available from **View > Script Debugger**. It is
intended for debugging the scene that is already running in Play, including
scripts loaded by the runtime scene stack.

## Attach to Play

1. Start the scene with **Play**.
2. Open **View > Script Debugger**.
3. Press **Attach to Play**.
4. Enter the source path and line number, then press **Add breakpoint**.
5. Use **Continue**, **Pause**, **Step Into**, **Step Over**, or **Step Out**.

The source field accepts the path shown by Lua's chunk name. Project-relative
paths also match when the runtime reports an absolute or `lua://`-prefixed
path.

## Watches and stack

Watches are evaluated only while the debugger is paused. The panel displays a
snapshot of Lua frames captured at the stop location and shows the stop reason:

| Reason | Meaning |
| --- | --- |
| `breakpoint` | A configured source line matched. |
| `step` | A step operation reached a new source location. |
| `pause` | The user paused the live Play session. |
| `error` | Lua reported a runtime error. |

The integration pauses game events and runtime simulation systems together.
Rendering remains available, so the scene can be inspected while stopped.
Press **Detach** before ending Play when you want to remove the live hook
explicitly; stopping Play also removes it automatically.

## Standalone and CI debugging

The editor panel observes the live Play VM. For an isolated script or an IDE
adapter, use the headless command instead:

```text
quantum-editor-cmd script debug --file scripts/player.lua \
  --breakpoint scripts/player.lua:12 --protocol --tcp-loopback 0
```

The two modes do not share a VM or breakpoint list, which keeps CI runs
deterministic and prevents a stopped editor session from affecting a build.
