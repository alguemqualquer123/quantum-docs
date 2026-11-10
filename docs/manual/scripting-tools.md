---
description: Headless Lua debugging, linting, visual scripting graphs, profiling, and hot reload in Quantum.
---

# Scripting tools

Quantum supports Lua for fast iteration and C++ scripts for native gameplay.
The editor command-line twin makes the scripting workflow usable in CI and IDE
adapters without opening the graphical editor.

## Debug and lint

```text
quantum-editor-cmd script debug --file scripts/player.lua \
  --breakpoint scripts/player.lua:12 \
  --commands "watch speed;stack;next;continue" --json

quantum-editor-cmd script lint --file scripts/player.lua --json --strict
```

The debugger supports breakpoints, continue, step into/over/out, watches, call
stack snapshots, conditional expressions evaluated with current locals/globals,
and deterministic diagnostics. For example:

```text
quantum-editor-cmd script debug --file scripts/player.lua \
  --breakpoint scripts/player.lua:12 --condition "speed > 10" \
  --commands "continue"
```

The line protocol can be served to one local adapter over loopback:

```text
quantum-editor-cmd script debug --file scripts/player.lua \
  --breakpoint scripts/player.lua:12 --protocol \
  --tcp-loopback 0 --tcp-timeout-ms 30000
```

For a live standalone/exported runtime, `quantum-engine` exposes a loopback
endpoint before loading the project entry:

```text
quantum-engine --project build/game --debug-port 0 \
  --debug-token-env QUANTUM_DEBUG_TOKEN
```

The selected port is printed to stdout. The first event is a JSON `hello` with
protocol version `2`; when authentication is enabled, the client must send
`auth TOKEN` before using
`status`, `break <source>:<line> [if <expression>]`, `delete`, `clear`,
`continue`, `pause`, `step`, `next`, `out`, `watch`, `stack`,
`errors on|off|all|none|<categories>`,
`ping` or `quit`.
The server accepts one client, listens only on `127.0.0.1`, bounds commands to
64 KiB and supports reconnecting after a client closes. A paused callback is
allowed to unwind safely; its locals and upvalues are snapshotted for watches
while game events are paused and the service keeps drawing/responding.

Error filters can be selected with `errors runtime,callback`, `errors all` or
`errors none`; `+runtime` and `-callback` update the current selection. The
default `errors on` mask is `runtime,callback`. Responses expose both the
human-readable `errorFilter` list and its numeric `errorMask`.

The reproducible smoke is:

```text
python scripts/remote-debug-smoke.py \
  --executable build/Release/quantum-engine.exe
```

The editor's **View > Script Debugger** panel keeps the in-process Play tab and
also provides a **Remote TCP** tab. Enter the loopback port and token shown by
the runtime, then use the panel for status, breakpoints, stepping, watches and
stack refresh. The connection is non-blocking and restricted to loopback; a
remote IDE can still use the line protocol directly. Version 2 adds optional
request correlation without breaking older clients: send `@<id> <command>` and
the JSON response echoes that opaque ID as `requestId`. IDs may contain up to 64
ASCII letters, digits, `-`, `_` and `.` characters and can be kept across
reconnects.

The graphical editor also has a **View > Script Debugger** panel. During Play,
**Attach to Play** installs the debugger hook in the live Lua VM used by the
runtime scene. Breakpoints, pause/continue, step into/over/out, watch
expressions and the captured call stack are available without starting a
second Lua process.

The Play integration is cooperative: a breakpoint is observed inside a Lua
callback, the current callback is allowed to unwind, and game events are
paused at the next safe frame. This keeps the editor's render thread and Lua
VM out of an unsafe cross-thread wait. Detaching removes the hook before the
Play session is destroyed.

For CI and IDE adapters, the `quantum-editor-cmd script debug` loopback
protocol remains the deterministic standalone debugger. The editor panel and
the CLI session are deliberately separate debugging modes: the former
observes the live Play VM, while the latter executes an isolated Lua chunk.
The standalone chunk does not preload engine globals such as `Scene` or project
modules; use `quantum-engine --script-smoke`, the runtime debugger endpoint or
the editor Play integration when the test needs the live engine API.

## Graph assets

Visual scripting graph assets have a stable YAML schema and deterministic
headless validation:

```text
quantum-editor-cmd script graph-validate --file assets/Scripts/Player.graph
quantum-editor-cmd script graph-roundtrip --file assets/Scripts/Player.graph \
  --out .quantum/graphs/Player.roundtrip.graph
```

The runtime also prepares the built-in nodes before Play/export. This catches a
graph that passes the authoring schema but has no registered operation:

```text
quantum-resource-compiler graph \
  --validate-runtime assets/Scripts/Player.graph --json
quantum-resource-compiler graph \
  --validate-runtime .quantum/graphs/Player.gdat
```

The same gate accepts source `.graph` and compiled `.gdat` files. Reflected
method entries can call Lua-registered entity methods through the same runtime
adapter used by the Play graph; static/C++-only methods and object-valued returns
remain outside this adapter.

The runtime interpreter is covered separately by the standalone headless runner:

```text
quantum-engine --headless --graph-smoke --frames 1 --warmup 0
```

This executes a pure math node followed by a variable write and requires the
expected `result=7.500` output.

The generated reflection catalog can now be consumed by a headless gate before
an exported project is packaged:

```text
quantum-reflector catalog --bindings engine/core/script/binding \
  --engine-core engine/core --out build/generated/engine_node_catalog.json
quantum-resource-compiler graph \
  --catalog-file build/generated/engine_node_catalog.json --json
```

The second command validates catalog version, class uniqueness, method
signatures and all reflected member lists, then emits the class/method/property
counts. This audits the generated artifact. `--validate-runtime` covers the
built-in nodes and the reflected method adapter. A graph node with kind
`method.<Class>.<method>` calls a Lua-registered method on its `target` entity;
the `Call Reflected Method` editor node is the editable form for the same path.
Entity handles and primitive/vector arguments are supported, while static or
C++-only methods and object-valued returns remain outside this adapter.

The exported-project load path can be checked without modifying the source scene:

```powershell
build\Release\quantum-engine.exe --project templates/daynight --headless `
  --graph-smoke --graph-project-smoke --frames 1 --warmup 0
```

The project smoke compiles a temporary graph blob, loads it through `asset://`,
executes it with `GraphBinding`, calls a reflected `Object` method, checks the
resulting variable, and removes the temporary asset before shutdown.

## C++ hot reload

During a C++ Play session, use **Scene > Reload C++ Scripts** to rebuild the
project script library asynchronously. The editor keeps the current DLL loaded
while the candidate is compiled and staged, validates its `quantumProjectAbi`,
then pauses game events, runs script cleanup on the owner thread, swaps the
library copy and initializes the live scenes again. A build or ABI failure leaves
the previous library active. The previous Play pause state and attached Lua
debugger are restored after either a successful or failed reload.

The command is available only for an active C++ Play session. Adding new script
source files or changing generated project structure still requires restarting
Play so the project generator can rebuild its source list; the GUI Play path is
the integration surface and should be smoke-tested on the target project after
editor upgrades.

