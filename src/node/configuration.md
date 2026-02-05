# Node Configuration

BLVM node configuration supports different use cases.

## Protocol Variants

The node supports multiple Bitcoin protocol variants: **Regtest** (default, regression testing network for development), **Testnet3** (Bitcoin test network), and **BitcoinV1** (production Bitcoin mainnet). See [Protocol Variants](../protocol/overview.md#protocol-variants) for details.

## Configuration File

Create a `blvm.toml` configuration file:

```toml
[network]
protocol = "regtest"  # or "testnet" or "mainnet"
port = 18444          # P2P port (regtest default)

[storage]
data_dir = "/var/lib/blvm"
backend = "auto"      # Auto-select best available backend (prefers redb)

[rpc]
enabled = true
port = 8332
host = "127.0.0.1"    # Bind address

[mining]
enabled = false
```

## Environment Variables

You can also configure via environment variables:

```bash
export BLVM_NETWORK=testnet
export BLVM_DATA_DIR=/var/lib/blvm
export BLVM_RPC_PORT=8332
```

## Command Line Options

```bash
# Start with specific network
blvm --network testnet

# Use custom config file
blvm --config /path/to/config.toml

# Override data directory
blvm --data-dir /custom/path
```

## Storage Backends

The node uses multiple [storage backends](storage-backends.md) with automatic fallback:

### Database Backends

- **redb** (default, recommended): Production-ready embedded database (see [Storage Backends](storage-backends.md#redb))
- **sled**: Beta, fallback option (see [Storage Backends](storage-backends.md#sled))
- **auto**: Auto-select based on availability (prefers redb, falls back to sled)

### Storage Configuration

```toml
[storage]
data_dir = "/var/lib/blvm"
backend = "auto"  # or "redb", "sled"

[storage.cache]
block_cache_mb = 100
utxo_cache_mb = 50
header_cache_mb = 10

[storage.pruning]
enabled = false
keep_blocks = 288  # Keep last 288 blocks (2 days)
```

### Backend Selection

The system automatically selects the best available backend:
1. Attempts to use redb (default)
2. Falls back to sled if redb fails and sled is available
3. Returns error if no backend is available

### Cache Configuration

Storage cache sizes can be configured:
- **Block cache**: Default 100 MB, caches recently accessed blocks
- **UTXO cache**: Default 50 MB, caches frequently accessed UTXOs
- **Header cache**: Default 10 MB, caches block headers

### Pruning

Pruning reduces storage requirements by removing old block data:

```toml
[storage.pruning]
enabled = true
keep_blocks = 288  # Keep last 288 blocks (2 days)
```

**Pruning Modes:**
- **Disabled** (default): Keep all blocks (full archival node)
- **Light client**: Keep last N blocks (configurable)
- **Full pruning**: Remove all blocks, keep only UTXO set (planned)

**Note**: Pruning reduces storage but limits ability to serve historical blocks to peers.

## Network Configuration

### Transport Options

Configure transport selection (see [Transport Abstraction](transport-abstraction.md)):

```toml
[network]
transport_preference = "tcp_only"  # or "iroh_only", "hybrid"
```

## RBF Configuration

Configure Replace-By-Fee (RBF) behavior with 4 modes: Disabled, Conservative, Standard (default), and Aggressive.

### RBF Modes

**Disabled**: No RBF replacements allowed
```toml
[rbf]
mode = "disabled"
```

**Conservative**: Strict rules with higher fee requirements
```toml
[rbf]
mode = "conservative"
min_fee_rate_multiplier = 2.0
min_fee_bump_satoshis = 5000
min_confirmations = 1
max_replacements_per_tx = 3
cooldown_seconds = 300
```

**Standard** (default): BIP125-compliant RBF
```toml
[rbf]
mode = "standard"
min_fee_rate_multiplier = 1.1
min_fee_bump_satoshis = 1000
```

**Aggressive**: Relaxed rules for miners
```toml
[rbf]
mode = "aggressive"
min_fee_rate_multiplier = 1.05
min_fee_bump_satoshis = 500
allow_package_replacements = true
```

See [RBF and Mempool Policies](rbf-mempool-policies.md) for complete configuration guide.

## Advanced Indexing

Enable address and value range indexing for efficient queries:

```toml
[storage.indexing]
enable_address_index = true
enable_value_index = true
strategy = "eager"  # or "lazy"
max_indexed_addresses = 1000000
```

## Module Configuration

Configure process-isolated modules:

```toml
[modules]
enabled = true
modules_dir = "modules"
enabled_modules = ["blvm-lightning", "blvm-mesh"]
```

See [Module System](../architecture/module-system.md) for module configuration details.

## See Also

- [Node Overview](overview.md) - Node features and architecture
- [Node Operations](operations.md) - Running and managing your node
- [Storage Backends](storage-backends.md) - Detailed storage backend information
- [Transport Abstraction](../protocol/network-protocol.md#transport-abstraction-layer) - Transport options
- [Network Protocol](../protocol/network-protocol.md) - Protocol variants and network configuration
- [Configuration Reference](../reference/configuration-reference.md) - Complete configuration reference
- [Getting Started](../getting-started/installation.md) - Installation guide
- [Troubleshooting](../appendices/troubleshooting.md) - Common configuration issues

