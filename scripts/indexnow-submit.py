#!/usr/bin/env python3
# Pushes the canonical documentation URLs to IndexNow, which Bing, Yandex,
# Seznam and Naver poll for changes. This is the account-free half of search
# discovery: the other half (Google Search Console, Bing Webmaster Tools)
# needs the owner's own Google/Microsoft login; see scripts/README.md for the
# account-free half of the pipeline.
#
# Run it AFTER a deploy, because IndexNow validates that the key file is
# reachable at keyLocation before accepting the URL list:
#
#   python scripts/indexnow-submit.py
#
# The key is the same one scripts/mkdocs_hooks.py writes into every build as
# <key>.txt; changing it here without changing it there breaks validation.

import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

KEY = "1368afa1bbe6cc5759e2ce97f03e4b03"
SITE = "https://alguemqualquer123.github.io/quantum-docs/"
HOST = "alguemqualquer123.github.io"
KEY_LOCATION = SITE + KEY + ".txt"
SITEMAP = SITE + "sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"

# Versioned and unstable builds are noindex; submitting them would ask the
# engines to crawl pages we explicitly told them not to index.
EXCLUDE = re.compile(r"^https?://[^/]+/(unstable/|\d+\.\d+(\.\d+)?/)")


def main():
    with urllib.request.urlopen(SITEMAP, timeout=30) as resp:
        tree = ET.fromstring(resp.read())
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [e.text for e in tree.iter(f"{ns}loc") if e.text]
    urls = [u for u in urls if not EXCLUDE.search(u)]
    print(f"{len(urls)} indexable URLs from {SITEMAP}")
    if not urls:
        return 1

    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls[:10000],
    }).encode()
    req = urllib.request.Request(
        ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            print(f"IndexNow answered HTTP {resp.status}")
            return 0 if resp.status in (200, 202) else 1
    except urllib.error.HTTPError as exc:
        print(f"IndexNow answered HTTP {exc.code}: {exc.read().decode()[:400]}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
