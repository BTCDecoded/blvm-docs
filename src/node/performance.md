# Performance Optimizations

## Overview

The node implements performance optimizations for initial block download (IBD), parallel validation, and efficient UTXO operations. Actual speedup depends on hardware, network, and workload. For current numbers, see [benchmarks.thebitcoincommons.org](https://benchmarks.thebitcoincommons.org) (when available) or run benchmarks locally ([Benchmarking](../development/benchmarking.md)).

## Parallel Initial Block Download (IBD)

### Overview

Parallel IBD downloads and validates blocks from multiple peers concurrently. The pipeline uses checkpoint-based header download, block pipelining, streaming validation, and batch storage writes.

The node uses parallel IBD for initial sync. **Code**: [parallel_ibd/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)

The parallel IBD system consists of several coordinated optimizations:

1. **Checkpoint Parallel Headers**: Download headers in parallel using hardcoded checkpoints
2. **Block Pipelining**: Download multiple blocks concurrently from each peer
3. **Streaming Validation**: Validate blocks as they arrive using a reorder buffer
4. **Batch Storage**: Use batch writes for efficient UTXO set updates

### Checkpoint Parallel Headers

Headers are downloaded in parallel using hardcoded checkpoints at well-known block heights. This allows multiple header ranges to be downloaded simultaneously from different peers.

**Checkpoints**: Genesis, 11111, 33333, 74000, 105000, 134444, 168000, 193000, 210000 (first halving), 250000, 295000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000


**Algorithm**:
1. Identify checkpoint ranges for the target height range
2. Download headers in parallel for each range
3. Each range uses the checkpoint hash as its starting locator
4. Verification ensures continuity and checkpoint hash matching

### Block Pipelining

Blocks are downloaded with deep pipelining per peer, allowing multiple outstanding block requests to hide network latency.

**Configuration** (see [IBD Configuration](../reference/configuration-reference.md#ibd-configuration) and [Node Configuration](configuration.md#ibd-configuration)):
- `chunk_size`: blocks per chunk (default: **128**; ENV **`BLVM_IBD_CHUNK_SIZE`** 16-2000)
- `max_blocks_in_transit_per_peer`: in-flight blocks per peer (default: **128**; keep ≥ `chunk_size`)
- `download_timeout_secs`: timeout per block in seconds (default: 30)
- `max_concurrent_per_peer`: fixed at 64 in code (not in `[ibd]` config; see `ParallelIBDConfig`)


**Dynamic Work Dispatch**:
- Uses a shared work queue instead of static chunk assignment
- Fast peers automatically grab more work as they finish chunks
- On WAN-only **`parallel`** sync, **multi-peer work-stealing** is default; set **`BLVM_IBD_WAN_SINGLE_PEER=1`** for single-peer download. Peers that exceed max download failures are blacklisted for **300 seconds** before reassignment.
- FIFO ordering ensures lowest heights are processed first

### Streaming Validation with Reorder Buffer

Blocks may arrive out of order from parallel downloads. A reorder buffer ensures blocks are validated in sequential order while allowing downloads to continue.

**Implementation**:
- Reorder buffer (BTreeMap) holds blocks until next expected height; buffer limit is height-dependent (see [memory.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/memory.rs)).
- Streaming validation: validates blocks in order as they become available.
- Backpressure: downloads pause when buffer is full.


### Batch Storage Operations

UTXO set updates use batch writes for efficient bulk operations (single transaction vs many).

**BatchWriter Trait**:
- Accumulates multiple put/delete operations
- Commits all operations atomically in a single transaction
- Ensures database consistency even on crash


**Usage**:
```rust
let mut batch = tree.batch();
for (key, value) in utxo_updates {
 batch.put(key, value);
}
batch.commit()?; // Single atomic commit
```

### Peer Scoring and Filtering

The system tracks peer performance and filters out extremely slow peers during IBD:

- **Latency Tracking**: Monitors average block download latency per peer
- **Slow Peer Filtering**: Drops peers with >90s average latency (keeps at least 2)
- **Dynamic Selection**: Fast peers automatically get more work


### Configuration

```toml
[ibd]
chunk_size = 128
download_timeout_secs = 30
mode = "parallel"
eviction = "fifo"
max_blocks_in_transit_per_peer = 128
headers_timeout_secs = 30
headers_max_failures = 10
```
(`max_concurrent_per_peer` is fixed at 64 in the node; not in `IbdConfig`. See [Node Configuration](configuration.md#ibd-configuration) and [configuration-reference](../reference/configuration-reference.md#ibd-configuration).)


Parallel headers, pipelining, streaming validation, and batch storage all contribute to faster IBD compared to a single-threaded sequential sync. See benchmarks for current measurements.

## IBD UTXO engine (optional)

When **`BLVM_IBD_ENGINE=1`**, validated blocks apply UTXO changes through the age-tiered engine under `storage/ibd_engine/` (checkpoints, crash-safe resume). Download still uses the parallel pipeline above.

See **[IBD UTXO engine](ibd-engine.md)** for enablement, architecture, and checkpoint env vars.

## Parallel Block Validation

### Architecture

Blocks are validated in parallel when they are deep enough from the chain tip. This optimization uses Rayon for parallel execution.


### Safety Conditions

Parallel validation is only used when:
- Blocks are beyond `max_parallel_depth` from tip (default in code: 100 blocks; see `ParallelBlockValidator::default`)
- Each block uses its own UTXO set snapshot (independent validation)
- Blocks are validated sequentially if too close to tip


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


## Batch UTXO Operations

### Batch Fee Calculation

Transaction fees are calculated in batches by pre-fetching all UTXOs before validation:

1. Collect all prevouts from all transactions
2. Batch UTXO lookup (single pass through HashMap)
3. Cache UTXOs for fee calculation
4. Calculate fees using cached UTXOs


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


### Tuning (environment variables)

Batch UTXO lookups and parallel validation batch size are **not** `blvm.toml` keys: `NodeConfig` has no `[performance]` table (unknown tables are ignored). Tune via consensus env vars loaded at node startup:

```bash
export BLVM_BATCH_UTXO_LOOKUPS=1 # default true
export BLVM_PARALLEL_BATCH_SIZE=8 # transactions per parallel batch
```

See [Performance configuration](#performance-configuration) for the full env list.

## Assume-Valid Height

### Overview

Assume-valid height skips expensive signature verification for blocks before a configured height, reducing IBD time. The node merges **`[block_validation]`** into consensus validation config at startup.


### Safety

This optimization is safe because:
1. These blocks are already validated by the network
2. Block structure, Merkle roots, and proof-of-work are still validated
3. Only signature verification is skipped (the expensive operation)

### Configuration

```toml
[block_validation]
assume_valid_height = 912683 # mainnet library default when unset; use 0 for full script checks
# assume_valid_hash = "…" # optional: hash at assume_valid_height (-assumevalid)
```

**Environment variable** (overrides file):

```bash
export BLVM_ASSUME_VALID_HEIGHT=912683
```

Network defaults when neither file nor env is set: mainnet **912 683**, testnet **4 550 000**, regtest **0**. See [configuration-reference](../reference/configuration-reference.md#block_validationassume_valid_height).

Signature verification is a major cost; skipping it for blocks below the threshold speeds IBD. Set **`assume_valid_height = 0`** for maximum script-validation assurance.

## Parallel Transaction Validation

### Architecture

Within a block, transaction validation is parallelized where safe:

1. **Parallel validation** (read-only UTXO access): transaction structure, input validation, fee calculation, script verification.
2. **Sequential application** (write operations): UTXO set updates and state transitions to maintain correctness.


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


## Advanced Indexing

### Address Indexing

Indexes transactions by address for fast lookup:

- **Address Database**: Maps addresses to transaction history
- **Fast Lookup**: O(1) address-to-transaction mapping
- **Incremental Updates**: Updates on each block


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


### Cache-Friendly Memory Layouts

32-byte aligned hash structures for better cache performance:

```rust
#[repr(align(32))]
pub struct CacheAlignedHash([u8; 32]);
```


## Performance configuration

Consensus performance tuning uses **environment variables** (see [blvm-consensus `config.rs`](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs)). There is **no** `[performance]` section in `blvm.toml`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `BLVM_SCRIPT_THREADS` | `0` (auto CPU count) | Script verification thread pool |
| `BLVM_PARALLEL_BATCH_SIZE` | `8` | Transactions per parallel validation batch |
| `BLVM_SIMD` | `true` | SIMD / vectorization when available |
| `BLVM_CACHE_OPTIMIZATIONS` | `true` | Cache-friendly memory layouts |
| `BLVM_BATCH_UTXO_LOOKUPS` | `true` | Pre-fetch UTXOs before batch validation |
| `BLVM_IBD_CHUNK_THRESHOLD` | hardware-derived | Parallelize IBD when sig count exceeds threshold |
| `BLVM_IBD_MIN_CHUNK_SIZE` | hardware-derived | Minimum chunk size for parallel IBD batches |

Assume-valid height is configured in **`blvm.toml`** under **`[block_validation]`** or via **`BLVM_ASSUME_VALID_HEIGHT`** (see above). IBD download tuning uses **`[ibd]`** and **`BLVM_IBD_*`** env vars ([configuration-reference](../reference/configuration-reference.md#ibd-configuration)).


## Benchmark Results

Benchmark results are published at [benchmarks.thebitcoincommons.org](https://benchmarks.thebitcoincommons.org), generated by workflows in the `blvm-bench` repository. Run benchmarks locally for your hardware; see [Benchmarking](../development/benchmarking.md).

## Components

The performance optimization system includes:
- Parallel block validation
- Batch UTXO operations
- Assume-valid height (signature skip below threshold)
- Parallel transaction validation
- Advanced indexing (address, value range)
- Runtime optimizations (constant folding, bounds checks, cache-friendly layouts)
- Performance configuration


## Source

- [parallel_ibd/checkpoints.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/checkpoints.rs)
- [ParallelIBDConfig](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)
- [parallel_ibd](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/) (feeder, validation_loop when `production` feature enabled)
- [BatchWriter](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/database/mod.rs) (trait and backend impls)
- [parallel_ibd](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/) (peer scoring and filtering)
- [parallel_ibd/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)
- [validation/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/validation/mod.rs)
- [block/apply.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/apply.rs)
- [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/config.rs)
- [config/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs) (`BlockValidationNodeConfig`), [block/mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/mod.rs)
- [block/mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/block/mod.rs)
- [txindex.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/storage/txindex.rs), [Transaction Indexing](transaction-indexing.md)
- [optimizations.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/optimizations.rs)
## See Also

- [Operator guide: IBD hub](../getting-started/operator-guide.md#initial-block-download-ibd): Map of all IBD docs
- [Node Overview](overview.md) - Node implementation details
- [Node Configuration](configuration.md) - `[ibd]`, `[block_validation]`, and CLI flags
- [Benchmarking](../development/benchmarking.md) - Performance benchmarking
- [Storage Backends](storage-backends.md) - Storage performance
- [Consensus Overview](../consensus/overview.md#optimization-passes) - Optimization passes
- [UTXO Commitments](utxo-commitments.md) - UTXO proof verification and fast sync
- [IBD UTXO engine](ibd-engine.md): Optional age-tiered UTXO store during sync
- [IBD Bandwidth Protection](ibd-protection.md) - IBD bandwidth management
