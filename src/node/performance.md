# Performance Optimizations

## Overview

Bitcoin Commons implements performance optimizations for faster initial block download (IBD), parallel validation, and efficient UTXO operations. These optimizations provide 10-50x speedups for common operations while maintaining consensus correctness.

## Parallel Block Validation

### Architecture

Blocks are validated in parallel when they are deep enough from the chain tip. This optimization uses Rayon for parallel execution.

**Code**: ```78:122:bllvm-node/src/validation/mod.rs```

### Safety Conditions

Parallel validation is only used when:
- Blocks are beyond `max_parallel_depth` from tip (default: 6 blocks)
- Each block uses its own UTXO set snapshot (independent validation)
- Blocks are validated sequentially if too close to tip

**Code**: ```86:90:bllvm-node/src/validation/mod.rs```

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

**Code**: ```80:118:bllvm-node/src/validation/mod.rs```

## Batch UTXO Operations

### Batch Fee Calculation

Transaction fees are calculated in batches by pre-fetching all UTXOs before validation:

1. Collect all prevouts from all transactions
2. Batch UTXO lookup (single pass through HashMap)
3. Cache UTXOs for fee calculation
4. Calculate fees using cached UTXOs

**Code**: ```306:325:bllvm-consensus/src/block.rs```

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

**Code**: ```308:324:bllvm-consensus/src/block.rs```

### Configuration

```toml
[performance]
enable_batch_utxo_lookups = true
parallel_batch_size = 8
```

**Code**: ```245:248:bllvm-consensus/src/config.rs```

## Assume-Valid Checkpoints

### Overview

Assume-valid checkpoints skip expensive signature verification for blocks before a configured height, providing 10-50x faster IBD.

**Code**: ```58:86:bllvm-consensus/src/block.rs```

### Safety

This optimization is safe because:
1. These blocks are already validated by the network
2. Block structure, Merkle roots, and PoW are still validated
3. Only signature verification is skipped (the expensive operation)

**Code**: ```79:85:bllvm-consensus/src/block.rs```

### Configuration

```toml
[performance]
assume_valid_height = 700000  # Skip signatures before this height
```

**Environment Variable**:
```bash
ASSUME_VALID_HEIGHT=700000
```

**Code**: ```74:86:bllvm-consensus/src/block.rs```

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

**Code**: ```326:400:bllvm-consensus/src/block.rs```

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

**Code**: ```329:400:bllvm-consensus/src/block.rs```

## Advanced Indexing

### Address Indexing

Indexes transactions by address for fast lookup:

- **Address Database**: Maps addresses to transaction history
- **Fast Lookup**: O(1) address-to-transaction mapping
- **Incremental Updates**: Updates on each block

**Code**: ```1:66:bllvm-node/INDEXING_OPTIMIZATIONS.md```

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

**Code**: ```15:37:bllvm-consensus/src/optimizations.rs```

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

**Code**: ```39:76:bllvm-consensus/src/optimizations.rs```

### Cache-Friendly Memory Layouts

32-byte aligned hash structures for better cache performance:

```rust
#[repr(align(32))]
pub struct CacheAlignedHash([u8; 32]);
```

**Code**: ```78:100:bllvm-consensus/src/optimizations.rs```

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

**Code**: ```218:265:bllvm-consensus/src/config.rs```

### Default Values

- `script_verification_threads`: 0 (auto-detect from CPU count)
- `parallel_batch_size`: 8 transactions per batch
- `enable_simd_optimizations`: true
- `enable_cache_optimizations`: true
- `enable_batch_utxo_lookups`: true

**Code**: ```255:265:bllvm-consensus/src/config.rs```

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

**Location**: `bllvm-consensus/src/optimizations.rs`, `bllvm-consensus/src/block.rs`, `bllvm-consensus/src/config.rs`, `bllvm-node/src/validation/mod.rs`

