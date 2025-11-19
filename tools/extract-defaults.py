#!/usr/bin/env python3
"""
Extract configuration defaults from source code.
Minimal, bespoke solution for bllvm-docs.
Run from bllvm-docs directory: python3 tools/extract-defaults.py
"""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
# In CI, repos are checked out as siblings; locally, they're siblings too
ROOT_DIR = DOCS_DIR.parent
OUTPUT_FILE = DOCS_DIR / "CONFIGURATION_DEFAULTS.md"

def extract_value_from_function(func_body):
    """Extract default value from function body."""
    # Simple return statement: return 123;
    m = re.search(r'return\s+(\d+)\s*;', func_body)
    if m:
        return m.group(1)
    
    # Direct value: 123
    m = re.search(r'^\s*(\d+)\s*$', func_body, re.MULTILINE)
    if m:
        return m.group(1)
    
    # Expression: 512 * 1024 * 1024
    m = re.search(r'(\d+)\s*\*\s*(\d+)(?:\s*\*\s*(\d+))?', func_body)
    if m:
        val = int(m.group(1)) * int(m.group(2))
        if m.group(3):
            val *= int(m.group(3))
        return str(val)
    
    # With comment: 300 // 5 minutes
    m = re.search(r'(\d+)\s*//\s*(.+)', func_body)
    if m:
        return f"{m.group(1)} ({m.group(2).strip()})"
    
    # String: "mainnet"
    m = re.search(r'"([^"]+)"', func_body)
    if m:
        return f'"{m.group(1)}"'
    
    # Boolean
    if 'true' in func_body:
        return 'true'
    if 'false' in func_body:
        return 'false'
    
    return None

def extract_defaults_from_file(file_path):
    """Extract all default_* functions from Rust file."""
    if not file_path.exists():
        return []
    
    content = file_path.read_text()
    defaults = []
    
    # Skip helper functions (too generic)
    skip_functions = {'default_true', 'default_false', 'default_zero'}
    
    # Find all default_* functions
    # Match function with body that may span multiple lines
    pattern = r'fn (default_\w+)\(\) -> [^{]+\{([^}]+)\}'
    
    for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
        func_name = match.group(1)
        
        # Skip helper functions
        if func_name in skip_functions:
            continue
        
        func_body = match.group(2)
        
        value = extract_value_from_function(func_body)
        if value:
            setting = func_name.replace('default_', '').replace('_', '.')
            defaults.append((setting, value, func_name))
    
    return defaults

def categorize(setting):
    """Categorize setting by name."""
    s = setting.lower()
    if 'cache' in s or 'pruning' in s or 'storage' in s:
        return 'Storage'
    elif 'peer' in s or 'network' in s or 'connection' in s or 'timeout' in s or 'addr' in s:
        return 'Network'
    elif 'rate' in s or 'rpc' in s or 'auth' in s:
        return 'RPC'
    elif 'module' in s:
        return 'Modules'
    elif 'dos' in s or 'ban' in s or 'protection' in s:
        return 'DoS Protection'
    else:
        return 'Other'

def main():
    output = []
    output.append("# Configuration Defaults")
    output.append("")
    output.append("<!-- Auto-generated from source code -->")
    output.append("<!-- Regenerate: cd bllvm-docs && python3 tools/extract-defaults.py -->")
    output.append("")
    
    # Extract from bllvm-node
    node_config = ROOT_DIR / "bllvm-node" / "src" / "config" / "mod.rs"
    if node_config.exists():
        defaults = extract_defaults_from_file(node_config)
        if defaults:
            output.append("## bllvm-node Defaults")
            output.append("")
            
            # Group by category
            categories = {}
            for setting, value, func_name in defaults:
                cat = categorize(setting)
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append((setting, value, func_name))
            
            # Output by category
            for cat in ['Storage', 'Network', 'RPC', 'Modules', 'DoS Protection', 'Other']:
                if cat in categories:
                    output.append(f"### {cat} Configuration")
                    output.append("")
                    output.append("| Setting | Default Value | Source |")
                    output.append("|---------|---------------|--------|")
                    for setting, value, func_name in sorted(categories[cat]):
                        output.append(f"| `{setting}` | {value} | `{func_name}()` |")
                    output.append("")
            
            output.append(f"[Source: bllvm-node/src/config/mod.rs](../../bllvm-node/src/config/mod.rs)")
            output.append("")
    
    # Extract from bllvm-commons
    commons_config = ROOT_DIR / "bllvm-commons" / "bllvm-commons" / "src" / "config.rs"
    if commons_config.exists():
        defaults = extract_defaults_from_file(commons_config)
        if defaults:
            output.append("## bllvm-commons Defaults")
            output.append("")
            output.append("| Setting | Default Value | Source |")
            output.append("|---------|---------------|--------|")
            for setting, value, func_name in sorted(defaults):
                output.append(f"| `{setting}` | {value} | `{func_name}()` |")
            output.append("")
            output.append(f"[Source: bllvm-commons/bllvm-commons/src/config.rs](../../bllvm-commons/bllvm-commons/src/config.rs)")
            output.append("")
    
    # Write output
    OUTPUT_FILE.write_text('\n'.join(output))
    print(f"✅ Generated: {OUTPUT_FILE}")
    print(f"   Extracted {sum(len(extract_defaults_from_file(f)) for f in [node_config, commons_config] if f.exists())} defaults")

if __name__ == '__main__':
    main()
