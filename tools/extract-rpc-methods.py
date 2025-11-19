#!/usr/bin/env python3
"""
Extract RPC methods from source code.
Minimal, bespoke solution for bllvm-docs.
Run from bllvm-docs directory: python3 tools/extract-rpc-methods.py
"""
import re
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
ROOT_DIR = DOCS_DIR.parent
OUTPUT_FILE = DOCS_DIR / "RPC_METHODS.md"

def extract_rpc_methods_from_control(file_path):
    """Extract RPC methods from ACTIVE_COMMANDS constant."""
    if not file_path.exists():
        return []
    
    content = file_path.read_text()
    
    # Find ACTIVE_COMMANDS array
    pattern = r'const ACTIVE_COMMANDS: &\[&str\] = &\[([^\]]+)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return []
    
    methods_str = match.group(1)
    # Extract quoted strings
    methods = re.findall(r'"([^"]+)"', methods_str)
    
    return methods

def categorize_method(method):
    """Categorize RPC method by name."""
    if method.startswith('getblock') or method.startswith('gettx') or method in ['getblockchaininfo', 'getblockcount', 'getblockhash', 'getdifficulty', 'gettxoutsetinfo', 'verifychain', 'gettxoutproof', 'verifytxoutproof']:
        return 'Blockchain'
    elif method.startswith('get') and ('mempool' in method or 'raw' in method or 'tx' in method):
        return 'Mempool & Transactions'
    elif method.startswith('send') or method.startswith('test') or method.startswith('decoderaw'):
        return 'Mempool & Transactions'
    elif method.startswith('getnetwork') or method.startswith('getpeer') or method.startswith('getconnection') or method in ['ping', 'addnode', 'disconnectnode', 'getnettotals', 'clearbanned', 'setban', 'listbanned', 'getaddednodeinfo', 'getnodeaddresses', 'setnetworkactive']:
        return 'Network'
    elif method.startswith('getmining') or method.startswith('getblocktemplate') or method.startswith('submitblock') or method.startswith('estimate') or method.startswith('prioritise'):
        return 'Mining'
    elif method in ['stop', 'uptime', 'getmemoryinfo', 'getrpcinfo', 'help', 'logging', 'gethealth', 'getmetrics']:
        return 'Control'
    elif method.startswith('getblockfilter') or method.startswith('getindexinfo'):
        return 'Indexing'
    else:
        return 'Other'

def main():
    output = []
    output.append("# RPC Methods")
    output.append("")
    output.append("<!-- Auto-generated from source code -->")
    output.append("<!-- Regenerate: cd bllvm-docs && python3 tools/extract-rpc-methods.py -->")
    output.append("")
    output.append("Complete list of available JSON-RPC 2.0 methods in `bllvm-node`.")
    output.append("")
    output.append("For detailed method documentation, see [RPC Reference](../bllvm-node/docs/RPC_REFERENCE.md).")
    output.append("")
    
    # Extract from bllvm-node
    control_file = ROOT_DIR / "bllvm-node" / "src" / "rpc" / "control.rs"
    if control_file.exists():
        methods = extract_rpc_methods_from_control(control_file)
        if methods:
            # Group by category
            categories = {}
            for method in methods:
                cat = categorize_method(method)
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(method)
            
            # Output by category
            category_order = [
                'Blockchain',
                'Mempool & Transactions',
                'Network',
                'Mining',
                'Indexing',
                'Control',
                'Other'
            ]
            
            total = 0
            for cat in category_order:
                if cat in categories:
                    method_list = sorted(categories[cat])
                    total += len(method_list)
                    output.append(f"## {cat} ({len(method_list)} methods)")
                    output.append("")
                    output.append("| Method |")
                    output.append("|--------|")
                    for method in method_list:
                        output.append(f"| `{method}` |")
                    output.append("")
            
            output.append(f"**Total: {total} methods**")
            output.append("")
            output.append(f"[Source: bllvm-node/src/rpc/control.rs](../../bllvm-node/src/rpc/control.rs)")
            output.append("")
            output.append("[Full RPC Reference](../bllvm-node/docs/RPC_REFERENCE.md)")
            output.append("")
    
    # Write output
    OUTPUT_FILE.write_text('\n'.join(output))
    print(f"✅ Generated: {OUTPUT_FILE}")
    print(f"   Extracted {len(methods) if control_file.exists() else 0} RPC methods")

if __name__ == '__main__':
    main()

