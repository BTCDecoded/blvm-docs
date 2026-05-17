# Storage Backends

## Overview

The node supports multiple database backends for persistent storage of blocks, UTXO set, and chain state. When `database_backend = "auto"` (the default), the backend is chosen by build features: **RocksDB** when the `rocksdb` feature is enabled, then TidesDB, Redb, Sled. **Official `blvm` / `blvm-node` default features include `rocksdb`**, so **`auto` usually means RocksDB** unless you build with `--no-default-features` or a custom feature set. See [Configuration Reference](../reference/configuration-reference.md) for the full `database_backend` options. The system falls back gracefully if the preferred backend is unavailable.

## Supported Backends

### rocksdb (typical default via `auto`)

**RocksDB** is the **first choice** when `database_backend = "auto"` and the `rocksdb` cargo feature is enabled (true for default `blvm-node` / `blvm` release builds):

- **High performance** for large chain state
- **Interop**: Can work with **typical** LevelDB-format chain state and `blk*.dat` layouts where supported
- **Build**: Requires system **libclang** / LLVM for the `librocksdb-sys` stack
- **Feature**: `rocksdb` (on by default in `blvm-node` / `blvm` default features)

**Code**: [database/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs), [bitcoin_core_storage.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/bitcoin_core_storage.rs)

**Note**: RocksDB and **erlay** features are mutually exclusive in this tree (dependency conflicts).

### redb (pure Rust)

**redb** is a production-ready embedded database. It is chosen by **`auto` only when** RocksDB and TidesDB are **not** in the build (or you set `database_backend = "redb"`):

- **Pure Rust**: No C dependencies
- **ACID Compliance**: Full ACID transactions
- **Typical use**: `--no-default-features` / minimal builds that omit RocksDB, or explicit operator choice

**Code**: [database/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs)

### tidesdb

**TidesDB** is optional; in **`auto`** it is preferred over Redb/Sled **only when** RocksDB is not enabled. See crate features and [Configuration Reference](../reference/configuration-reference.md).

### sled (Fallback)

**sled** is available as a fallback option:

- **Beta Quality**: Not recommended for production
- **Pure Rust**: No C dependencies
- **Performance**: Good for development and testing
- **Storage**: Key-value storage with B-tree indexing

**Code**: [database/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs)

## Backend Selection

When `database_backend = "auto"`, the node chooses the backend by **build features** in this order:

1. **RocksDB** (if the `rocksdb` feature is enabled)
2. **TidesDB** (if the `tidesdb` feature is enabled and RocksDB is not)
3. **Redb** (if the `redb` feature is enabled and neither RocksDB nor TidesDB is)
4. **Sled** (if the `sled` feature is enabled and no other backend is)

At least one backend feature must be enabled at build time. If the chosen backend fails to open (e.g. missing data dir or lock), the node may fall back to another enabled backend where implemented.

**Interop:** When RocksDB is enabled, the node may detect and use existing LevelDB-format chain data. That is separate from the `auto` selection order above.

**Code**: [database/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs) (`default_backend()`, `fallback_backend()`), [storage/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/mod.rs)

### Automatic Fallback

If the backend chosen by `auto` fails to open, the node may fall back to another enabled backend (see `fallback_backend()` in code).

```rust
// Backend is chosen by default_backend() when using "auto"; fallback on open failure
let storage = Storage::new(data_dir)?;
```

**Code**: [storage/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/mod.rs)

## Database Abstraction

The storage layer uses a unified database abstraction:

### Database Trait

```rust
pub trait Database: Send + Sync {
    fn open_tree(&self, name: &str) -> Result<Box<dyn Tree>>;
    fn flush(&self) -> Result<()>;
}
```

**Code**: [database/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs) (`Database` trait)

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

**Code**: [database/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs) (`Tree` trait)

## Storage Components

### BlockStore

Stores blocks by hash:

- **Key**: Block hash (32 bytes)
- **Value**: Serialized block data
- **Indexing**: Hash-based lookup

**Code**: [blockstore.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/blockstore.rs)

### UtxoStore

Manages UTXO set:

- **Key**: OutPoint (36 bytes: txid + output index)
- **Value**: UTXO data (script, amount)
- **Operations**: Add, remove, query UTXOs

