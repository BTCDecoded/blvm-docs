#!/usr/bin/env python3
"""Add the Commons menu to each built book page.

The chapter sidebar stays. This is the site menu from thebitcoincommons.org.
"""
from __future__ import annotations

import sys
from pathlib import Path

NAV = """<nav class="commons-nav" aria-label="Bitcoin Commons">
  <a href="https://thebitcoincommons.org/#pipeline">Specification</a>
  <a href="https://thebitcoincommons.org/#implementations">Install</a>
  <a href="https://thebitcoincommons.org/whitepaper.html">White paper</a>
  <a href="https://thebitcoincommons.org/#governance">Governance</a>
  <a href="https://thebitcoincommons.org/ecosystem.html">Ecosystem</a>
  <a href="https://thebitcoincommons.org/#faq">FAQ</a>
  <a href="https://docs.btcdecoded.org/blvm/" aria-current="page">Documentation</a>
</nav>
"""

MARKER = 'class="commons-nav"'


def insert(html: str) -> str:
    if MARKER in html:
        return html
    needle = "<body>"
    if needle not in html:
        return html
    return html.replace(needle, "<body>\n" + NAV, 1)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "book")
    if not root.is_dir():
        print(f"missing book dir: {root}", file=sys.stderr)
        return 1
    n = 0
    for path in root.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        updated = insert(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            n += 1
    print(f"commons menu inserted in {n} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
