---
description: Headless release validation, manifests, artifact hashes, and platform matrix for Quantum.
---

# Release and platforms

The release pipeline keeps platform packaging separate from editor authoring.
Every package carries a `release-manifest.json` with product, version, platform,
architecture, backend, build type, and build number.
The manifest is generated at install time. This matters for Visual Studio and
other multi-config generators: `cmake --install --config Release` records
`Release` even when the build tree was initially configured as `Debug`.
`release-smoke.py` validates the manifest schema and rejects platform/backend
mismatches before it hashes any artifact (for example, Android must use GLES3,
while macOS/iOS must use Metal).

## Desktop gate

```powershell
cmake -S . -B build -DQUANTUMEDITOR_VERSION=v0.1.0
cmake --build build --config Release --target quantum-editor quantum-editor-cmd quantum-engine quantum-network-relay
cmake --install build --config Release --prefix stage --strip
cpack --config build/CPackConfig.cmake --output-directory dist
python scripts/release-smoke.py --root stage `
  --manifest stage/release-manifest.json `
  --executable stage/bin/quantum-engine.exe `
  --editor-cmd stage/bin/quantum-editor-cmd.exe `
  --relay-executable stage/bin/quantum-network-relay.exe `
  --resource-server stage/bin/quantum-resource-server.exe `
  --runtime-project templates/daynight `
  --resource-project tests/scale/probe `
  --report stage/release-smoke-report.json
```

`release-smoke.py` runs `--help` on the engine, headless editor command, relay and
resource server, recording SHA-256 and size for each, plus SHA-256 and size for
files or complete directories/bundles. When `--runtime-project` is supplied it also
executes the installed engine headlessly with Lua and visual-graph probes; when
`--resource-project` is supplied it runs the installed resource server with `--once`.
The same report format is used for
desktop packages, Android APKs, WebGL outputs, and Apple `.app` bundles.
Windows/MSVC shared packages install the matching VC143 runtime DLLs beside the
engine DLL, so the extracted ZIP is not tied to the build machine's Visual Studio
environment.
The desktop package also contains `quantum-network-relay.exe`; its deployment
token and hosting topology are intentionally external to the release artifact.

The desktop CI also executes a display-free runtime smoke on Windows, Linux and
macOS:

```text
quantum-engine --project templates/daynight --headless --script-smoke \
  --graph-smoke --graph-project-smoke --frames 1 --warmup 0
```

This exercises Lua/ECS initialization and the visual-graph interpreter without
opening X11, Cocoa, Metal, Vulkan or another graphics context.

The desktop release matrix also runs `scripts/network-relay-smoke.py`, starting
the packaged relay path with one real headless server and two simultaneous
clients before publishing the artifact. This verifies room registration,
capacity admission and two distinct gameplay handshakes in the release build.

The validator also checks the artifact format: APK/AAB files must be readable
ZIP archives containing `AndroidManifest.xml`, WebAssembly files must have the
wasm binary magic and version 1 header, and Apple app bundles must contain a
valid `Info.plist` with `CFBundleIdentifier`, `CFBundleExecutable` and a
non-empty executable. `.ipa` archives must contain exactly one valid app under
`Payload/`. The Emscripten workflow publishes the same smoke report next to the
JS/WASM/HTML artifacts.

The local Windows CPack package has also passed this gate: its manifest reported
the Windows/AMD64 package identity, `quantum-engine --help` returned successfully,
and the resource compiler, build generator and reflector binaries were hashed into the smoke
report. This is a packaging gate, not proof that external signing, notarization,
or device certification has run.

## Matrix

The repository workflows cover Windows/MSVC, Linux, macOS, Android Release,
Emscripten/WebGL2, and the checked-in Xcode macOS/iOS targets. Signing,
notarization, store submission, and device certification remain deployment
responsibilities rather than implicit build guarantees.

