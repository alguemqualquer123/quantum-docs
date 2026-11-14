# scripts/

Build and publication tooling for the documentation site.

- `build-versions.sh` — builds every published version into one tree
  (`site/` canonical stable, `site/<version>/` archived, `site/unstable/`,
  plus `versions.json` for the header picker). This is what CI runs.
- `mkdocs_hooks.py` — MkDocs hook, wired in `mkdocs.yml` under `hooks:`.
  Emits into every build: `robots.txt`, `llms.txt` (the llmstxt.org index,
  descriptions taken from each page's front matter), `llms-full.txt` (the
  whole manual as one markdown document with absolute links) and the IndexNow
  key file. Derived from the nav, so it cannot drift from it.
  `build-versions.sh` copies this file into each release-tag worktree and
  injects it through the generated child config, because the root build comes
  from a tag whose own `mkdocs.yml` predates the hook.
- `make-og-image.py` — regenerates `docs/assets/logo/quantum_og.png`, the
  1200x630 Open Graph / Twitter card composited from the brand logo and a
  hero screenshot. Run it after changing the logo, tagline or hero.
- `indexnow-submit.py` — pushes the indexable URLs of the live sitemap to
  IndexNow (Bing, Yandex, Seznam, Naver). Run it after a deploy; IndexNow
  checks that the key file is reachable first. On the very first run it
  answers HTTP 403 `SiteVerificationNotCompleted` while it verifies the key
  against the host — that is expected; run it again later the same day.

Search-engine ownership proofs are not scripts: paste the code Google Search
Console or Bing Webmaster Tools hands you into `mkdocs.yml` as
`extra.verification_google` / `extra.verification_bing` and `theme/main.html`
emits the matching meta tag.
