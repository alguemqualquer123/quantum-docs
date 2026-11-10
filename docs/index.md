---
hide_title: true
description: Official documentation for Quantum — a C++17 game engine and visual editor for 2D/3D games, Lua/C++ scripting, rendering, networking, and release automation.
---

<div class="dx-hero" markdown>

<span class="dx-hero-badge">C++17 · Lua · Open Source</span>

# Build worlds. Ship runtimes. <span class="dx-text-gradient">Stay in control.</span> { .dx-hero-title }

Welcome to the official documentation for **Quantum Engine** — a free, lightweight,
and efficient open-source game engine with an integrated editor for creating 2D and
3D games. Script in **Lua** or **C++**, author scenes in the editor, validate real frames,
and ship a tested runtime across desktop, mobile, and web targets.

<div class="dx-hero-actions" markdown>
[Get Started](getting-started/introduction.md){ .dx-btn .dx-btn-primary }
[Editor &amp; runtime workflow](getting-started/the-editor.md){ .dx-btn .dx-btn-outline }
</div>

</div>

!!! note "Documentation status"
    This documentation covers the editor workflow, runtime architecture, core
    subsystems, build targets, and the current public API surface exposed by the
    Quantum source tree. Quantum is moving quickly, so the reference pages are written
    to be practical guides rather than frozen ABI guarantees.

## Start here

<div class="dx-cards" markdown>

<a class="dx-card" href="getting-started/introduction/">
<p class="dx-card-title">Introduction</p>
<p class="dx-card-desc">What Quantum is, its architecture, and what you can build with it.</p>
</a>

<a class="dx-card" href="getting-started/installation/">
<p class="dx-card-title">Installation</p>
<p class="dx-card-desc">Download a prebuilt editor or build Quantum from source.</p>
</a>

<a class="dx-card" href="getting-started/first-project/">
<p class="dx-card-title">Your First Project</p>
<p class="dx-card-desc">Create a scene, add an entity, and run your first game.</p>
</a>

<a class="dx-card" href="manual/entity-component-system/">
<p class="dx-card-title">Entity Component System</p>
<p class="dx-card-desc">Understand the data-oriented ECS at the core of the engine.</p>
</a>

<a class="dx-card" href="reference/">
<p class="dx-card-title">API Reference</p>
<p class="dx-card-desc">Complete class reference with C++ and Lua on every page.</p>
</a>

<a class="dx-card" href="manual/networking/">
<p class="dx-card-title">Multiplayer</p>
<p class="dx-card-desc">Authenticated UDP, replication policy, reconnect soak, and two-player Network Play.</p>
</a>

<a class="dx-card" href="manual/asset-pipeline/">
<p class="dx-card-title">Assets &amp; releases</p>
<p class="dx-card-desc">Deep asset audits, DXPK2 integrity, manifests, and release artifact hashes.</p>
</a>

</div>

## Why Quantum

<div class="dx-feature-grid" markdown>

<div class="dx-feature" markdown>
**2D &amp; 3D Engine**
<p>Full support for both 2D and 3D development — sprites, tilemaps, 3D models, skeletal animation, and more in one lean workflow.</p>
</div>

<div class="dx-feature" markdown>
**Built-in Editor**
<p>Scene hierarchy, properties inspector, animation timeline, integrated code editor, and resource management — all in one place.</p>
</div>

<div class="dx-feature" markdown>
**Lua &amp; C++**
<p>Prototype quickly in Lua or compile C++ at build time for maximum native performance. Combine both seamlessly.</p>
</div>

<div class="dx-feature" markdown>
**Entity Component System**
<p>A modern, data-driven ECS that maximizes CPU cache performance while keeping the engine lightweight and efficient.</p>
</div>

<div class="dx-feature" markdown>
**Cross-Platform**
<p>Build for Windows, Linux, macOS, Android, iOS, and WebGL2 with platform-specific release manifests and smoke gates.</p>
</div>

<div class="dx-feature" markdown>
**PBR Rendering**
<p>Physically-based rendering with dynamic shadows, fog, sky system, water, and advanced materials for photorealistic visuals.</p>
</div>

<div class="dx-feature" markdown>
**Editor Export Pipeline**
<p>Scene serialization, script generation, shader compilation, and platform-specific project generation live in the editor.</p>
</div>

<div class="dx-feature" markdown>
**Production diagnostics**
<p>Crash sidecars, safe mode, script lint/debug, asset verification, frame capture, and artifact hashing keep failures observable.</p>
</div>

</div>

## The editor

![Quantum atmosphere runtime capture with HDR, TAA, and analytical atmosphere](assets/screenshots/quantum-atmosphere-banner.png)

Quantum ships with a visual editor for scene structure, assets, properties,
animation, code, terrain, shader variants, Network Play, and export. Learn more
in [The Editor](editor/index.md), or jump to [Network Play](editor/network-play.md)
and [stability &amp; recovery](editor/stability-and-recovery.md).

---

!!! note "Documentation status"
    The docs distinguish integrated runtime paths from roadmap items. Backend- and
    GPU-specific visual baselines, artistic rendering fixtures, signing/notarization, matchmaking/NAT, and the
    editor Play debugger endpoint remain explicit follow-up work.
