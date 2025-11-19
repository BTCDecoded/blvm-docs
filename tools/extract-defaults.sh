#!/bin/bash
# Extract configuration defaults from source code
# Run from bllvm-docs directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
ROOT_DIR="$(dirname "$DOCS_DIR")"

OUTPUT_FILE="$DOCS_DIR/CONFIGURATION_DEFAULTS.md"

cat > "$OUTPUT_FILE" << 'EOFHEAD'
# Configuration Defaults

<!-- Auto-generated from source code -->
<!-- Regenerate: cd bllvm-docs && ./tools/extract-defaults.sh -->

This document lists configuration defaults extracted directly from source code.

EOFHEAD

# Extract from bllvm-node
if [ -f "$ROOT_DIR/bllvm-node/src/config/mod.rs" ]; then
    echo "## bllvm-node Defaults" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    # Extract default functions with simple grep/sed
    grep -E "fn default_\w+\(\) ->" "$ROOT_DIR/bllvm-node/src/config/mod.rs" | \
    while IFS= read -r line; do
        func_name=$(echo "$line" | sed -n 's/.*fn \(default_\w\+\)().*/\1/p')
        if [ -n "$func_name" ]; then
            # Get the value from the function body
            value=$(sed -n "/fn $func_name()/,/^}/p" "$ROOT_DIR/bllvm-node/src/config/mod.rs" | \
                    grep -E "^\s*(return\s+)?[0-9]+" | head -1 | sed 's/.*return\s*//;s/;//;s/\s*$//')
            setting=$(echo "$func_name" | sed 's/default_//;s/_/./g')
            
            if [ -n "$value" ]; then
                echo "| \`$setting\` | $value | \`$func_name()\` |" >> "$OUTPUT_FILE"
            fi
        fi
    done
    
    echo "" >> "$OUTPUT_FILE"
    echo "[Source: bllvm-node/src/config/mod.rs](../../bllvm-node/src/config/mod.rs)" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# Extract from bllvm-commons
if [ -f "$ROOT_DIR/bllvm-commons/bllvm-commons/src/config.rs" ]; then
    echo "## bllvm-commons Defaults" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    # Extract default functions
    grep -E "fn default_\w+\(\) ->" "$ROOT_DIR/bllvm-commons/bllvm-commons/src/config.rs" | \
    while IFS= read -r line; do
        func_name=$(echo "$line" | sed -n 's/.*fn \(default_\w\+\)().*/\1/p')
        if [ -n "$func_name" ]; then
            value=$(sed -n "/fn $func_name()/,/^}/p" "$ROOT_DIR/bllvm-commons/bllvm-commons/src/config.rs" | \
                    grep -E "^\s*(return\s+)?[0-9]+|^\s*\"[^\"]+\"" | head -1 | sed 's/.*return\s*//;s/;//;s/"//g;s/\s*$//')
            setting=$(echo "$func_name" | sed 's/default_//;s/_/./g')
            
            if [ -n "$value" ]; then
                echo "| \`$setting\` | $value | \`$func_name()\` |" >> "$OUTPUT_FILE"
            fi
        fi
    done
    
    echo "" >> "$OUTPUT_FILE"
    echo "[Source: bllvm-commons/bllvm-commons/src/config.rs](../../bllvm-commons/bllvm-commons/src/config.rs)" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

echo "Generated: $OUTPUT_FILE"
