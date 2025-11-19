# Extractable Data for Documentation

This document outlines data that can be automatically extracted from source code to enhance documentation while keeping it timeless.

## Principles

- **Timeless**: No dates, versions, or status updates
- **Code-sourced**: Extracted directly from source, always accurate
- **Contextual**: Dropped into appropriate documentation sections
- **Minimal**: Only extract what adds value

## Extractable Data Types

### 1. API Endpoints

**bllvm-commons REST API**:
- Route definitions (`Router::new().route(...)`)
- HTTP methods (GET, POST)
- Request/response types
- Path parameters

**Extraction Points**:
- `bllvm-commons/src/main.rs` - Main routes
- `bllvm-commons/src/node_registry/api.rs` - Node registry routes

**Use Cases**:
- API reference documentation
- Integration guides
- Webhook documentation

**Example Output**:
```markdown
| Method | Path | Handler | Description |
|--------|------|---------|-------------|
| GET | `/health` | `health_check` | Health status |
| POST | `/webhooks/block` | `handle_block_notification` | Block notifications |
```

---

### 2. RPC Methods

**bllvm-node JSON-RPC**:
- Method names (from `ACTIVE_COMMANDS` constant)
- Method categories (blockchain, network, mining, etc.)
- Parameter validation limits

**Extraction Points**:
- `bllvm-node/src/rpc/control.rs` - `ACTIVE_COMMANDS` array
- `bllvm-node/src/rpc/server.rs` - Method routing
- `bllvm-node/src/rpc/validation.rs` - Validation constants

**Use Cases**:
- RPC reference (already exists, can be auto-updated)
- Method discovery
- Validation limits documentation

**Example Output**:
```markdown
## Available RPC Methods

### Blockchain
- `getblockchaininfo`
- `getblock`
- `getblockhash`
...

### Network
- `getnetworkinfo`
- `getpeerinfo`
...
```

---

### 3. Error Codes

**RPC Error Codes**:
- JSON-RPC 2.0 standard codes
- Bitcoin Core-compatible codes
- Custom error codes

**Extraction Points**:
- `bllvm-node/src/rpc/errors.rs` - `RpcErrorCode` enum
- `bllvm-commons/src/error.rs` - `GovernanceError` enum
- `bllvm-consensus/src/error.rs` - `ConsensusError` enum

**Use Cases**:
- Error handling guides
- API reference
- Troubleshooting

**Example Output**:
```markdown
| Code | Name | Message | Description |
|------|------|---------|-------------|
| -32700 | ParseError | "Parse error" | Invalid JSON |
| -32601 | MethodNotFound | "Method not found" | Unknown RPC method |
| -5 | BlockNotFound | "Block not found" | Block hash not found |
```

---

### 4. Consensus Constants

**Bitcoin Protocol Constants**:
- Block limits (size, weight, inputs, outputs)
- Script limits
- Subsidy and halving
- Difficulty adjustment

**Extraction Points**:
- `bllvm-consensus/src/constants.rs` - All consensus constants
- `bllvm-protocol/src/network_params.rs` - Network-specific constants

**Use Cases**:
- Protocol reference
- Validation limits
- Network parameters

**Example Output**:
```markdown
| Constant | Value | Description |
|----------|-------|-------------|
| `MAX_BLOCK_WEIGHT` | 4,000,000 | Maximum block weight (BIP141) |
| `MAX_TX_SIZE` | 1,000,000 | Maximum transaction size (bytes) |
| `HALVING_INTERVAL` | 210,000 | Blocks between halvings |
| `DIFFICULTY_ADJUSTMENT_INTERVAL` | 2,016 | Blocks between difficulty adjustments |
```

---

### 5. Network Parameters

**Network-Specific Constants**:
- Magic bytes
- Default ports
- Genesis block hashes
- DNS seeds

**Extraction Points**:
- `bllvm-protocol/src/network_params.rs` - `NetworkConstants` struct

**Use Cases**:
- Network configuration
- Protocol reference
- Integration guides

**Example Output**:
```markdown
## Mainnet Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Magic Bytes | `0xf9beb4d9` | P2P protocol identifier |
| Default Port | 8333 | P2P listening port |
| Genesis Hash | `0x6fe28c0a...` | Genesis block hash |
```

---

### 6. Validation Limits

**Input Validation Constants**:
- Maximum string lengths
- Maximum hash lengths
- Maximum block heights
- Maximum fee rates

**Extraction Points**:
- `bllvm-node/src/rpc/validation.rs` - Validation constants

**Use Cases**:
- API reference
- Error handling
- Input validation

