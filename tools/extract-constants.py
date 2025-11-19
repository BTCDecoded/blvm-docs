#!/usr/bin/env python3
"""
Extract consensus constants from source code.
Minimal, bespoke solution for bllvm-docs.
Run from bllvm-docs directory: python3 tools/extract-constants.py
"""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
ROOT_DIR = DOCS_DIR.parent
OUTPUT_FILE = DOCS_DIR / "PROTOCOL_CONSTANTS.md"

def extract_doc_comment(content, pos):
    """Extract doc comment before a position."""
    # Look backwards for doc comments
    lines = content[:pos].split('\n')
    doc_lines = []
    
    # Check last few lines for doc comments
    for line in reversed(lines[-10:]):
        stripped = line.strip()
        if stripped.startswith('///'):
            doc_lines.insert(0, stripped[3:].strip())
        elif stripped.startswith('//!'):
            doc_lines.insert(0, stripped[3:].strip())
        elif stripped and not stripped.startswith('//'):
            break
    
    return ' '.join(doc_lines) if doc_lines else None

def extract_constants_from_file(file_path):
    """Extract pub const declarations from Rust file."""
    if not file_path.exists():
        return []
    
    content = file_path.read_text()
    constants = []
    
    # Pattern: pub const NAME: Type = value;
    # Also handle multi-line values
    pattern = r'pub const (\w+):\s*(\w+(?:<[^>]+>)?)\s*=\s*([^;]+);'
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1)
        type_ = match.group(2)
        value = match.group(3).strip()
        
        # Clean up value (remove newlines, extra spaces)
        value = ' '.join(value.split())
        
        # Format large numbers with commas
        if value.isdigit() and len(value) > 3:
            value = f"{int(value):,}"
        elif '_' in value and value.replace('_', '').replace('*', '').replace(' ', '').isdigit():
            # Handle expressions like "21_000_000 * 100_000_000"
            try:
                # Simple evaluation for multiplication
                eval_value = eval(value.replace('_', ''))
                if isinstance(eval_value, int) and eval_value > 1000:
                    value = f"{eval_value:,}"
            except:
                pass
        
        # Get doc comment
        doc = extract_doc_comment(content, match.start())
        
        constants.append({
            'name': name,
            'type': type_,
            'value': value,
            'doc': doc
        })
    
    return constants

def categorize_constant(name):
    """Categorize constant by name."""
    name_lower = name.lower()
    if 'block' in name_lower or 'weight' in name_lower or 'size' in name_lower:
        return 'Block Limits'
    elif 'tx' in name_lower or 'transaction' in name_lower:
        return 'Transaction Limits'
    elif 'script' in name_lower or 'stack' in name_lower or 'ops' in name_lower:
        return 'Script Limits'
    elif 'subsidy' in name_lower or 'halving' in name_lower or 'money' in name_lower:
        return 'Monetary Policy'
    elif 'difficulty' in name_lower or 'target' in name_lower or 'time' in name_lower:
        return 'Difficulty Adjustment'
    elif 'satoshis' in name_lower or 'btc' in name_lower:
        return 'Units'
    else:
        return 'Other'

def main():
    output = []
    output.append("# Protocol Constants")
    output.append("")
    output.append("<!-- Auto-generated from source code -->")
    output.append("<!-- Regenerate: cd bllvm-docs && python3 tools/extract-constants.py -->")
    output.append("")
    output.append("Bitcoin protocol constants extracted from `bllvm-consensus` source code.")
    output.append("")
    
    # Extract from bllvm-consensus
    constants_file = ROOT_DIR / "bllvm-consensus" / "src" / "constants.rs"
    if constants_file.exists():
        constants = extract_constants_from_file(constants_file)
        if constants:
            # Group by category
            categories = {}
            for const in constants:
                cat = categorize_constant(const['name'])
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(const)
            
            # Output by category
            category_order = [
                'Block Limits',
                'Transaction Limits',
                'Script Limits',
                'Monetary Policy',
                'Difficulty Adjustment',
                'Units',
                'Other'
            ]
            
            for cat in category_order:
                if cat in categories:
                    output.append(f"## {cat}")
                    output.append("")
                    output.append("| Constant | Type | Value | Description |")
                    output.append("|----------|------|-------|-------------|")
                    
                    for const in sorted(categories[cat], key=lambda x: x['name']):
                        doc = const['doc'] or ""
                        # Clean up doc (remove markdown links, etc.)
                        doc = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', doc)
                        output.append(f"| `{const['name']}` | `{const['type']}` | {const['value']} | {doc} |")
                    
                    output.append("")
            
            output.append(f"[Source: bllvm-consensus/src/constants.rs](../../bllvm-consensus/src/constants.rs)")
            output.append("")
    
    # Write output
    OUTPUT_FILE.write_text('\n'.join(output))
    print(f"✅ Generated: {OUTPUT_FILE}")
    print(f"   Extracted {len(constants) if constants_file.exists() else 0} constants")

if __name__ == '__main__':
    main()

