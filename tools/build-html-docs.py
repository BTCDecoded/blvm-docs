#!/usr/bin/env python3
"""
Build HTML documentation from markdown files.
Creates a styled documentation site for GitHub Pages.
"""
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
BUILD_DIR = DOCS_DIR / "docs"
SRC_DIR = DOCS_DIR

# HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Bitcoin Commons Documentation</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <a href="index.html" class="logo">Bitcoin Commons Documentation</a>
                <span class="version-badge" id="version">v1.0.0</span>
            </div>
        </div>
    </header>

    <div class="main-layout">
        <nav class="sidebar">
            <ul class="sidebar-nav" id="nav">
                {nav_items}
            </ul>
        </nav>

        <main class="content">
            <div id="content"></div>
        </main>
    </div>

    <script>
        // Load version
        fetch('VERSION')
            .then(r => r.text())
            .then(v => {{
                const badge = document.getElementById('version');
                if (badge) badge.textContent = 'v' + v.trim();
            }})
            .catch(() => {{}});

        // Configure marked
        marked.setOptions({{
            highlight: function(code, lang) {{
                if (lang && hljs.getLanguage(lang)) {{
                    return hljs.highlight(code, {{ language: lang }}).value;
                }}
                return hljs.highlightAuto(code).value;
            }},
            breaks: true,
            gfm: true
        }});

        // Load and render markdown
        fetch('{md_file}')
            .then(r => r.text())
            .then(md => {{
                document.getElementById('content').innerHTML = marked.parse(md);
                // Update active nav
                const current = '{html_file}';
                document.querySelectorAll('.sidebar-nav a').forEach(a => {{
                    a.classList.remove('active');
                    if (a.getAttribute('href') === current) {{
                        a.classList.add('active');
                    }}
                }});
            }})
            .catch(e => {{
                document.getElementById('content').innerHTML = '<p>Documentation not found.</p>';
            }});
    </script>
</body>
</html>
"""

# Navigation items
NAV_ITEMS = [
    ("index.html", "Home"),
    ("QUICK_START.html", "Quick Start"),
    ("ARCHITECTURE.html", "Architecture"),
    ("INTEGRATION.html", "Integration"),
    ("CONFIGURATION.html", "Configuration"),
    ("TROUBLESHOOTING.html", "Troubleshooting"),
    ("PERFORMANCE_TUNING.html", "Performance Tuning"),
    ("BEST_PRACTICES.html", "Best Practices"),
    ("CONFIGURATION_DEFAULTS.html", "Configuration Defaults"),
    ("PROTOCOL_CONSTANTS.html", "Protocol Constants"),
    ("RPC_METHODS.html", "RPC Methods"),
    ("ERROR_CODES.html", "Error Codes"),
]

def get_title_from_md(md_content):
    """Extract title from markdown (first # heading)."""
    match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    return match.group(1).strip() if match else "Documentation"

def build_nav_items(current_file):
    """Build navigation HTML."""
    items = []
    for href, label in NAV_ITEMS:
        active = 'class="active"' if href == current_file else ''
        items.append(f'<li><a href="{href}" {active}>{label}</a></li>')
    return '\n'.join(items)

def build_docs():
    """Build HTML documentation from markdown."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    (BUILD_DIR / "assets" / "css").mkdir(parents=True, exist_ok=True)
    
    # Copy CSS (if source is different from destination)
    css_src = DOCS_DIR / "docs" / "assets" / "css" / "style.css"
    css_dst = BUILD_DIR / "assets" / "css" / "style.css"
    if css_src.exists() and css_src != css_dst:
        import shutil
        shutil.copy2(css_src, css_dst)
    
    # Copy VERSION
    version_file = DOCS_DIR / "VERSION"
    if version_file.exists():
        import shutil
        shutil.copy2(version_file, BUILD_DIR / "VERSION")
    
    # Build HTML for each markdown file
    md_files = list(SRC_DIR.glob("*.md"))
    
    for md_file in md_files:
        if md_file.name.startswith('_') or md_file.name in ['README.md']:
            continue
        
        md_content = md_file.read_text()
        title = get_title_from_md(md_content)
        html_file = md_file.stem + ".html"
        
        nav_items = build_nav_items(html_file)
        
        html = HTML_TEMPLATE.format(
            title=title,
            nav_items=nav_items,
            md_file=md_file.name,
            html_file=html_file
        )
        
        (BUILD_DIR / html_file).write_text(html)
        print(f"✅ Built {html_file}")
    
    # Build index.html
    index_md = SRC_DIR / "INDEX.md"
    if index_md.exists():
        md_content = index_md.read_text()
        title = get_title_from_md(md_content)
        nav_items = build_nav_items("index.html")
        
        html = HTML_TEMPLATE.format(
            title="Bitcoin Commons Documentation",
            nav_items=nav_items,
            md_file="INDEX.md",
            html_file="index.html"
        )
        
        (BUILD_DIR / "index.html").write_text(html)
        print("✅ Built index.html")
    
    print(f"\n✅ Documentation built in {BUILD_DIR}")

if __name__ == '__main__':
    build_docs()

