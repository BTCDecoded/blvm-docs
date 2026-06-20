#!/usr/bin/env python3
"""Post-process mdBook HTML: convert mermaid code fences to rendered diagrams."""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

MERMAID_SCRIPT = """<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true, theme: 'default' });
</script>"""

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


def inject_script(content: str) -> str:
    if "mermaid.min.js" in content:
        return content
    if "</body>" in content:
        return content.replace("</body>", MERMAID_SCRIPT + "\n</body>", 1)
    if "</head>" in content:
        return content.replace("</head>", MERMAID_SCRIPT + "\n</head>", 1)
    return content


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
        if "mermaid.min.js" not in new_text:
            new_text = inject_script(new_text)
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
