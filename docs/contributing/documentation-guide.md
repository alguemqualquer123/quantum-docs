---
description: How to contribute to the Quantum documentation site.
---

# Documentation Guide

The documentation site is built with MkDocs and a custom Quantum theme. Source pages
live under `docs/`; generated site output lives under `site/`.

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve
mkdocs build --strict
```

## Reference documentation

API reference pages live under `docs/reference/classes/`. Each file documents **one
class** with C++ and Lua on the same page, using the Quantum naming and examples.

**Do not** use a bulk markdown generator in this repo. Pages are edited by hand.

### Inventory tool

To list every bound class, method, and property, run the engine script (reference only):

```bash
cmake --build build --target generate_lua_docs generate_lua_types
```

Use that output when adding or verifying APIs. Then edit the matching
`docs/reference/classes/<name>.md` file and add descriptions for important methods.

### Priority for descriptions

Expand these first when touching the reference: `Engine`, `Scene`, `Object`, `Input`,
`Camera`, `Body2D`, `Body3D`, `PhysicsSystem`, `Mesh`, `Sprite`, `Action`, `Animation`.

### Page structure

1. Short class description
2. Properties / Methods / Events tables with a **Languages** column (`C++ | Lua`)
3. **Method details** for important APIs (tabbed C++ / Lua examples)
4. Enumerations when relevant

## File organization

| Folder | Purpose |
| --- | --- |
| `getting-started/` | Orientation and first-run |
| `tutorials/` | Step-by-step workflows |
| `editor/` | Editor panels and export |
| `manual/` | Concepts (ECS, scripting, events) |
| `reference/classes/` | Per-class API (hand-maintained) |
| `building/` | Platform build setup |

## Screenshots

Screenshots live in `docs/assets/screenshots/` as PNG files.

- Capture the editor at **1920×1080** in its default layout (**View → Reset Layout**),
  so every page shows the same editor.
- Use the whole window when a page walks through a workflow. When it documents one
  panel, menu, or dialog, crop to it at its native size instead of scaling.
- Keep local paths and personal data out of the Output panel and dialogs.
- Name the file after what it shows (`properties-script.png`, `export-desktop.png`) and
  say the same in the alt text.
- Delete a screenshot once no page references it.

## Links

Use relative links. Run `mkdocs build --strict` after nav or path changes.

## Versioned documentation

The published site carries one build per stable patch release plus the
in-development docs from `main`:

| URL | Contents |
| --- | --- |
| `alguemqualquer123.github.io/quantum-docs/` | Latest stable release (canonical URLs) |
| `alguemqualquer123.github.io/quantum-docs/0.8.2/` | Exact `v0.8.2` release |
| `alguemqualquer123.github.io/quantum-docs/unstable/` | Current `main` branch |

`main` is always the unstable docs. Changes land there and reach the stable URLs
only when a release is tagged, so a page describing an unreleased feature does
not have to be held back.

Every stable patch tag gets its own path (`v0.8.2` → `0.8.2`). Pre-release tags
are ignored, so every URL is reproducible and previous releases remain available.

`scripts/build-versions.sh` assembles the whole tree: it builds every release,
mirrors the newest one at the root, and writes `versions.json`, which drives the
version picker in the header. Old builds read that file at runtime, so they list
newer releases without being rebuilt.

`mkdocs serve` builds only the unstable version, and the picker stays hidden
because there is no `versions.json` to read. To preview the full versioned site:

```bash
scripts/build-versions.sh site
python3 -m http.server -d site
```

### Releasing a version

Tag the documentation repository when the matching engine release goes out:

```bash
git tag v0.7.1
git push origin v0.7.1
```

The tag push rebuilds and redeploys every version. Only the tagged commit's own
`docs/` is published for that version, so the tag must point at the commit whose
docs describe the release.

Correcting published docs means moving the tag, since a tag is the only thing
the build reads:

```bash
git commit -am "Fix physics layer description"   # on main
git tag -f v0.7.1 && git push -f origin v0.7.1
```

The `github-pages` environment must allow tags to deploy, or the tag run builds
the site and then fails at the deploy step: under **Settings → Environments →
github-pages → Deployment branches and tags**, `v*` needs a tag rule alongside
the `main` branch rule.

### Layout and theme changes

Only `docs/` and `mkdocs.yml` come from a release tag. Every version is built
with the theme from `main`, so a fix to the header, CSS, or search reaches all
published versions on the next build, and a version tagged before a theme
feature existed still gets it.

The trade-off is that a theme change has to keep rendering older content. Preview
one against the real thing before pushing:

```bash
scripts/build-versions.sh site        # every version, current theme
DOCS_SHARED_THEME=0 scripts/build-versions.sh site   # each version's own theme
```

`versions.json` is a compatibility contract in the other direction: already
published builds parse it with the JavaScript they shipped with. Add fields to
it, never rename or remove them.
