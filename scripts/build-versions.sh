#!/usr/bin/env bash
#
# Builds every published version of the documentation into one output tree:
#
#   site/            latest stable release (mirror, the canonical URLs)
#   site/0.8.2/      an exact release tag
#   site/unstable/   the current main branch
#   site/versions.json   drives the version picker in the header
#
# Every stable patch tag gets its own URL (v0.8.2 -> /0.8.2/). The newest tag
# is also mirrored at the root as the canonical stable manual. Pre-release tags
# (v0.8.0-rc1) are ignored, so the picker lists every reproducible release.
#
# Every version is built with main's theme/, so a layout fix reaches published
# versions on the next build; only docs/ and mkdocs.yml come from the tag
# itself. Set DOCS_SHARED_THEME=0 to build each version with its own theme.
#
# Usage: scripts/build-versions.sh [output-dir]
set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$REPO_ROOT"

OUT="$(realpath -m "${1:-site}")"
SITE_URL="${DOCS_SITE_URL_BASE:-https://alguemqualquer123.github.io/quantum-docs}"
SITE_URL="${SITE_URL%/}"
SHARED_THEME="${DOCS_SHARED_THEME:-1}"

WORKTREES=()
cleanup() {
  rm -f "$REPO_ROOT/.mkdocs.version.yml"
  for w in "${WORKTREES[@]:-}"; do
    [ -n "$w" ] && git worktree remove --force "$w" 2>/dev/null || true
  done
}
trap cleanup EXIT

# checkout <ref> -> sets CHECKOUT_PATH to a throwaway worktree holding that ref.
# Sets a global rather than printing: called in a command substitution it would
# register its worktree in a subshell, and cleanup would never remove it.
CHECKOUT_PATH=""
checkout() {
  local ref="$1" path
  path="$(mktemp -d)/src"
  git worktree add --detach "$path" "$ref" >/dev/null
  WORKTREES+=("$path")
  if [ "$SHARED_THEME" = 1 ]; then
    rm -rf "$path/theme"
    cp -a "$REPO_ROOT/theme" "$path/theme"
  fi
  CHECKOUT_PATH="$path"
}

# build <config-dir> <version-id> <dest-subdir|""> <noindex>
#
# Each build gets a generated child config that INHERITs the version's own
# mkdocs.yml and overrides the version metadata. (A child config rather than
# env vars: mkdocs resolves !ENV values through YAML's implicit types, which
# would read a version like 0.10 as the float 0.1.) It also means a version
# predating the picker still builds with one, since the keys the theme needs
# come from here rather than from that version's mkdocs.yml.
build() {
  local src="$1" id="$2" sub="$3" noindex="$4"
  local dest="$OUT" url="$SITE_URL/" root=""
  if [ -n "$sub" ]; then
    dest="$OUT/$sub"
    url="$SITE_URL/$sub/"
    root="/.."
  fi

  local cfg="$src/.mkdocs.version.yml"
  cat > "$cfg" <<YAML
INHERIT: mkdocs.yml
site_url: '$url'
extra:
  version: '$id'
  version_root: '$root'
  version_noindex: $noindex
YAML

  echo "==> building '$id' -> ${sub:-<root>}"
  mkdocs build --strict -f "$cfg" -d "$dest"
  rm -f "$cfg"
}

declare -A RELEASE_REF=() RELEASE_TITLE=()
RELEASES=()

# Release tags, highest version first. Keep every stable patch release.
while read -r ref; do
  [ -n "$ref" ] || continue
  version="${ref##*/v}"
  case "$version" in *-*) continue ;; esac          # skip pre-releases
  RELEASE_REF[$version]="$ref"
  RELEASE_TITLE[$version]="$version"
  RELEASES+=("$version")
done < <(git for-each-ref --sort=-v:refname --format='%(refname)' 'refs/tags/v[0-9]*')

LATEST="${RELEASES[0]:-}"

rm -rf "$OUT"
mkdir -p "$OUT"

# The root build must come first: mkdocs wipes its own site_dir, and here that
# is the directory the per-version subdirectories live in.
if [ -n "$LATEST" ]; then
  echo "==> latest release '$LATEST' from ${RELEASE_REF[$LATEST]#refs/tags/}"
  checkout "${RELEASE_REF[$LATEST]}"
  build "$CHECKOUT_PATH" "$LATEST" "" false
else
  echo "==> no release tags found; publishing 'unstable' at the root"
  build "$REPO_ROOT" unstable "" false
fi

for version in "${RELEASES[@]:-}"; do
  [ -n "$version" ] || continue
  echo "==> release '$version' from ${RELEASE_REF[$version]#refs/tags/}"
  checkout "${RELEASE_REF[$version]}"
  build "$CHECKOUT_PATH" "$version" "$version" true
done

build "$REPO_ROOT" unstable unstable true

RELEASE_TITLES="{"
for version in "${RELEASES[@]:-}"; do
  [ -n "$version" ] || continue
  RELEASE_TITLES="$RELEASE_TITLES\"$version\":\"${RELEASE_TITLE[$version]}\","
done
RELEASE_TITLES="${RELEASE_TITLES%,}}"
export RELEASE_TITLES

python3 - "$OUT/versions.json" "$LATEST" "${RELEASES[@]:-}" <<'PY'
import json, os, sys

out, latest = sys.argv[1], sys.argv[2]
releases = [s for s in sys.argv[3:] if s]
titles = json.loads(os.environ["RELEASE_TITLES"])

versions = [{"id": "unstable", "title": "unstable", "note": "in development"}]
for release in releases:
    versions.append({
        "id": release,
        "title": titles[release],
        "note": "latest" if release == latest else "",
    })

with open(out, "w") as f:
    json.dump({"latest": latest or "unstable", "versions": versions}, f, indent=2)
    f.write("\n")
PY

echo "==> versions.json"
cat "$OUT/versions.json"
