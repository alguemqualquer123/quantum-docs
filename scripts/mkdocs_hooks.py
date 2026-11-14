# MkDocs build hooks: emit the machine-readable artefacts that are derived
# from the nav and therefore must never drift from it.
#
#   robots.txt      crawler policy (the real noindex mechanism is the
#                   <meta name="robots"> tag in theme/main.html; this file
#                   only becomes authoritative if a custom domain is ever
#                   pointed at the site, because on GitHub Pages a
#                   project-site robots.txt is not read from the domain root)
#   llms.txt        the llmstxt.org index of the documentation for AI agents
#   llms-full.txt   the same documentation as one markdown document
#   <key>.txt       the IndexNow ownership key, see scripts/indexnow-submit.py
#
# Wired in mkdocs.yml under `hooks:`. Every file is written into site_dir at
# the end of each build, including the per-version builds, so nothing here
# needs to be kept in sync by hand.

import os
import posixpath
import re

INDEXNOW_KEY = "1368afa1bbe6cc5759e2ce97f03e4b03"

_DESC_LIMIT = 220
_IMAGE_LINE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
_INLINE_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_FENCE = re.compile(r"^```")


def _site_url(config):
    url = config["site_url"] or ""
    return url if url.endswith("/") else url + "/"


def _walk_nav(nav):
    """Yield (section_path, title, md_path) for every leaf of the raw nav."""
    def walk(items, trail):
        for item in items:
            if isinstance(item, dict):
                for title, value in item.items():
                    if isinstance(value, list):
                        yield from walk(value, trail + [title])
                    else:
                        yield trail, title, value
            elif isinstance(item, str):
                yield trail, None, item
    yield from walk(nav, [])


def _first_paragraph(path):
    """A one-line summary of a markdown page.

    Pages carry a curated YAML front matter `description:`; when present it
    wins, because it was written for exactly this purpose. Otherwise the first
    prose paragraph is used.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return ""

    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                for raw in lines[1:i]:
                    if raw.startswith("description:"):
                        desc = raw.split(":", 1)[1].strip().strip("'\"")
                        desc = _INLINE_IMAGE.sub("", desc)
                        desc = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", desc)
                        desc = re.sub(r"\s+", " ", desc).strip()
                        if len(desc) > _DESC_LIMIT:
                            desc = desc[:_DESC_LIMIT].rsplit(" ", 1)[0] + "…"
                        return desc
                start = i + 1
                break

    out, in_fence, started = [], False, False
    for line in lines[start:]:
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped:
            if started:
                break
            continue
        if started:
            out.append(stripped)
            continue
        # Skip headings, images, tables, admonitions, raw html and lists of
        # links: none of them summarise the page.
        if stripped[0] in "#>|!<[":
            continue
        if stripped.startswith("- [") or stripped.startswith("* ["):
            continue
        started = True
        out.append(stripped)
    text = _INLINE_IMAGE.sub("", " ".join(out)).strip()
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_]+", "", text)
    text = re.sub(r"\s+", " ", text)
    if len(text) > _DESC_LIMIT:
        text = text[:_DESC_LIMIT].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return text


def _absolutize(markdown, page_md, base):
    """Rewrite relative .md links to absolute URLs and drop image embeds."""
    doc_dir = posixpath.dirname(page_md)

    def repl(match):
        label, target = match.group(1), match.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        target, _, anchor = target.partition("#")
        if not target:
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(doc_dir, target))
        url = base + resolved.replace(".md", "/")
        if resolved in ("index.md",) or resolved.endswith("/index.md"):
            url = url.rsplit("index/", 1)[0]
        return f"[{label}]({url}{'#' + anchor if anchor else ''})"

    markdown = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", markdown)
    return re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", repl, markdown)


def _strip_frontmatter(text):
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return "\n".join(lines[i + 1:]).lstrip("\n")
    return text


def _write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def on_post_build(*, config):
    site_dir = config["site_dir"]
    docs_dir = config["docs_dir"]
    base = _site_url(config)

    _write(os.path.join(site_dir, f"{INDEXNOW_KEY}.txt"), INDEXNOW_KEY + "\n")

    _write(os.path.join(site_dir, "robots.txt"), "\n".join([
        "# Quantum Engine documentation.",
        "# Archived and in-development builds live under /<version>/ and",
        "# /unstable/ and carry <meta name=\"robots\" content=\"noindex\">, so",
        "# the canonical stable tree at the site root is what gets indexed.",
        "User-agent: *",
        "Allow: /",
        "Disallow: /unstable/",
        "Disallow: /search/",
        "",
        f"Sitemap: {base}sitemap.xml",
        "",
    ]))

    leaves = [(trail, title, md) for trail, title, md in _walk_nav(config["nav"])]

    # --- llms.txt: the index -------------------------------------------------
    out = [
        "# Quantum Engine",
        "",
        "> Quantum is an MIT-licensed C++17 game engine and visual editor for 2D",
        "> and 3D games: an ECS runtime, forward PBR rendering with shadows and",
        "> reflection probes, Lua and C++ scripting, Box2D/Jolt physics, audio,",
        "> networking, CDLOD terrain and a shallow-water simulation, and native",
        "> export to Windows, Linux, macOS, Android, iOS and HTML5.",
        "",
        "Machine-readable index of the official documentation. Every URL is",
        "absolute. The documentation is also available as a single markdown",
        f"document at {base}llms-full.txt.",
        "",
        "## For AI agents",
        "",
        f"- [MCP Server]({base}editor/mcp-server/): the editor exposes an MCP",
        "  server, so an agent can drive projects, scenes and builds directly.",
        f"- [Command-Line Tools]({base}editor/command-line/): headless verbs to",
        "  validate, export and doctor a project without opening the GUI.",
        f"- [Full documentation as markdown]({base}llms-full.txt): every page",
        "  below concatenated, with links absolutized.",
        f"- [Source code](https://github.com/alguemqualquer123/quantum): the",
        "  engine and editor, MIT-licensed, with the repo's own AGENTS.md.",
        "",
    ]

    sections = []
    for trail, title, md in leaves:
        top = trail[0] if trail else (title or md)
        if top not in sections:
            sections.append(top)

    for section in sections:
        out.append(f"## {section}")
        out.append("")
        for trail, title, md in leaves:
            top = trail[0] if trail else (title or md)
            if top != section:
                continue
            label = title or md.replace(".md", "")
            desc = _first_paragraph(os.path.join(docs_dir, md))
            url = base + md.replace(".md", "/")
            if md.endswith("index.md"):
                url = url[: -len("index/")]
            line = f"- [{label}]({url})"
            out.append(f"{line}: {desc}" if desc else line)
        out.append("")

    _write(os.path.join(site_dir, "llms.txt"), "\n".join(out))

    # --- llms-full.txt: everything, in nav order -----------------------------
    full = [
        "# Quantum Engine — complete documentation",
        "",
        f"Canonical source: {base}",
        "Index: " + base + "llms.txt",
        "",
    ]
    for trail, title, md in leaves:
        path = os.path.join(docs_dir, md)
        try:
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
        except OSError:
            continue
        heading = " > ".join([t for t in (trail + [title or ""]) if t])
        url = base + md.replace(".md", "/")
        if md.endswith("index.md"):
            url = url[: -len("index/")]
        full.append(f"\n\n---\n\n# {heading}\n\nSource: {url}\n")
        full.append(_absolutize(_strip_frontmatter(body), md, base))

    _write(os.path.join(site_dir, "llms-full.txt"), "\n".join(full))
