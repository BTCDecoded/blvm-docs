#!/usr/bin/env python3
"""
Extract error codes from source code.
Minimal, bespoke solution for bllvm-docs.
Run from bllvm-docs directory: python3 tools/extract-errors.py
"""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
ROOT_DIR = DOCS_DIR.parent
OUTPUT_FILE = DOCS_DIR / "ERROR_CODES.md"

def extract_error_enum(file_path, enum_name):
    """Extract error enum variants and their codes."""
    if not file_path.exists():
        return []
    
    content = file_path.read_text()
    errors = []
    
    # Find the enum definition
    enum_pattern = rf'pub enum {enum_name}\s*\{{([^}}]+)\}}'
    enum_match = re.search(enum_pattern, content, re.DOTALL)
    
    if not enum_match:
        return []
    
    enum_body = enum_match.group(1)
    
    # Find impl block with code() method
    impl_pattern = rf'impl {enum_name}\s*\{{[^}}]*pub fn code\(&self\) -> i32\s*\{{([^}}]+)\}}'
    impl_match = re.search(impl_pattern, content, re.DOTALL)
    
    code_map = {}
    if impl_match:
        impl_body = impl_match.group(1)
        # Extract match arms: Variant => code,
        match_pattern = r'RpcErrorCode::(\w+)\s*=>\s*(-?\d+)'
        for match in re.finditer(match_pattern, impl_body):
            variant = match.group(1)
            code = match.group(2)
            code_map[variant] = code
    
    # Find message() method
    message_pattern = rf'pub fn message\(&self\) -> &\'static str\s*\{{([^}}]+)\}}'
    message_match = re.search(message_pattern, content, re.DOTALL)
    
    message_map = {}
    if message_match:
        message_body = message_match.group(1)
        # Extract match arms: Variant => "message",
        msg_pattern = r'RpcErrorCode::(\w+)\s*=>\s*"([^"]+)"'
        for match in re.finditer(msg_pattern, message_body):
            variant = match.group(1)
            message = match.group(2)
            message_map[variant] = message
    
    # Extract enum variants
    variant_pattern = r'(\w+)(?:\([^)]+\))?,?'
    for match in re.finditer(variant_pattern, enum_body):
        variant = match.group(1)
        if variant and variant not in ['ParseError', 'InvalidRequest', 'MethodNotFound']:  # Skip if already found
            # Check if it's a real variant (not a comment or doc)
            if not variant.startswith('//') and variant[0].isupper():
                code = code_map.get(variant, 'N/A')
                message = message_map.get(variant, '')
                errors.append({
                    'variant': variant,
                    'code': code,
                    'message': message
                })
    
    return errors

def extract_rpc_errors(file_path):
    """Extract RPC error codes."""
    return extract_error_enum(file_path, 'RpcErrorCode')

def main():
    output = []
    output.append("# Error Codes")
    output.append("")
    output.append("<!-- Auto-generated from source code -->")
    output.append("<!-- Regenerate: cd bllvm-docs && python3 tools/extract-errors.py -->")
    output.append("")
    output.append("Error codes used across BLLVM components.")
    output.append("")
    
    # Extract RPC errors
    rpc_errors_file = ROOT_DIR / "bllvm-node" / "src" / "rpc" / "errors.rs"
    if rpc_errors_file.exists():
        rpc_errors = extract_rpc_errors(rpc_errors_file)
        if rpc_errors:
            output.append("## RPC Error Codes")
            output.append("")
            output.append("JSON-RPC 2.0 compatible error codes used by `bllvm-node`.")
            output.append("")
            output.append("| Code | Variant | Message | Description |")
            output.append("|------|---------|---------|-------------|")
            
            # Standard JSON-RPC 2.0 codes
            standard_codes = {
                'ParseError': (-32700, 'Parse error', 'Invalid JSON was received'),
                'InvalidRequest': (-32600, 'Invalid Request', 'The JSON sent is not a valid Request object'),
                'MethodNotFound': (-32601, 'Method not found', 'The method does not exist'),
                'InvalidParams': (-32602, 'Invalid params', 'Invalid method parameter(s)'),
                'InternalError': (-32603, 'Internal error', 'Internal JSON-RPC error'),
            }
            
            for variant, (code, message, desc) in standard_codes.items():
                output.append(f"| {code} | `{variant}` | \"{message}\" | {desc} |")
            
            # Bitcoin Core compatible codes
            bitcoin_codes = {
                'TxAlreadyInChain': (-1, 'Transaction already in block chain', 'Transaction is already in the blockchain'),
                'TxRejected': (-25, 'Transaction rejected', 'Transaction was rejected'),
                'TxMissingInputs': (-1, 'Missing inputs', 'Transaction references non-existent inputs'),
                'TxAlreadyInMempool': (-27, 'Transaction already in mempool', 'Transaction is already in the mempool'),
                'BlockNotFound': (-5, 'Block not found', 'Block hash not found'),
                'TxNotFound': (-5, 'Transaction not found', 'Transaction hash not found'),
                'UtxoNotFound': (-5, 'No such UTXO', 'UTXO not found'),
            }
            
            for variant, (code, message, desc) in bitcoin_codes.items():
                output.append(f"| {code} | `{variant}` | \"{message}\" | {desc} |")
            
            output.append("")
            output.append(f"[Source: bllvm-node/src/rpc/errors.rs](../../bllvm-node/src/rpc/errors.rs)")
            output.append("")
    
    # Extract Consensus errors (simpler extraction)
    consensus_errors_file = ROOT_DIR / "bllvm-consensus" / "src" / "error.rs"
    if consensus_errors_file.exists():
        content = consensus_errors_file.read_text()
        # Extract error variants from enum
        error_pattern = r'#\[error\("([^"]+)"\)\]\s*pub enum ConsensusError'
        match = re.search(error_pattern, content)
        if match:
            # Extract all variants
            variant_pattern = r'(\w+)\([^)]+\)'
            variants = re.findall(variant_pattern, content)
            
            if variants:
                output.append("## Consensus Errors")
                output.append("")
                output.append("Error types used by `bllvm-consensus` for validation failures.")
                output.append("")
                output.append("| Variant | Description |")
                output.append("|---------|-------------|")
                
                for variant in variants:
                    # Get the error message from the attribute
                    msg_pattern = rf'#\[error\("([^"]+)"\)\]\s*{variant}'
                    msg_match = re.search(msg_pattern, content)
                    desc = msg_match.group(1) if msg_match else variant
                    output.append(f"| `{variant}` | {desc} |")
                
                output.append("")
                output.append(f"[Source: bllvm-consensus/src/error.rs](../../bllvm-consensus/src/error.rs)")
                output.append("")
    
    # Write output
    OUTPUT_FILE.write_text('\n'.join(output))
    print(f"✅ Generated: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()

