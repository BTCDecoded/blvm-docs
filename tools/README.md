# Documentation Tools

Minimal tools for maintaining bllvm-docs.

## extract-defaults.py

Extracts configuration defaults from source code in other repositories.

**Usage**:
```bash
cd bllvm-docs
python3 tools/extract-defaults.py
```

**What it does**:
- Reads `bllvm-node/src/config/mod.rs`
- Reads `bllvm-commons/bllvm-commons/src/config.rs`
- Extracts `default_*` functions
- Generates `CONFIGURATION_DEFAULTS.md`

**Requirements**:
- Python 3.6+
- Access to sibling repositories (bllvm-node, bllvm-commons)

**Integration**:
- Run before committing documentation changes
- Can be added to CI to validate docs are up-to-date
