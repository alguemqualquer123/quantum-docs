---
description: An overview of Quantum Engine — its architecture, features, and what you can build with it.
---

# Introduction

**Quantum Engine** is a free, open-source 2D/3D game engine with an integrated editor
for building cross-platform games and interactive projects. It combines a lightweight,
data-oriented runtime with a modern desktop editor, so you can author scenes visually,
script in Lua or C++, and export to multiple platforms from a single environment.

Quantum is maintained by SR VINIX as a focused C++17 engine/editor stack. The
repository combines the runtime, editor, headless tools, templates, and platform
workflows in one source tree.

## Design philosophy

Quantum is built around a few core principles:

- **Lightweight and efficient** — no heavy GUI overhead or unnecessary processing. The
  engine stays lean and produces small output.
- **Data-oriented design** — an Entity Component System (ECS) arranges data to take
  advantage of CPU caching, avoiding the performance pitfalls of traditional
  object-oriented designs.
- **Two languages, one workflow** — use **Lua** for rapid iteration and flexible
  scripting, or **C++** for full native performance. C++ scripts are compiled at build
  time, not runtime.
- **Independent runtime** — export turns scenes and bundles into C++ that builds and
  runs without the editor. See
  [how export works](../editor/export.md#from-editor-data-to-runtime-code).
- **Observable production workflow** — real-frame captures, shader matrices, asset
  manifests, crash sidecars, and release artifact hashes make the pipeline testable.

## Documentation structure

This documentation follows a broad structure similar to large engine manuals:

| Section | Use it for |
| --- | --- |
| Getting Started | Install Quantum, understand the editor, and create a first project |
| Tutorials | Step-by-step 2D, 3D, and export walkthroughs |
| Editor | Panels, project workflow, assets, code editing, animation, and export tools |
| Manual | Engine concepts and subsystem guides |
| Reference | API maps, components, Lua bindings, and build options |
| Building | Platform-specific toolchain setup |

## What you can build

| Capability | Description |
| --- | --- |
| 2D games | Sprites, tilemaps, sprite slicing, and 2D physics |
| 3D games | GLTF/OBJ/FBX models, PBR materials, dynamic shadows, fog, sky, and water |
| Animation | Skeletal animation, morph targets, and a timeline editor |
| UI | A built-in UI system for menus, HUDs, and overlays |
| Physics | Integrated 2D and 3D physics via Box2D and Jolt Physics |
| Audio | 3D positional audio |
| Monetization | AdMob ads and in-app purchases (Google Play and the App Store) on mobile, and the SDKs of five web game portals — see [Monetization](../manual/monetization.md) |

## Engine features

- 2D and 3D scenes with a shared ECS foundation
- GLTF and OBJ model loading, and FBX import
- Skeletal animation and morph targets
- PBR materials, dynamic shadows, fog, sky, and water
- HDR post-processing with bloom, TAA, motion blur, LUT grading, SSGI, SSR, decals,
  clustered forward lighting, and analytical atmosphere
- Particle systems, UI, terrain LOD, mesh LOD, and instancing
- Authenticated UDP networking, replication policy, prediction, reconnect, and
  two-window local multiplayer testing
- Headless Lua lint/debug, visual-script graph validation, deep asset verification,
  DXPK2 resource-pack integrity, and release smoke reports
- Scene serialization, texture and shader pools, and multithreading
- 3D audio
- Google AdMob ads, Google Play and App Store in-app purchases, and web game portal SDKs

!!! tip "Custom shaders"
    Fork, edit, and customize the built-in shaders for Mesh, UI, Points, Lines, Sky, and
    Water components directly in the editor — see [Custom Shaders](../editor/custom-shaders.md).

## Platforms

| Area | Support |
| --- | --- |
| Editor downloads | Windows, Linux, macOS |
| Project targets | Windows, Linux, macOS, Android, iOS, HTML5 |
| Graphics APIs | OpenGL, Vulkan, Metal, DirectX |
| Scripting | Lua, C++ |

## Next steps

<div class="dx-cards" markdown>

<a class="dx-card" href="../installation/">
<p class="dx-card-title">Installation →</p>
<p class="dx-card-desc">Download the editor or build Quantum from source.</p>
</a>

<a class="dx-card" href="../first-project/">
<p class="dx-card-title">Your First Project →</p>
<p class="dx-card-desc">Build and run your first Quantum scene.</p>
</a>

<a class="dx-card" href="../../manual/architecture/">
<p class="dx-card-title">Architecture →</p>
<p class="dx-card-desc">Learn how the runtime is organized internally.</p>
</a>

</div>