**Code**: [utxostore.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/utxostore.rs)

### ChainState

Tracks chain metadata:

- **Tip Hash**: Current chain tip
- **Height**: Current block height
- **Chain Work**: Cumulative proof-of-work
- **UTXO Stats**: Cached UTXO set statistics

**Code**: [chainstate.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/chainstate.rs)

### TxIndex

Transaction indexing:

- **Key**: Transaction ID (32 bytes)
- **Value**: Transaction data and metadata
- **Lookup**: Fast transaction retrieval

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs)

## Configuration

### Backend Selection

```toml
[storage]
data_dir = "/var/lib/blvm"
database_backend = "auto"  # typical release: RocksDB; or "rocksdb" | "tidesdb" | "redb" | "sled"
```

**Options**:
- `"auto"`: Select by build features (RocksDB when `rocksdb` enabled, then TidesDB, Redb, Sled)
- `"rocksdb"`: Force RocksDB (requires `rocksdb` feature)
- `"tidesdb"`: Force TidesDB (requires `tidesdb` feature)
- `"redb"`: Force redb backend
- `"sled"`: Force sled backend

**Code**: [config](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/) (storage / database_backend)

### RocksDB Configuration

The **`rocksdb`** feature is **enabled by default** in `blvm-node` / `blvm`; you only need flags when building a **minimal** tree without RocksDB:

```bash
cargo build -p blvm-node --features rocksdb
```

**System Requirements**:
- `libclang` must be installed (required for RocksDB FFI bindings)
- On Ubuntu/Debian: `sudo apt-get install libclang-dev`
- On Arch: `sudo pacman -S clang`
- On macOS: `brew install llvm`

**Default data directories** (common layouts):
The system can detect typical Bitcoin-style data directories:
- Mainnet: `~/.bitcoin/` or `~/Library/Application Support/Bitcoin/`
- Testnet: `~/.bitcoin/testnet3/` or `~/Library/Application Support/Bitcoin/testnet3/`
- Regtest: `~/.bitcoin/regtest/` or `~/Library/Application Support/Bitcoin/regtest/`

**Code**: [bitcoin_core_detection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/bitcoin_core_detection.rs)

### Cache Configuration

```toml
[storage.cache]
block_cache_mb = 100
utxo_cache_mb = 50
header_cache_mb = 10
```

**Cache Sizes**: See [Configuration Reference](../reference/configuration-reference.md) for canonical defaults (e.g. block 100 MB, UTXO 50 MB, header 10 MB).

**Code**: [config](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/)

## Performance Characteristics

### redb Backend

- **When**: Explicit `database_backend = "redb"` or `auto` without RocksDB/TidesDB in the build
- **Read Performance**: Excellent for sequential and random reads
- **Write Performance**: Good for batch writes
- **Production**: A solid **pure-Rust** choice when you are not using RocksDB

### RocksDB Backend

- **When**: Default **`auto`** path in standard `blvm` builds
- **Read/Write**: Tuned for large chain-state workloads; see upstream RocksDB characteristics

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

All backends support pruning:

```toml
[storage.pruning]
mode = { type = "normal", keep_from_height = 0, min_recent_blocks = 288 }
auto_prune = true
auto_prune_interval = 144
```

**Pruning Modes**:
- **Disabled**: Keep all blocks (archival node)
- **Normal**: Conservative pruning (keep recent blocks)
- **Aggressive**: Prune with UTXO commitments (requires utxo-commitments feature)
- **Custom**: Fine-grained control over what to keep

**Code**: [PruningConfig in `config/storage.rs`](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/storage.rs), [runtime pruning logic](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/pruning.rs)

## Error Handling

The storage layer handles backend failures gracefully:

- **Automatic Fallback**: Falls back to alternative backend if primary fails
- **Error Recovery**: Attempts to recover from transient errors
- **Data Integrity**: Verifies data integrity on startup
- **Corruption Detection**: Detects and reports database corruption

**Code**: [storage/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/mod.rs)

## See Also

- [Node Configuration](configuration.md) - Storage configuration options
- [Node Operations](operations.md) - Storage operations and maintenance
- [Pruning](#pruning-support) — pruning configuration on this page; see also [Node configuration](configuration.md)