**Example Output**:
```markdown
| Limit | Value | Applies To |
|-------|-------|------------|
| `MAX_HEX_STRING_LENGTH` | 2,000,000 | Hex-encoded transactions |
| `MAX_HASH_STRING_LENGTH` | 64 | Hash strings |
| `MAX_BLOCK_HEIGHT` | 2,000,000,000 | Block height values |
```

---

### 7. CLI Commands

**Command-Line Interface**:
- Available commands
- Subcommands
- Command options

**Extraction Points**:
- `bllvm/src/bin/main.rs` - Main CLI
- `bllvm-commons/bllvm-commons/src/bin/*.rs` - Tool CLIs
- `bllvm-sdk/src/bin/*.rs` - SDK tools

**Use Cases**:
- CLI reference
- Usage examples
- Command discovery

**Example Output**:
```markdown
## bllvm Commands

### Node Management
- `start` - Start the node (default)
- `status` - Show node status
- `health` - Health check

### Configuration
- `config show` - Show configuration
- `config validate` - Validate config file
```

---

### 8. Protocol Versions

**Supported Protocol Versions**:
- Version enum variants
- Version-specific parameters

**Extraction Points**:
- `bllvm-protocol/src/lib.rs` - `ProtocolVersion` enum

**Use Cases**:
- Protocol reference
- Compatibility information
- Version selection

---

### 9. Feature Flags

**Compile-Time Features**:
- Available feature flags
- Feature dependencies

**Extraction Points**:
- `Cargo.toml` files - `[features]` sections

**Use Cases**:
- Build configuration
- Feature documentation
- Dependency information

---

## Implementation Strategy

### Phase 1: High-Value Extractions

1. **Consensus Constants** - Most stable, high value
2. **RPC Methods** - Already documented, can auto-update
3. **Error Codes** - Critical for troubleshooting

### Phase 2: API Documentation

4. **REST Endpoints** - For bllvm-commons integration
5. **Network Parameters** - For protocol reference

### Phase 3: Developer Tools

6. **CLI Commands** - For tool documentation
7. **Validation Limits** - For API reference

### Phase 4: Advanced

8. **Feature Flags** - For build documentation
9. **Protocol Versions** - For compatibility

---

## Extraction Tools

### Tool 1: `extract-defaults.py` (Existing)
- Extracts configuration defaults
- ✅ Implemented

### Tool 2: `extract-constants.py` (Proposed)
- Extracts `pub const` declarations
- Groups by category
- Generates constants reference

### Tool 3: `extract-api.py` (Proposed)
- Extracts route definitions
- Extracts RPC method lists
- Generates API reference

### Tool 4: `extract-errors.py` (Proposed)
- Extracts error enums
- Maps codes to messages
- Generates error reference

---

## Integration Points

### Documentation Files

1. **CONFIGURATION_DEFAULTS.md** - ✅ Already using extraction
2. **CONFIGURATION.md** - References extracted defaults
3. **API_REFERENCE.md** (new) - REST and RPC endpoints
4. **PROTOCOL_REFERENCE.md** (new) - Constants and parameters
5. **ERROR_CODES.md** (new) - Error code reference
6. **CLI_REFERENCE.md** (new) - Command-line tools

### GitHub Actions

- Run all extraction tools before Pages deployment
- Generate all reference documents
- Include in documentation site

---

## Example: Constants Extraction

```python
# tools/extract-constants.py
import re
from pathlib import Path

def extract_constants(file_path):
    """Extract pub const declarations."""
    content = file_path.read_text()
    constants = []
    
    # Pattern: pub const NAME: Type = value;
    pattern = r'pub const (\w+):\s*(\w+)\s*=\s*([^;]+);'
    
    for match in re.finditer(pattern, content):
        name = match.group(1)
        type_ = match.group(2)
        value = match.group(3).strip()
        
        # Get doc comment if available
        doc = extract_doc_comment(content, match.start())
        
        constants.append({
            'name': name,
            'type': type_,
            'value': value,
            'doc': doc
        })
    
    return constants
```

---

## Benefits

1. **Accuracy**: Always matches source code
2. **Maintenance**: No manual updates needed
3. **Completeness**: Captures all constants/endpoints
4. **Timeless**: No version numbers or dates
5. **Discoverability**: Easy to find limits and defaults

---

## Next Steps

1. Implement `extract-constants.py` for consensus constants
2. Implement `extract-api.py` for REST/RPC endpoints
3. Implement `extract-errors.py` for error codes
4. Create reference documentation pages
5. Integrate into GitHub Actions workflow

