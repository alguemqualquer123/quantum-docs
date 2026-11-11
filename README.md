# Quantum Engine Documentation

Official documentation for [Quantum](https://github.com/alguemqualquer123/quantum),
the C++17 game engine and visual editor maintained by SR VINIX. Published at
<https://alguemqualquer123.github.io/quantum-docs/>. Built with
[MkDocs](https://www.mkdocs.org/).

Documentation content lives in [`docs/`](docs/). The site is organized into:

- `getting-started/` — orientation, installation, and first project pages
- `tutorials/` — step-by-step workflows
- `editor/` — editor panels, project workflow, resources, animation, code, and export
- `manual/` — engine concepts and subsystem guides
- `reference/` — API reference, enumerations, and build options
- `contributing/` — documentation and screenshot contribution notes

The current docs also cover authenticated networking, Network Play, rendering
validation, Lua tooling, DXPK2 asset integrity, editor recovery, and release
artifact smoke reports.

## Engine release versions

The current stable engine release is **[Quantum v0.8.3](https://github.com/alguemqualquer123/quantum/releases/tag/v0.8.3)**.
The documentation site keeps the latest stable manual at its root, publishes the
development documentation under [`unstable/`](https://alguemqualquer123.github.io/quantum-docs/unstable/),
and exposes patch releases through the version selector. The engine repository is
at <https://github.com/alguemqualquer123/quantum>.

## Local development

Install the dependencies (MkDocs + PyMdown Extensions):

```bash
pip install -r requirements.txt
```

Serve the site locally with live reload:

```bash
mkdocs serve
```

Then open <http://127.0.0.1:8000>.

## Building

Produce a static site in the `site/` directory:

```bash
mkdocs build --strict
```

## License

Documentation content is licensed under
[CC&nbsp;BY&nbsp;4.0](https://creativecommons.org/licenses/by/4.0/).
