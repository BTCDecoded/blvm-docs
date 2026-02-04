# Performance Optimizations

## Overview

Bitcoin Commons implements performance optimizations for faster initial block download (IBD), parallel validation, and efficient UTXO operations. These optimizations provide 10-50x speedups for common operations while maintaining consensus correctness.

## Parallel Initial Block Download (IBD)

### Overview

Parallel IBD significantly speeds up initial blockchain synchronization by downloading and validating blocks concurrently from multiple peers. The system uses checkpoint-based parallel header download, block pipelining, streaming validation, and efficient batch storage operations.

**Code**: [parallel_ibd.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L1-L1819)

### Architecture

The parallel IBD system consists of several coordinated optimizations:

1. **Checkpoint Parallel Headers**: Download headers in parallel using hardcoded checkpoints
2. **Block Pipelining**: Download multiple blocks concurrently from each peer
3. **Streaming Validation**: Validate blocks as they arrive using a reorder buffer
4. **Batch Storage**: Use batch writes for efficient UTXO set updates

### Checkpoint Parallel Headers

Headers are downloaded in parallel using hardcoded checkpoints at well-known block heights. This allows multiple header ranges to be downloaded simultaneously from different peers.

**Checkpoints**: Genesis, 11111, 33333, 74000, 105000, 134444, 168000, 193000, 210000 (first halving), 250000, 295000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000

**Code**: [MAINNET_CHECKPOINTS](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L36-L198)

**Algorithm**:
1. Identify checkpoint ranges for the target height range
2. Download headers in parallel for each range
3. Each range uses the checkpoint hash as its starting locator
4. Verification ensures continuity and checkpoint hash matching

**Performance**: 4-8x faster header download vs sequential

### Block Pipelining

Blocks are downloaded with deep pipelining per peer, allowing multiple outstanding block requests to hide network latency.

**Configuration**:
- `max_concurrent_per_peer`: 64 concurrent downloads per peer (default)
- `chunk_size`: 100 blocks per chunk (default)
- `download_timeout_secs`: 60 seconds per block (default)

**Code**: [ParallelIBDConfig](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L209-L245)

**Dynamic Work Dispatch**:
- Uses a shared work queue instead of static chunk assignment
- Fast peers automatically grab more work as they finish chunks
- FIFO ordering ensures lowest heights are processed first
- Natural load balancing across peers

**Performance**: 4-8x improvement vs sequential block requests

### Streaming Validation with Reorder Buffer

Blocks may arrive out of order from parallel downloads. A reorder buffer ensures blocks are validated in sequential order while allowing downloads to continue.

**Implementation**:
- Bounded channel: 1000 blocks max in flight (~500MB-1GB memory)
- Reorder buffer: BTreeMap maintains blocks until next expected height
- Streaming validation: Validates blocks as they become available in order
- Natural backpressure: Downloads pause when buffer is full

**Code**: [streaming validation](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L536-L745)

**Memory Bounds**: ~500MB-1GB maximum (1000 blocks × ~500KB average)

### Batch Storage Operations

UTXO set updates use batch writes for efficient bulk operations. Batch writes are 10-100x faster than individual inserts.

**BatchWriter Trait**:
- Accumulates multiple put/delete operations
- Commits all operations atomically in a single transaction
- Ensures database consistency even on crash

**Code**: [BatchWriter](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database.rs#L67-L100)

**Performance**:
- Individual `Tree::insert()`: ~1ms per operation (transaction overhead)
- BatchWriter: ~1ms total for thousands of operations (single transaction)

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

**Code**: [peer filtering](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L492-L529)

### Configuration

```toml
[ibd]
# Number of parallel workers (default: CPU count)
num_workers = 8

# Chunk size in blocks (default: 100)
chunk_size = 100

# Maximum concurrent downloads per peer (default: 64)
max_concurrent_per_peer = 64

# Checkpoint interval in blocks (default: 10,000)
checkpoint_interval = 10000

# Timeout for block download in seconds (default: 60)
download_timeout_secs = 60
```

**Code**: [ParallelIBDConfig](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L209-L245)

### Performance Impact

- **Parallel Headers**: 4-8x faster header download
- **Block Pipelining**: 4-8x improvement vs sequential requests
- **Streaming Validation**: Enables concurrent download + validation
- **Batch Storage**: 10-100x faster UTXO updates
- **Overall IBD**: 10-50x faster than sequential IBD

## Parallel Block Validation

### Architecture

Blocks are validated in parallel when they are deep enough from the chain tip. This optimization uses Rayon for parallel execution.

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/validation/mod.rs#L78-L122)

### Safety Conditions

Parallel validation is only used when:
- Blocks are beyond `max_parallel_depth` from tip (default: 6 blocks)
- Each block uses its own UTXO set snapshot (independent validation)
- Blocks are validated sequentially if too close to tip

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/validation/mod.rs#L86-L90)

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

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/validation/mod.rs#L80-L118)

## Batch UTXO Operations

### Batch Fee Calculation

Transaction fees are calculated in batches by pre-fetching all UTXOs before validation:

1. Collect all prevouts from all transactions
2. Batch UTXO lookup (single pass through HashMap)
3. Cache UTXOs for fee calculation
4. Calculate fees using cached UTXOs

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L306-L325)

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

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L308-L324)

