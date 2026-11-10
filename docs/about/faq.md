---
description: Frequently asked questions about Quantum Engine — license, platforms, scripting, and project status.
---

# Frequently Asked Questions

## What is Quantum Engine?

Quantum is a free, open-source C++17 2D/3D game engine with an integrated desktop
editor, maintained by SR VINIX. You author scenes visually, script in **Lua** or
**C++**, and export buildable native projects for desktop, mobile, and web while
keeping the ECS-based, data-oriented runtime transparent and extensible.

## How much does it cost? Can I sell my game?

Quantum is released under the **MIT License** — free for personal and commercial use,
with no royalties, revenue share, or seat licenses. Bundled third-party libraries keep
their own (compatible) open-source licenses. See [License & Credits](license.md).

## Which platforms are supported?

| Area | Platforms |
| --- | --- |
| Editor | Windows, Linux, macOS |
| Exported projects | Windows, Linux, macOS, Android, iOS, HTML5 (WebAssembly) |
| Graphics backends | OpenGL, OpenGL ES 3, Vulkan, Metal, Direct3D 11, WebGPU |

## Why can't I choose Vulkan when exporting on macOS?

macOS has no native Vulkan driver. Vulkan runs there through MoltenVK, a translation
layer on top of Metal, and MoltenVK does not yet implement `VK_EXT_descriptor_buffer` —
the feature the renderer uses to bind textures, buffers and samplers. A macOS Vulkan
build compiles and links, but exits at startup on every Mac tested so far.

Rather than offer a build that cannot run, the export dialog lists **Metal** (the default
and recommended choice) and **OpenGL**. The Vulkan backend itself is in the engine and can
be built from the command line; see [Vulkan backend](../building/macos.md#vulkan-backend).
Windows and Linux are unaffected — Vulkan is available on both.

## Lua or C++ — which should I use?

Both target the same runtime API. **Lua** gives the fastest iteration (no compile step)
and is the best starting point; **C++** gives native performance for hot paths. Most
projects mix them — see [Scripting](../manual/scripting.md).

## Does exporting produce a finished executable?

Exporting produces a **self-contained, buildable native project** (CMake, Gradle, or
Xcode depending on the target) with your scenes, assets, scripts, and compiled shaders.
You then build it with the platform's standard toolchain — see
[Exporting a Project](../tutorials/exporting-a-project.md) and
[Command-Line Tools](../editor/command-line.md) for automating this in CI.

## Is Quantum production-ready?

Quantum is under active development. The downloadable editor builds track the `main`
branch and are **not stable releases** — expect breaking changes while the engine and
documentation are refreshed under the Quantum name. Pin a commit for serious projects and
follow the repository for release tags.

## How does Quantum differ from Godot, Unity, or Unreal?

Quantum aims to be **lightweight and code-transparent**: a small MIT-licensed C++ runtime
with an ECS core, where exporting gives you a native project you fully own and can read,
modify, and build yourself. It does not try to match the breadth of larger engines'
tooling; it focuses on a compact feature set — 2D, 3D, UI, physics (Box2D / Jolt), audio
(SoLoud), particles, terrain, and skeletal animation — with both Lua and C++ as
first-class languages.

## Does Quantum use engine-specific asset formats?

Quantum avoids an opaque editor database. The runtime opens standard formats directly —
`.glb`/`.gltf`/`.obj` for models, PNG/JPG/TGA/BMP/HDR/PSD/SVG for textures,
OGG/WAV/MP3/FLAC for audio, and TTF/OTF/TTC for fonts. The file your content tool produces
is the file the game loads.

The exception is FBX: the editor converts it to a standard binary glTF, which the game
loads in its place. The `.fbx` itself is left as it is.

A native export can optionally combine those original bytes into a DXPK2 resource
pack with a SHA-256 digest per entry. That is packaging and integrity verification,
not a converted engine format — see the [asset pipeline](../manual/asset-pipeline.md)
and [Native resource pack](../editor/export.md#native-resource-pack).

Scenes, bundles, and materials are the exception. They are authored as YAML for the editor
and converted at export into C++ that is compiled into your game, rather than shipped as
data the runtime parses. See
[Resources & Assets](../manual/resources-and-assets.md#asset-types).

## Can I load assets at runtime?

Yes, for media. Models, textures, sounds, and fonts can be loaded or swapped from any path
at any point during gameplay, with `Engine.asyncLoading = true` moving the work to worker
threads and [`ResourceProgress`](../reference/classes/resourceprogress.md) reporting how
far along it is. Lua scripts also load at runtime through the `lua://` root.

Those same paths work in a packed native export through engine loaders and `Data`. A
direct `File` handle cannot open a packed entry.

Entity hierarchies work differently, because scenes and bundles are compiled rather than
parsed. Spawning them on demand is fully supported through
[`BundleManager.createBundle`](../reference/classes/bundlemanager.md#createbundle) for any
bundle that existed at build time, but a scene or hierarchy contained in a file the
executable was not built with cannot be loaded. That is a deliberate trade: it keeps entity
setup statically typed, leaves reflection and deserialization out of the runtime, and keeps
startup cost and binary size low on the web and mobile targets. If you need player-supplied
or downloaded content, drive it with runtime media loading plus bundles composed in script.

## Where do my old Supernova projects stand?

Legacy Supernova projects should be migrated to the Quantum editor workflow. The
runtime API carried over in places, but projects should not assume old generated
files, namespaces, or build settings remain compatible. Keep a copy of the original
project and regenerate its project metadata before opening it in the current editor.

## Where can I find the editor crash log?

The desktop editor writes Output-panel messages to `editor.log`. If the editor exits
because of a fatal signal or an unhandled exception, it writes a separate
`editor.log.crash` sidecar and rotates up to four older crash reports. Include the
live log and the newest crash sidecar when reporting a crash.

The log is beside the active `settings.yaml`. An editor started from an installed
desktop launcher normally uses:

| Platform | Log path |
| --- | --- |
| Windows | `%APPDATA%\Quantum\editor.log` |
| macOS | `~/Library/Application Support/Quantum/editor.log` |
| Linux | `$XDG_CONFIG_HOME/quantum/editor.log`, or `~/.config/quantum/editor.log` when `XDG_CONFIG_HOME` is unset |

When you run the editor from source or another writable working directory, it may keep
both `settings.yaml` and `editor.log` in that directory instead. The definitive rule is
that the two files are together.

At startup, the editor keeps the crash path bounded and uses a session marker to
offer safe mode after an interrupted boot. If the editor cannot start, try
`quantum-editor.exe --safe-mode` or `--reset-layout`; use
[Stability & Recovery](../editor/stability-and-recovery.md) for the complete recovery
workflow.

## Where can I get help or report bugs?

- **Discord** — [discord.gg/gSHUVHXNwP](https://discord.gg/gSHUVHXNwP) for questions and
  discussion.
- **GitHub** — [github.com/alguemqualquer123/quantum](https://github.com/alguemqualquer123/quantum)
  for issues and contributions. For editor crashes, attach the
  [`editor.log`](#where-can-i-find-the-editor-crash-log) described above.

## How can I contribute?

Code contributions go through pull requests on GitHub. Documentation lives in its own
repository and accepts fixes through the **Edit this page** links — see the
[Documentation Guide](../contributing/documentation-guide.md).
