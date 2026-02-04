# Storage Backends

## Overview

The node supports multiple database backends for persistent storage of blocks, UTXO set, and chain state. The system automatically selects the best available backend with graceful fallback.

## Supported Backends

### redb (Default, Recommended)

**redb** is the default, production-ready embedded database:

- **Pure Rust**: No C dependencies
- **ACID Compliance**: Full ACID transactions
- **Production Ready**: Stable, well-tested
- **Performance**: Optimized for read-heavy workloads
- **Storage**: Efficient key-value storage

**Code**: [database.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database.rs#L1-L170)

### sled (Fallback)

**sled** is available as a fallback option:

- **Beta Quality**: Not recommended for production
- **Pure Rust**: No C dependencies
- **Performance**: Good for development and testing
- **Storage**: Key-value storage with B-tree indexing

**Code**: [database.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database.rs#L131-L200)

### rocksdb (Optional, Bitcoin Core Compatible)

**rocksdb** is an optional high-performance backend with Bitcoin Core compatibility:

- **Bitcoin Core Compatibility**: Can read Bitcoin Core LevelDB databases directly
- **Automatic Detection**: Automatically detects and uses Bitcoin Core data if present
- **Block File Access**: Direct access to Bitcoin Core block files (`blk*.dat`)
- **Format Parsing**: Parses Bitcoin Core's internal data formats
- **High Performance**: Optimized for large-scale blockchain data
- **System Dependency**: Requires `libclang` for build
- **Feature Flag**: `rocksdb` (optional, not enabled by default)

**Bitcoin Core Integration**:
- Automatically detects Bitcoin Core data directories
- Reads LevelDB chainstate databases via RocksDB's LevelDB compatibility
- Accesses block files (`blk*.dat`) with lazy indexing
- Supports mainnet, testnet, regtest, and signet networks

**Code**: [database.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database.rs#L78-L84), ```1:105:blvm-node/src/storage/bitcoin_core_storage.rs```

**Note**: RocksDB and erlay features are mutually exclusive due to dependency conflicts.

## Backend Selection

The system automatically selects the best available backend:

1. **Checks for Bitcoin Core data** (if RocksDB feature enabled) - uses RocksDB if detected
2. **Attempts redb** (default, preferred)
3. **Falls back to sled** if redb fails and sled is available
4. **Falls back to RocksDB** if available and other backends fail
5. **Returns error** if no backend is available

**Code**: [database.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database.rs#L80-L129), ```59:100:blvm-node/src/storage/mod.rs```

### Automatic Fallback

```rust
// System automatically tries redb first, falls back to sled if needed
let storage = Storage::new(data_dir)?;
```

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/mod.rs#L46-L73)

## Database Abstraction

The storage layer uses a unified database abstraction:

### Database Trait

```rust
pub trait Database: Send + Sync {
    fn open_tree(&self, name: &str) -> Result<Box<dyn Tree>>;
    fn flush(&self) -> Result<()>;
}
```

**Code**: [database.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database.rs#L13-L19)

### Tree Trait

```rust
pub trait Tree: Send + Sync {
    fn insert(&self, key: &[u8], value: &[u8]) -> Result<()>;
    fn get(&self, key: &[u8]) -> Result<Option<Vec<u8>>>;
    fn remove(&self, key: &[u8]) -> Result<()>;
    fn contains_key(&self, key: &[u8]) -> Result<bool>;
    fn len(&self) -> Result<usize>;
    fn iter(&self) -> Box<dyn Iterator<Item = Result<(Vec<u8>, Vec<u8>)>> + '_>;
}
```

**Code**: [database.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database.rs#L21-L50)

## Storage Components

### BlockStore

Stores blocks by hash:

- **Key**: Block hash (32 bytes)
- **Value**: Serialized block data
- **Indexing**: Hash-based lookup

**Code**: [blockstore.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/blockstore.rs#L1-L200)

### UtxoStore

Manages UTXO set:

- **Key**: OutPoint (36 bytes: txid + output index)
- **Value**: UTXO data (script, amount)
- **Operations**: Add, remove, query UTXOs

**Code**: [utxostore.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/utxostore.rs#L1-L200)

### ChainState

Tracks chain metadata:

- **Tip Hash**: Current chain tip
- **Height**: Current block height
- **Chain Work**: Cumulative proof-of-work
- **UTXO Stats**: Cached UTXO set statistics

**Code**: [chainstate.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/chainstate.rs#L1-L121)

### TxIndex

Transaction indexing:

- **Key**: Transaction ID (32 bytes)
- **Value**: Transaction data and metadata
- **Lookup**: Fast transaction retrieval

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs#L1-L200)

## Configuration

### Backend Selection

```toml
[storage]
data_dir = "/var/lib/blvm"
backend = "auto"  # or "redb", "sled"
```

**Options**:
- `"auto"`: Auto-select based on availability (checks Bitcoin Core data, prefers redb, falls back to sled/rocksdb)
- `"redb"`: Force redb backend
- `"sled"`: Force sled backend
- `"rocksdb"`: Force rocksdb backend (requires `rocksdb` feature)

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs#L1116-L1130)

### RocksDB Configuration

Enable RocksDB with the `rocksdb` feature:

```bash
cargo build --features rocksdb
```

**System Requirements**:
- `libclang` must be installed (required for RocksDB FFI bindings)
- On Ubuntu/Debian: `sudo apt-get install libclang-dev`
- On Arch: `sudo pacman -S clang`
- On macOS: `brew install llvm`

**Bitcoin Core Detection**:
The system automatically detects Bitcoin Core data directories:
- Mainnet: `~/.bitcoin/` or `~/Library/Application Support/Bitcoin/`
- Testnet: `~/.bitcoin/testnet3/` or `~/Library/Application Support/Bitcoin/testnet3/`
- Regtest: `~/.bitcoin/regtest/` or `~/Library/Application Support/Bitcoin/regtest/`

**Code**: [bitcoin_core_detection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/bitcoin_core_detection.rs#L1-L219)

### Cache Configuration

```toml
[storage.cache]
block_cache_mb = 100
utxo_cache_mb = 50
header_cache_mb = 10
```

**Cache Sizes**:
- **Block Cache**: Default 100 MB, caches recently accessed blocks
- **UTXO Cache**: Default 50 MB, caches frequently accessed UTXOs
- **Header Cache**: Default 10 MB, caches block headers

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs#L1-L100)

## Performance Characteristics

### redb Backend

- **Read Performance**: Excellent for sequential and random reads
- **Write Performance**: Good for batch writes
- **Storage Efficiency**: Efficient key-value storage
- **Memory Usage**: Moderate memory footprint
- **Production Ready**: Recommended for production

### sled Backend

- **Read Performance**: Good for sequential reads
- **Write Performance**: Good for batch writes
- **Storage Efficiency**: Efficient with B-tree indexing
- **Memory Usage**: Higher memory footprint
- **Production Ready**: Beta quality, not recommended for production

## Migration

### Backend Migration

To migrate between backends:

1. **Export Data**: Export all data from current backend
2. **Import Data**: Import data into new backend
3. **Verify**: Verify data integrity

**Note**: Manual migration is supported. Export data from the current backend and import into the new backend.

## Pruning Support

Both backends support pruning:

```toml
[storage.pruning]
enabled = true
keep_blocks = 288  # Keep last 288 blocks (2 days)
```

**Pruning Modes**:
- **Disabled**: Keep all blocks (archival node)
- **Normal**: Conservative pruning (keep recent blocks)
- **Aggressive**: Prune with UTXO commitments (requires utxo-commitments feature)
- **Custom**: Fine-grained control over what to keep

**Code**: [pruning.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/pruning.rs#L1-L200)

## Error Handling

The storage layer handles backend failures gracefully:

- **Automatic Fallback**: Falls back to alternative backend if primary fails
- **Error Recovery**: Attempts to recover from transient errors
- **Data Integrity**: Verifies data integrity on startup
- **Corruption Detection**: Detects and reports database corruption

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/mod.rs#L46-L73)

## See Also

- [Node Configuration](configuration.md) - Storage configuration options
- [Node Operations](operations.md) - Storage operations and maintenance
- [Pruning](pruning.md) - Pruning configuration and usage


