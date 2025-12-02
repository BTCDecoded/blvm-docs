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

**Code**: ```1:170:bllvm-node/src/storage/database.rs```

### sled (Fallback)

**sled** is available as a fallback option:

- **Beta Quality**: Not recommended for production
- **Pure Rust**: No C dependencies
- **Performance**: Good for development and testing
- **Storage**: Key-value storage with B-tree indexing

**Code**: ```131:200:bllvm-node/src/storage/database.rs```

## Backend Selection

The system automatically selects the best available backend:

1. **Attempts redb** (default, preferred)
2. **Falls back to sled** if redb fails and sled is available
3. **Returns error** if no backend is available

**Code**: ```80:129:bllvm-node/src/storage/database.rs```

### Automatic Fallback

```rust
// System automatically tries redb first, falls back to sled if needed
let storage = Storage::new(data_dir)?;
```

**Code**: ```46:73:bllvm-node/src/storage/mod.rs```

## Database Abstraction

The storage layer uses a unified database abstraction:

### Database Trait

```rust
pub trait Database: Send + Sync {
    fn open_tree(&self, name: &str) -> Result<Box<dyn Tree>>;
    fn flush(&self) -> Result<()>;
}
```

**Code**: ```13:19:bllvm-node/src/storage/database.rs```

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

**Code**: ```21:50:bllvm-node/src/storage/database.rs```

## Storage Components

### BlockStore

Stores blocks by hash:

- **Key**: Block hash (32 bytes)
- **Value**: Serialized block data
- **Indexing**: Hash-based lookup

**Code**: ```1:200:bllvm-node/src/storage/blockstore.rs```

### UtxoStore

Manages UTXO set:

- **Key**: OutPoint (36 bytes: txid + output index)
- **Value**: UTXO data (script, amount)
- **Operations**: Add, remove, query UTXOs

**Code**: ```1:200:bllvm-node/src/storage/utxostore.rs```

### ChainState

Tracks chain metadata:

- **Tip Hash**: Current chain tip
- **Height**: Current block height
- **Chain Work**: Cumulative proof-of-work
- **UTXO Stats**: Cached UTXO set statistics

**Code**: ```1:121:bllvm-node/src/storage/chainstate.rs```

### TxIndex

Transaction indexing:

- **Key**: Transaction ID (32 bytes)
- **Value**: Transaction data and metadata
- **Lookup**: Fast transaction retrieval

**Code**: ```1:200:bllvm-node/src/storage/txindex.rs```

## Configuration

### Backend Selection

```toml
[storage]
data_dir = "/var/lib/bllvm"
backend = "auto"  # or "redb", "sled"
```

**Options**:
- `"auto"`: Auto-select based on availability (prefers redb, falls back to sled)
- `"redb"`: Force redb backend
- `"sled"`: Force sled backend

**Code**: ```1:100:bllvm-node/src/config/mod.rs```

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

**Code**: ```1:100:bllvm-node/src/config/mod.rs```

## Performance Characteristics

### redb Backend

- **Read Performance**: Excellent for sequential and random reads
- **Write Performance**: Good for batch writes
- **Storage Efficiency**: Efficient key-value storage
- **Memory Usage**: Moderate memory footprint
- **Production Ready**: ✅ Recommended for production

### sled Backend

- **Read Performance**: Good for sequential reads
- **Write Performance**: Good for batch writes
- **Storage Efficiency**: Efficient with B-tree indexing
- **Memory Usage**: Higher memory footprint
- **Production Ready**: ⚠️ Beta quality, not recommended for production

## Migration

### Backend Migration

The system supports migrating between backends:

1. **Export Data**: Export all data from current backend
2. **Import Data**: Import data into new backend
3. **Verify**: Verify data integrity

**Note**: Automatic migration is planned but not yet implemented.

## Pruning Support

Both backends support pruning:

```toml
[storage.pruning]
enabled = true
keep_blocks = 288  # Keep last 288 blocks (2 days)
```

**Pruning Modes**:
- **Disabled** (default): Keep all blocks
- **Light Client**: Keep last N blocks (configurable)
- **Full Pruning**: Remove all blocks, keep only UTXO set (planned)

**Code**: ```1:200:bllvm-node/src/storage/pruning.rs```

## Error Handling

The storage layer handles backend failures gracefully:

- **Automatic Fallback**: Falls back to alternative backend if primary fails
- **Error Recovery**: Attempts to recover from transient errors
- **Data Integrity**: Verifies data integrity on startup
- **Corruption Detection**: Detects and reports database corruption

**Code**: ```46:73:bllvm-node/src/storage/mod.rs```

## See Also

- [Node Configuration](configuration.md) - Storage configuration options
- [Node Operations](operations.md) - Storage operations and maintenance
- [Pruning](pruning.md) - Pruning configuration and usage


