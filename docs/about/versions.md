---
description: Quantum Engine release history and matching documentation versions.
---

# Engine versions

The documentation site always publishes the newest stable engine release at its
root URL. Previous stable releases remain available under their exact version path,
and `unstable` tracks the `main` branch.

| Engine | Documentation | Status |
| --- | --- | --- |
| [v0.8.3](https://github.com/alguemqualquer123/quantum/releases/tag/v0.8.3) | [0.8.3](../0.8.3/) | Current stable |
| [v0.8.2](https://github.com/alguemqualquer123/quantum/releases/tag/v0.8.2) | [0.8.2](../0.8.2/) | Previous stable |
| `main` | [unstable](../unstable/) | In development |

The version selector in the site header is generated from `versions.json`, so new
release tags are listed automatically by the Pages workflow. Release documentation
is built from the matching documentation tag, while the root URL is rebuilt from the
latest stable tag.
