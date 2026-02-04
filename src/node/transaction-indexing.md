# Transaction Indexing

## Overview

The node provides advanced transaction indexing capabilities for efficient querying of blockchain data. Indexes are built on-demand and support both address-based and value-based queries.

## Index Types

### Transaction Hash Index

Basic transaction lookup by hash:

- **Key**: Transaction hash (32 bytes)
- **Value**: Transaction metadata (block hash, height, index, size, weight)
- **Lookup**: O(1) hash-based lookup
- **Always Enabled**: Core indexing functionality

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs#L49-L706)

### Address Index (Optional)

Indexes transactions by output addresses:

- **Key**: Address hash (20 bytes for P2PKH, 32 bytes for P2SH/P2WPKH)
- **Value**: List of (transaction hash, output index) pairs
- **Lookup**: Fast address balance and transaction history queries
- **Lazy Indexing**: Built on-demand when first queried
- **Configuration**: Enable with `storage.indexing.enable_address_index = true`

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs#L128-L200)

### Value Range Index (Optional)

Indexes transactions by output value ranges:

- **Key**: Value bucket (logarithmic buckets: 0-1, 1-10, 10-100, 100-1000, etc.)
- **Value**: List of (transaction hash, output index, value) tuples
- **Lookup**: Efficient queries for transactions in specific value ranges
- **Lazy Indexing**: Built on-demand when first queried
- **Configuration**: Enable with `storage.indexing.enable_value_index = true`

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs#L200-L280)

## Indexing Strategy

### Lazy Indexing

Indexes are built on-demand to minimize impact on block processing:

1. **Basic Indexing**: All transactions are indexed with basic metadata (hash, block, height)
2. **On-Demand**: Address and value indexes are built when first queried
3. **Caching**: Indexed addresses are cached to avoid re-indexing
4. **Batch Operations**: Multiple transactions indexed together for efficiency

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs#L109-L126)

### Batch Indexing

Block-level indexing optimizations:

- **Single Pass**: Processes all transactions in a block at once
- **Deduplication**: Uses HashSet for O(1) duplicate checking
- **Batching**: Groups updates per unique address/bucket to reduce DB I/O
- **Conditional Writes**: Only writes to DB if updates were made

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs#L109-L126)

## Configuration

### Enable Indexing

```toml
[storage.indexing]
enable_address_index = true
enable_value_index = true
```

### Index Statistics

Query indexing statistics:

```rust
use blvm_node::storage::txindex::TxIndex;

let stats = txindex.get_stats()?;
println!("Total transactions: {}", stats.total_transactions);
println!("Indexed addresses: {}", stats.indexed_addresses);
println!("Indexed value buckets: {}", stats.indexed_value_buckets);
```

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs#L28-L36)

## Usage

### Query by Address

```rust
use blvm_node::storage::txindex::TxIndex;

// Query all transactions for an address
let address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa";
let transactions = txindex.query_by_address(&address)?;
```

### Query by Value Range

```rust
// Query transactions with outputs in value range [1000, 10000] satoshis
let transactions = txindex.query_by_value_range(1000, 10000)?;
```

### Query Transaction Metadata

```rust
// Get transaction metadata by hash
let tx_hash = Hash::from_hex("...")?;
let metadata = txindex.get_metadata(&tx_hash)?;
```

## Performance Characteristics

- **Hash Lookup**: O(1) constant time
- **Address Lookup**: O(1) after initial indexing, O(n) for first query (indexes on-demand)
- **Value Range Lookup**: O(log n) for bucket lookup, O(m) for results (where m is number of matches)
- **Index Building**: Lazy, only builds what's queried
- **Storage Overhead**: Minimal for basic index, grows with address/value index usage

## See Also

- [Storage Backends](storage-backends.md) - Database backend options
- [Node Configuration](configuration.md) - Indexing configuration options
- [Node Operations](operations.md) - Index maintenance and operations
