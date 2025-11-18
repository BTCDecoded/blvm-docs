# Node Configuration

BLLVM node supports flexible configuration for different use cases.

## Protocol Variants

The node supports multiple Bitcoin protocol variants:

- **Regtest** (default): Regression testing network for development
- **Testnet3**: Bitcoin test network
- **BitcoinV1**: Production Bitcoin mainnet

## Configuration File

Create a `bllvm.toml` configuration file:

```toml
[network]
protocol = "regtest"  # or "testnet" or "mainnet"
port = 18444          # P2P port (regtest default)

[storage]
data_dir = "/var/lib/bllvm"
backend = "sled"      # Storage backend

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
export BLLVM_NETWORK=testnet
export BLLVM_DATA_DIR=/var/lib/bllvm
export BLLVM_RPC_PORT=8332
```

## Command Line Options

```bash
# Start with specific network
cargo run -- --network testnet

# Use custom config file
cargo run -- --config /path/to/config.toml

# Override data directory
cargo run -- --data-dir /custom/path
```

## Storage Backends

The node supports multiple storage backends with automatic fallback:

### Database Backends

- **redb** (default, recommended): Production-ready embedded database
- **sled**: Beta, fallback option
- **auto**: Auto-select based on availability (prefers redb, falls back to sled)

### Storage Configuration

```toml
[storage]
data_dir = "/var/lib/bllvm"
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

Pruning allows reducing storage requirements by removing old block data:

```toml
[storage.pruning]
enabled = true
keep_blocks = 288  # Keep last 288 blocks (2 days)
```

**Pruning Modes:**
- **Disabled** (default): Keep all blocks
- **Light client**: Keep last N blocks (configurable)
- **Full pruning**: Remove all blocks, keep only UTXO set (future)

**Note**: Pruning reduces storage but limits ability to serve historical blocks to peers.

## Network Configuration

### Transport Options

- **TCP**: Traditional Bitcoin P2P protocol
- **Iroh/QUIC**: Modern transport protocol (experimental)

### Peer Discovery

- Automatic peer discovery on the network
- Manual peer configuration via config file
- DNS seed support for mainnet/testnet

## Security Settings

⚠️ **Important**: Configure security settings for production use:

- RPC authentication
- Network access controls
- Firewall rules
- Rate limiting

