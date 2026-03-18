# Performance Optimizations

## Overview

The node implements performance optimizations for initial block download (IBD), parallel validation, and efficient UTXO operations. Actual speedup depends on hardware, network, and workload. For current numbers, see [benchmarks.thebitcoincommons.org](https://benchmarks.thebitcoincommons.org) (when available) or run benchmarks locally ([Benchmarking](../development/benchmarking.md)).

## Parallel Initial Block Download (IBD)

### Overview

Parallel IBD significantly speeds up initial blockchain synchronization by downloading and validating blocks concurrently from multiple peers. The system uses checkpoint-based parallel header download, block pipelining, streaming validation, and efficient batch storage operations.

The node uses parallel IBD for initial sync. **Code**: [parallel_ibd/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)

### Architecture

The parallel IBD system consists of several coordinated optimizations:

1. **Checkpoint Parallel Headers**: Download headers in parallel using hardcoded checkpoints
2. **Block Pipelining**: Download multiple blocks concurrently from each peer
3. **Streaming Validation**: Validate blocks as they arrive using a reorder buffer
4. **Batch Storage**: Use batch writes for efficient UTXO set updates

### Checkpoint Parallel Headers

Headers are downloaded in parallel using hardcoded checkpoints at well-known block heights. This allows multiple header ranges to be downloaded simultaneously from different peers.

**Checkpoints**: Genesis, 11111, 33333, 74000, 105000, 134444, 168000, 193000, 210000 (first halving), 250000, 295000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000

**Code**: [parallel_ibd/checkpoints.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/checkpoints.rs)

**Algorithm**:
1. Identify checkpoint ranges for the target height range
2. Download headers in parallel for each range
3. Each range uses the checkpoint hash as its starting locator
4. Verification ensures continuity and checkpoint hash matching

### Block Pipelining

Blocks are downloaded with deep pipelining per peer, allowing multiple outstanding block requests to hide network latency.

**Configuration** (see [ParallelIBDConfig](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs) and [IBD Configuration](../reference/configuration-reference.md#ibd-configuration)):
- `chunk_size`: blocks per chunk (default: 16; ENV `BLVM_IBD_CHUNK_SIZE` 16–2000)
- `download_timeout_secs`: timeout per block in seconds (default: 30)
- `max_concurrent_per_peer`: fixed at 64 in code (not in `[ibd]` config; see `ParallelIBDConfig`)

**Code**: [ParallelIBDConfig](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)

**Dynamic Work Dispatch**:
- Uses a shared work queue instead of static chunk assignment
- Fast peers automatically grab more work as they finish chunks
- FIFO ordering ensures lowest heights are processed first
- Natural load balancing across peers

### Streaming Validation with Reorder Buffer

Blocks may arrive out of order from parallel downloads. A reorder buffer ensures blocks are validated in sequential order while allowing downloads to continue.

**Implementation**:
- Reorder buffer (BTreeMap) holds blocks until next expected height; buffer limit is height-dependent (see [memory.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/memory.rs)).
- Streaming validation: validates blocks in order as they become available.
- Backpressure: downloads pause when buffer is full.

**Code**: [parallel_ibd](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/) (feeder, validation_loop when `production` feature enabled)

### Batch Storage Operations

UTXO set updates use batch writes for efficient bulk operations (single transaction vs many).

**BatchWriter Trait**:
- Accumulates multiple put/delete operations
- Commits all operations atomically in a single transaction
- Ensures database consistency even on crash

**Code**: [BatchWriter](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs) (trait and backend impls)

**Usage**:
```rust
let mut batch = tree.batch();
for (key, value) in utxo_updates {
    batch.put(key, value);
}
batch.commit()?;  // Single atomic commit
```

### Peer Scoring and Filtering

The system tracks peer performance and filters out extremely slow peers during IBD:

- **Latency Tracking**: Monitors average block download latency per peer
- **Slow Peer Filtering**: Drops peers with >90s average latency (keeps at least 2)
- **Dynamic Selection**: Fast peers automatically get more work

**Code**: [parallel_ibd](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/) (peer scoring and filtering)

### Configuration

```toml
[ibd]
chunk_size = 16
download_timeout_secs = 30
mode = "parallel"
eviction = "fifo"
max_blocks_in_transit_per_peer = 16
headers_timeout_secs = 30
headers_max_failures = 10
```
(`max_concurrent_per_peer` is fixed at 64 in the node; not in `IbdConfig`. See [Node Configuration](configuration.md#ibd-configuration) and [configuration-reference](../reference/configuration-reference.md#ibd-configuration).)

**Code**: [ParallelIBDConfig](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)

Parallel headers, pipelining, streaming validation, and batch storage all contribute to faster IBD compared to a single-threaded sequential sync. See benchmarks for current measurements.

## Parallel Block Validation

### Architecture

Blocks are validated in parallel when they are deep enough from the chain tip. This optimization uses Rayon for parallel execution.

**Code**: [validation/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/validation/mod.rs)

### Safety Conditions

Parallel validation is only used when:
- Blocks are beyond `max_parallel_depth` from tip (default in code: 100 blocks; see `ParallelBlockValidator::default`)
- Each block uses its own UTXO set snapshot (independent validation)
- Blocks are validated sequentially if too close to tip

**Code**: [validation/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/validation/mod.rs)

### Implementation

```rust
pub fn validate_blocks_parallel(
    &self,
    contexts: &[BlockValidationContext],
    depth_from_tip: usize,
    network: Network,
) -> Result<Vec<(ValidationResult, UtxoSet)>> {
    if depth_from_tip <= self.max_parallel_depth {
        return self.validate_blocks_sequential(contexts, network);
    }
    
    // Parallel validation using Rayon
    use rayon::prelude::*;
    contexts.par_iter().map(|context| {
        connect_block(&context.block, ...)
    }).collect()
}
```

**Code**: [validation/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/validation/mod.rs)

## Batch UTXO Operations

### Batch Fee Calculation

Transaction fees are calculated in batches by pre-fetching all UTXOs before validation:

1. Collect all prevouts from all transactions
2. Batch UTXO lookup (single pass through HashMap)
3. Cache UTXOs for fee calculation
4. Calculate fees using cached UTXOs

**Code**: [block/apply.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/apply.rs)

### Implementation

```rust
// Pre-collect all prevouts for batch UTXO lookup
let all_prevouts: Vec<&OutPoint> = block
    .transactions
    .iter()
    .filter(|tx| !is_coinbase(tx))
    .flat_map(|tx| tx.inputs.iter().map(|input| &input.prevout))
    .collect();

// Batch UTXO lookup (single pass)
let mut utxo_cache: HashMap<&OutPoint, &UTXO> =
    HashMap::with_capacity(all_prevouts.len());
for prevout in &all_prevouts {
    if let Some(utxo) = utxo_set.get(prevout) {
        utxo_cache.insert(prevout, utxo);
    }
}
```

**Code**: [block/apply.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/apply.rs)

### Configuration

```toml
[performance]
enable_batch_utxo_lookups = true
parallel_batch_size = 8
```

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs)

## Assume-Valid Checkpoints

### Overview

Assume-valid checkpoints skip expensive signature verification for blocks before a configured height, reducing IBD time when enabled.

**Code**: [block/mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/mod.rs)

### Safety

This optimization is safe because:
1. These blocks are already validated by the network
2. Block structure, Merkle roots, and PoW are still validated
3. Only signature verification is skipped (the expensive operation)

**Code**: [block/mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/mod.rs)

### Configuration

```toml
[performance]
assume_valid_height = 700000  # Skip signatures before this height
```

**Environment Variable**:
```bash
ASSUME_VALID_HEIGHT=700000
```

**Code**: [block/mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/mod.rs)

Signature verification is a major cost; skipping it for pre-checkpoint blocks speeds IBD. Only signature verification is skipped; structure, Merkle, and PoW are still validated. Can be disabled (set to 0) for maximum safety.

## Parallel Transaction Validation

### Architecture

Within a block, transaction validation is parallelized where safe:

1. **Parallel validation** (read-only UTXO access): transaction structure, input validation, fee calculation, script verification.
2. **Sequential application** (write operations): UTXO set updates and state transitions to maintain correctness.

**Code**: [block/mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/mod.rs)

### Implementation

```rust
#[cfg(feature = "rayon")]
{
    use rayon::prelude::*;
    // Parallel validation (read-only)
    let validation_results: Vec<Result<...>> = block
        .transactions
        .par_iter()
        .map(|tx| { check_transaction(tx)?; check_tx_inputs(tx, &utxo_cache, height)?; ... })
        .collect();
    // Sequential application (write operations)
    for (tx, validation) in transactions.zip(validation_results) {
        apply_transaction(tx, &mut utxo_set)?;
    }
}
```

**Code**: [block/mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/mod.rs)

## Advanced Indexing

### Address Indexing

Indexes transactions by address for fast lookup:

- **Address Database**: Maps addresses to transaction history
- **Fast Lookup**: O(1) address-to-transaction mapping
- **Incremental Updates**: Updates on each block

**Code**: [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs), [transaction-indexing.md](transaction-indexing.md)

### Value Range Indexing

Indexes UTXOs by value range for efficient queries:

- **Range Queries**: Find UTXOs in value ranges
- **Optimized Lookups**: Indexed by value range for efficient queries
- **Memory Efficient**: Sparse indexing structure

## Runtime Optimizations

### Constant Folding

Pre-computed constants avoid runtime computation:

```rust
pub mod precomputed_constants {
    pub const U64_MAX: u64 = u64::MAX;
    pub const MAX_MONEY_U64: u64 = MAX_MONEY as u64;
    pub const BTC_PER_SATOSHI: f64 = 1.0 / (SATOSHIS_PER_BTC as f64);
}
```

**Code**: [optimizations.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations.rs)

### Bounds Check Optimization

Optimized bounds checking for proven-safe access patterns:

```rust
pub fn get_proven<T>(slice: &[T], index: usize, bound_check: bool) -> Option<&T> {
    if bound_check {
        slice.get(index)
    } else {
        // Unsafe only when bounds are statically proven
        unsafe { ... }
    }
}
```

**Code**: [optimizations.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations.rs)

### Cache-Friendly Memory Layouts

32-byte aligned hash structures for better cache performance:

```rust
#[repr(align(32))]
pub struct CacheAlignedHash([u8; 32]);
```

**Code**: [optimizations.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations.rs)

## Performance Configuration

### Configuration Options

```toml
[performance]
# Script verification threads (0 = auto-detect)
script_verification_threads = 0

# Parallel batch size
parallel_batch_size = 8

# Enable SIMD optimizations
enable_simd_optimizations = true

# Enable cache optimizations
enable_cache_optimizations = true

# Enable batch UTXO lookups
enable_batch_utxo_lookups = true
```

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs)

### Default Values

- `script_verification_threads`: 0 (auto-detect from CPU count)
- `parallel_batch_size`: 8 transactions per batch
- `enable_simd_optimizations`: true
- `enable_cache_optimizations`: true
- `enable_batch_utxo_lookups`: true

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs)

## Benchmark Results

Benchmark results are published at [benchmarks.thebitcoincommons.org](https://benchmarks.thebitcoincommons.org), generated by workflows in the `blvm-bench` repository. Run benchmarks locally for your hardware; see [Benchmarking](../development/benchmarking.md).

## Components

The performance optimization system includes:
- Parallel block validation
- Batch UTXO operations
- Assume-valid checkpoints
- Parallel transaction validation
- Advanced indexing (address, value range)
- Runtime optimizations (constant folding, bounds checks, cache-friendly layouts)
- Performance configuration

**Location**: `blvm-consensus/src/optimizations.rs`, `blvm-consensus/src/block/`, `blvm-consensus/src/config.rs`, `blvm-node/src/validation/mod.rs`. Storage default for IBD is RocksDB when the `rocksdb` feature is enabled.

## See Also

- [Node Overview](overview.md) - Node implementation details
- [Node Configuration](configuration.md) - Performance configuration options
- [Benchmarking](../development/benchmarking.md) - Performance benchmarking
- [Storage Backends](storage-backends.md) - Storage performance
- [Consensus Architecture](../consensus/architecture.md) - Optimization passes
- [UTXO Commitments](../consensus/utxo-commitments.md) - UTXO proof verification and fast sync
- [IBD Bandwidth Protection](ibd-protection.md) - IBD bandwidth management