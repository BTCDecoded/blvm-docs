#!/usr/bin/env python3
"""Post-process mdBook HTML: convert mermaid code fences to rendered diagrams."""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

# Match mdBook navy theme (book.toml default-theme / preferred-dark-theme).
MERMAID_INIT = """mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    themeVariables: {
      darkMode: true,
      background: '#161923',
      primaryColor: '#282d3f',
      primaryTextColor: '#bcbdd0',
      primaryBorderColor: '#2b79a2',
      secondaryColor: '#1e2333',
      secondaryTextColor: '#bcbdd0',
      secondaryBorderColor: '#505274',
      tertiaryColor: '#2d334f',
      tertiaryTextColor: '#bcbdd0',
      tertiaryBorderColor: '#737480',
      lineColor: '#737480',
      textColor: '#bcbdd0',
      mainBkg: '#282d3f',
      nodeBorder: '#2b79a2',
      clusterBkg: '#1e2333',
      clusterBorder: '#505274',
      titleColor: '#bcbdd0',
      edgeLabelBackground: '#282d3f',
      noteBkgColor: '#282d3f',
      noteTextColor: '#bcbdd0',
      noteBorderColor: '#505274',
      actorBkg: '#282d3f',
      actorBorder: '#2b79a2',
      actorTextColor: '#bcbdd0',
      signalColor: '#bcbdd0',
      signalTextColor: '#bcbdd0',
      labelBoxBkgColor: '#282d3f',
      labelBoxBorderColor: '#505274',
      labelTextColor: '#bcbdd0',
      loopTextColor: '#bcbdd0',
      activationBkgColor: '#2d334f',
      activationBorderColor: '#2b79a2',
      sequenceNumberColor: '#bcbdd0',
    },
  });"""

MERMAID_SCRIPT = f"""<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  {MERMAID_INIT}
</script>"""

MERMAID_SCRIPT_PATTERN = re.compile(
    r'<script src="https://cdn\.jsdelivr\.net/npm/mermaid@10/dist/mermaid\.min\.js"></script>\s*'
    r"<script>\s*mermaid\.initialize\(\{.*?\}\);\s*</script>",
    re.DOTALL,
)

BLOCK_PATTERN = re.compile(
    r'<pre><code class="language-mermaid">(.*?)</code></pre>',
    re.DOTALL,
)


def process_html(content: str) -> tuple[str, bool]:
    changed = False

    def replace_mermaid(match: re.Match[str]) -> str:
        nonlocal changed
        changed = True
        diagram = html.unescape(match.group(1)).strip()
        return f'<div class="mermaid">\n{diagram}\n</div>'

    content = BLOCK_PATTERN.sub(replace_mermaid, content)
    return content, changed


def inject_script(content: str) -> tuple[str, bool]:
    if MERMAID_SCRIPT_PATTERN.search(content):
        new_content = MERMAID_SCRIPT_PATTERN.sub(MERMAID_SCRIPT, content, count=1)
        return new_content, new_content != content
    if "mermaid.min.js" in content:
        return content, False
    if "</body>" in content:
        return content.replace("</body>", MERMAID_SCRIPT + "\n</body>", 1), True
    if "</head>" in content:
        return content.replace("</head>", MERMAID_SCRIPT + "\n</head>", 1), True
    return content, False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "book_dir",
        nargs="?",
        default="book",
        help="mdBook output directory (default: book)",
    )
    args = parser.parse_args()
    book_dir = Path(args.book_dir)
    if not book_dir.is_dir():
        print(f"::error::book directory not found: {book_dir}", file=sys.stderr)
        return 1

    updated = 0
    script_injected = False
    for path in sorted(book_dir.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if "language-mermaid" not in text and 'class="mermaid"' not in text:
            continue
        new_text, changed = process_html(text)
        new_text, script_changed = inject_script(new_text)
        changed = changed or script_changed
        if script_changed:
            script_injected = True
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
            print(f"Updated: {path}")

    if script_injected:
        print("Mermaid.js injected")
    print(f"postprocess-mermaid: {updated} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
