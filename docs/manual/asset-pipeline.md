---
description: Asset indexing, deep validation, deterministic resource packs, and release integrity checks in Quantum.
---

# Asset pipeline

The editor maintains `.quantum/assetdb.json` (format 2, with format-1 read
compatibility) with paths, types, sizes, mtime, SHA-1 content hashes, dependency
information, and deterministic importer metadata. PNG and JPEG records include
format and dimensions; WAV records include channels, sample rate, bit depth and
duration; OBJ records include vertex, UV, normal and face counts. GLB/glTF records
include deterministic counts for accessors, animations, buffers, images, materials,
meshes, nodes, scenes, skins and textures, plus primitive and morph-target counts,
skin/material-texture/extension flags, and preserve the generator and the FBX importer
marker (`quantumFbxImport`) when present, including source path/hash and texture count.
FBX records include its encoding and declared version when available; imported GLBs
also expose linked source files and resolved versus missing texture references.
External dependencies are collected from structured glTF/GLB `buffers` and `images`
URIs (including percent-escaped paths) and from texture references in ASCII or
printable binary FBX strings. URLs, `data:` URIs and paths that resolve outside the
project are ignored; missing referenced files remain visible to `assets doctor` and
`assets verify`.
The command-line twin can
build and audit the index without loading the editor:

```text
quantum-editor-cmd assets index --project <project>
quantum-editor-cmd assets verify --project <project> --deep --json
quantum-editor-cmd assets doctor --project <project>
quantum-editor-cmd assets import --project <project> [--assets <dir>] [--force] [--json]
```

`assets import` percorre os FBX na raiz de assets configurada (a raiz do projeto por
padrão), verifica o marcador de dependências e grava os GLB derivados em
`<project>/.quantum/imported/`. A execução é incremental; `--force`
reimporta tudo, e o retorno `1` transforma uma conversão com erro em falha de CI.

Deep verification checks image headers and dimensions, GLB/glTF/JSON, common
audio formats, fonts, OBJ/FBX, YAML scenes/materials, and graph assets.

The standalone `quantum-resource-server` keeps its incremental index across
restarts in `<project>/.quantum/resource-index.v1`. The cache is versioned and
written atomically; malformed or oversized caches are ignored, then the normal
scan revalidates file size, mtime, dependencies, and project containment. It is
only a hash-reuse acceleration and never replaces the project tree.

## Deterministic packs

`quantum-resource-compiler` is a headless desktop tool on Windows, Linux and
macOS; its CLI dispatch does not create an editor window. `quantum-resource-compiler pak` writes `DXPK2` packs with a SHA-256 digest of the
unobfuscated body for every entry. The runtime verifies the digest when reading;
the inspector verifies it before listing entries. `DXPK1` remains readable with
its historical structural checks.

```text
quantum-resource-compiler pak --project <project> --out resources.pak
quantum-resource-compiler inspect --pack resources.pak --verify \
  --manifest <project>/.quantum/assetdb.json
```

The manifest comparison reports `MANIFEST_MISSING`, `MANIFEST_CHANGED`, and
`MANIFEST_EXTRA` for the packed `assets/` and `lua/` roots. This closes the gap
between an indexed project and the artifact shipped to a player.