### Configuration

```toml
[performance]
enable_batch_utxo_lookups = true
parallel_batch_size = 8
```

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs#L245-L248)

## Assume-Valid Checkpoints

### Overview

Assume-valid checkpoints skip expensive signature verification for blocks before a configured height, providing 10-50x faster IBD.

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L58-L86)

### Safety

This optimization is safe because:
1. These blocks are already validated by the network
2. Block structure, Merkle roots, and PoW are still validated
3. Only signature verification is skipped (the expensive operation)

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L79-L85)

### Configuration

```toml
[performance]
assume_valid_height = 700000  # Skip signatures before this height
```

**Environment Variable**:
```bash
ASSUME_VALID_HEIGHT=700000
```

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L74-L86)

### Performance Impact

- **10-50x faster IBD**: Signature verification is the bottleneck
- **Safe**: Only skips signatures, validates everything else
- **Configurable**: Can be disabled (set to 0) for maximum safety

## Parallel Transaction Validation

### Architecture

Within a block, transaction validation is parallelized where safe:

1. **Phase 1: Parallel Validation** (read-only UTXO access)
   - Transaction structure validation
   - Input validation
   - Fee calculation
   - Script verification (read-only)

2. **Phase 2: Sequential Application** (write operations)
   - UTXO set updates
   - State transitions
   - Maintains correctness

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L326-L400)

### Implementation

```rust
#[cfg(feature = "rayon")]
{
    use rayon::prelude::*;
    // Phase 1: Parallel validation (read-only)
    let validation_results: Vec<Result<...>> = block
        .transactions
        .par_iter()
        .enumerate()
        .map(|(i, tx)| {
            // Validate transaction structure (read-only)
            check_transaction(tx)?;
            // Check inputs and calculate fees (read-only UTXO access)
            check_tx_inputs(tx, &utxo_cache, height)?;
        })
        .collect();
    
    // Phase 2: Sequential application (write operations)
    for (tx, validation) in transactions.zip(validation_results) {
        apply_transaction(tx, &mut utxo_set)?;
    }
}
```

**Code**: [block.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block.rs#L329-L400)

## Advanced Indexing

### Address Indexing

Indexes transactions by address for fast lookup:

- **Address Database**: Maps addresses to transaction history
- **Fast Lookup**: O(1) address-to-transaction mapping
- **Incremental Updates**: Updates on each block

**Code**: [INDEXING_OPTIMIZATIONS.md](https://github.com/BTCDecoded/blvm-node/blob/main/INDEXING_OPTIMIZATIONS.md#L1-L66)

### Value Range Indexing

Indexes UTXOs by value range for efficient queries:

- **Range Queries**: Find UTXOs in value ranges
- **Optimized Lookups**: Faster than scanning all UTXOs
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

**Code**: [optimizations.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations.rs#L15-L37)

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

**Code**: [optimizations.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations.rs#L39-L76)

### Cache-Friendly Memory Layouts

32-byte aligned hash structures for better cache performance:

```rust
#[repr(align(32))]
pub struct CacheAlignedHash([u8; 32]);
```

**Code**: [optimizations.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations.rs#L78-L100)

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

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs#L218-L265)

### Default Values

- `script_verification_threads`: 0 (auto-detect from CPU count)
- `parallel_batch_size`: 8 transactions per batch
- `enable_simd_optimizations`: true
- `enable_cache_optimizations`: true
- `enable_batch_utxo_lookups`: true

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs#L255-L265)

## Benchmark Results

Benchmark results are available at `benchmarks.thebitcoincommons.org`, generated by workflows in `blvm-bench`.

### Performance Improvements

- **Parallel Validation**: 4-8x speedup for deep blocks
- **Batch UTXO Lookups**: 2-3x speedup for fee calculation
- **Assume-Valid Checkpoints**: 10-50x faster IBD
- **Cache-Friendly Layouts**: 10-30% improvement for hash operations

## Components

The performance optimization system includes:
- Parallel block validation
- Batch UTXO operations
- Assume-valid checkpoints
- Parallel transaction validation
- Advanced indexing (address, value range)
- Runtime optimizations (constant folding, bounds checks, cache-friendly layouts)
- Performance configuration

**Location**: `blvm-consensus/src/optimizations.rs`, `blvm-consensus/src/block.rs`, `blvm-consensus/src/config.rs`, `blvm-node/src/validation/mod.rs`

## See Also

- [Node Overview](overview.md) - Node implementation details
- [Node Configuration](configuration.md) - Performance configuration options
- [Benchmarking](../development/benchmarking.md) - Performance benchmarking
- [Storage Backends](storage-backends.md) - Storage performance
- [Consensus Architecture](../consensus/architecture.md) - Optimization passes
- [UTXO Commitments](../consensus/utxo-commitments.md) - UTXO proof verification and fast sync
- [IBD Bandwidth Protection](ibd-protection.md) - IBD bandwidth management
