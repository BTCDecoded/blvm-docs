# Spam Filtering

## Overview

Spam filtering provides transaction-level filtering for bandwidth optimization and non-monetary transaction detection. The system filters spam transactions to achieve 40-60% bandwidth savings during ongoing sync while maintaining consensus correctness.

**Code**: ```1:680:bllvm-consensus/src/utxo_commitments/spam_filter.rs```

**Note**: While the implementation is located in the `utxo_commitments` module for organizational purposes, spam filtering is a general-purpose feature that can be used independently of UTXO commitments.

## Spam Detection Types

### 1. Ordinals/Inscriptions (`SpamType::Ordinals`)

Detects data embedded in Bitcoin transactions:

- **Witness Scripts**: Detects data embedded in witness scripts (SegWit v0 or Taproot) - **PRIMARY METHOD**
- **OP_RETURN Outputs**: Detects OP_RETURN outputs with large data pushes
- **Envelope Protocol**: Detects envelope protocol patterns (OP_FALSE OP_IF ... OP_ENDIF)
- **Pattern Detection**: Large scripts (>100 bytes) or OP_RETURN with >80 bytes
- **Witness Detection**: Large witness stacks (>1000 bytes) or suspicious data patterns

### 2. Dust Outputs (`SpamType::Dust`)

Filters outputs below threshold:

- **Threshold**: Default 546 satoshis (configurable)
- **Detection**: All outputs must be below threshold for transaction to be considered dust
- **Configuration**: `SpamFilterConfig::dust_threshold`

### 3. BRC-20 Tokens (`SpamType::BRC20`)

Detects BRC-20 token transactions:

- **Pattern Matching**: Detects BRC-20 JSON patterns in OP_RETURN outputs
- **Patterns**: `"p":"brc-20"`, `"op":"mint"`, `"op":"transfer"`, `"op":"deploy"`

### 4. Large Witness Data (`SpamType::LargeWitness`)

Detects transactions with suspiciously large witness data:

- **Threshold**: Default 1000 bytes (configurable)
- **Indication**: Potential data embedding in witness data
- **Configuration**: `SpamFilterConfig::max_witness_size`

### 5. Low Fee Rate (`SpamType::LowFeeRate`)

Detects transactions with suspiciously low fee rates:

- **Detection**: Low fee rate relative to transaction size
- **Indication**: Non-monetary transactions often pay minimal fees
- **Threshold**: Default 1 sat/vbyte (configurable)
- **Configuration**: `SpamFilterConfig::min_fee_rate`
- **Status**: **Disabled by default** (can be too aggressive)

### 6. High Size-to-Value Ratio (`SpamType::HighSizeValueRatio`)

Detects transactions with very large size relative to value transferred:

- **Pattern**: >1000 bytes per satoshi (default threshold)
- **Indication**: Non-monetary use (large data, small value)
- **Configuration**: `SpamFilterConfig::max_size_value_ratio`

### 7. Many Small Outputs (`SpamType::ManySmallOutputs`)

Detects transactions with many small outputs:

- **Pattern**: >10 outputs below dust threshold (default)
- **Indication**: Common in token distributions and Ordinal transfers
- **Configuration**: `SpamFilterConfig::max_small_outputs`

## Critical Design: Output-Only Filtering

**Important**: Spam filtering applies to **OUTPUTS only**, not entire transactions.

When processing a spam transaction:
- ✅ **INPUTS are ALWAYS removed** from UTXO tree (maintains consistency)
- ❌ **OUTPUTS are filtered out** (bandwidth savings)

This ensures UTXO set consistency even when spam transactions spend non-spam inputs.

**Implementation**: ```206:310:bllvm-consensus/src/utxo_commitments/initial_sync.rs```

## Configuration

### Default Configuration

```rust
use bllvm_consensus::utxo_commitments::spam_filter::{SpamFilter, SpamFilterConfig};

// Default configuration (all detection methods enabled except low_fee_rate)
let filter = SpamFilter::new();
```

### Custom Configuration

```rust
let config = SpamFilterConfig {
    filter_ordinals: true,
    filter_dust: true,
    filter_brc20: true,
    filter_large_witness: true,        // Detect large witness stacks
    filter_low_fee_rate: false,         // Disabled by default (too aggressive)
    filter_high_size_value_ratio: true, // Detect high size/value ratio
    filter_many_small_outputs: true,    // Detect many small outputs
    dust_threshold: 546,                // satoshis
    min_output_value: 546,              // satoshis
    min_fee_rate: 1,                    // satoshis per vbyte
    max_witness_size: 1000,             // bytes
    max_size_value_ratio: 1000.0,       // bytes per satoshi
    max_small_outputs: 10,              // count
};

let filter = SpamFilter::with_config(config);
```

## Witness Data Support

For improved detection accuracy, especially for Taproot/SegWit-based Ordinals, use `is_spam_with_witness()`:

```rust
use bllvm_consensus::witness::Witness;

let filter = SpamFilter::new();
let witnesses: Vec<Witness> = /* witness data for each input */;

// Better detection with witness data
let result = filter.is_spam_with_witness(&tx, Some(&witnesses));

// Backward compatible (works without witness data)
let result = filter.is_spam(&tx);
```

## Usage

### Basic Usage

```rust
use bllvm_consensus::utxo_commitments::spam_filter::SpamFilter;

let filter = SpamFilter::new();
let result = filter.is_spam(&transaction);

if result.is_spam {
    println!("Transaction is spam: {:?}", result.spam_type);
    for spam_type in &result.detected_types {
        println!("  - {:?}", spam_type);
    }
}
```

### Block Filtering

```rust
let spam_filter = SpamFilter::new();
let (filtered_txs, spam_summary) = spam_filter.filter_block(&block.transactions);

// Spam summary provides statistics:
// - filtered_count: Number of transactions filtered
// - filtered_size: Total bytes filtered
// - by_type: Breakdown by spam type (ordinals, dust, brc20)
```

### Block Filtering with Witness Data

```rust
let spam_filter = SpamFilter::new();
let witnesses: Vec<Vec<Witness>> = /* witness data for each transaction */;

let (filtered_txs, spam_summary) = spam_filter.filter_block_with_witness(
    &block.transactions,
    Some(&witnesses)
);
```

## Mempool-Level Spam Filtering

In addition to block-level filtering, spam filtering can be applied at the mempool entry point to reject spam transactions before they enter the mempool.

### Configuration

Enable mempool-level spam filtering in `MempoolConfig`:

```rust
use bllvm_consensus::config::MempoolConfig;

let mut config = MempoolConfig::default();
config.reject_spam_in_mempool = true; // Enable spam rejection at mempool entry

// Optional: Customize spam filter configuration
#[cfg(feature = "utxo-commitments")]
{
    use bllvm_consensus::utxo_commitments::config::SpamFilterConfigSerializable;
    config.spam_filter_config = Some(SpamFilterConfigSerializable {
        filter_ordinals: true,
        filter_dust: true,
        filter_brc20: true,
        // ... other spam filter settings
    });
}
```

### Standard Transaction Checks

The mempool also enforces stricter standard transaction checks:

#### OP_RETURN Limits

- **Maximum OP_RETURN size**: 80 bytes (Bitcoin Core standard, configurable)
- **Multiple OP_RETURN rejection**: By default, transactions with more than 1 OP_RETURN output are rejected
- **Configuration**: `MempoolConfig::max_op_return_size`, `max_op_return_outputs`, `reject_multiple_op_return`

#### Envelope Protocol Rejection

- **Envelope protocol detection**: Rejects scripts starting with `OP_FALSE OP_IF` (used by Ordinals)
- **Configuration**: `MempoolConfig::reject_envelope_protocol` (default: true)

#### Script Size Limits

- **Maximum standard script size**: 200 bytes (configurable)
- **Configuration**: `MempoolConfig::max_standard_script_size`

### Per-Peer Transaction Rate Limiting

To prevent peer flooding, transaction rate limiting is enforced per peer:

- **Burst limit**: 10 transactions (configurable)
- **Rate limit**: 1 transaction per second (configurable)
- **Configuration**: `MempoolPolicyConfig::tx_rate_limit_burst`, `tx_rate_limit_per_sec`
- **Location**: `blvm-node/src/network/mod.rs`

Transactions exceeding the rate limit are dropped before processing.

### Example Configuration

```toml
[mempool]
# Enable spam filtering at mempool entry
reject_spam_in_mempool = true

# OP_RETURN limits
max_op_return_size = 80
max_op_return_outputs = 1
reject_multiple_op_return = true

# Standard script checks
max_standard_script_size = 200
reject_envelope_protocol = true

# Fee rate requirements for large transactions
min_fee_rate_large_tx = 2
large_tx_threshold_bytes = 1000

[mempool_policy]
# Per-peer transaction rate limiting
tx_rate_limit_burst = 10
tx_rate_limit_per_sec = 1

# Per-peer byte rate limiting
tx_byte_rate_limit = 100000   # 100 KB/s
tx_byte_rate_burst = 1000000  # 1 MB burst

# Spam-aware eviction
eviction_strategy = "spamfirst"

[spam_ban]
# Spam-specific peer banning
spam_ban_threshold = 10
spam_ban_duration_seconds = 3600  # 1 hour
```

## Integration Points

### UTXO Commitments

Spam filtering is used in UTXO commitment processing to reduce bandwidth during sync:

- **Location**: `bllvm-consensus/src/utxo_commitments/initial_sync.rs`
- **Usage**: Filters outputs when processing blocks for UTXO commitments
- **Benefit**: 40-60% bandwidth reduction during ongoing sync

### Protocol Extensions

Spam filtering is used in protocol extensions for filtered block generation:

- **Location**: `bllvm-node/src/network/protocol_extensions.rs`
- **Usage**: Generates filtered blocks for network peers
- **Benefit**: Reduces bandwidth for filtered block relay

### Mempool Entry

Spam filtering can be applied at mempool entry to reject spam transactions:

- **Location**: `bllvm-consensus/src/mempool.rs::accept_to_memory_pool_with_config()`
- **Usage**: Optional spam check before accepting transactions to mempool
- **Benefit**: Prevents spam from entering mempool, reducing memory usage
- **Status**: Opt-in (default: disabled) to maintain backward compatibility

## Bandwidth Savings

- **40-60% bandwidth reduction** during ongoing sync
- Maintains consensus correctness
- Enables efficient UTXO commitment synchronization
- Reduces storage requirements for filtered block relay

## Performance Characteristics

- **CPU Overhead**: Minimal (pattern matching)
- **Memory**: O(1) per transaction
- **Detection Speed**: Fast (heuristic-based pattern matching)

## Use Cases

1. **UTXO Commitment Sync**: Reduce bandwidth during initial sync
2. **Ongoing Sync**: Skip spam transactions in filtered blocks
3. **Bandwidth Optimization**: For nodes with limited bandwidth
4. **Storage Optimization**: Reduce data that needs to be stored
5. **Network Efficiency**: Reduce bandwidth for filtered block relay
6. **Mempool Management**: Reject spam transactions at mempool entry (opt-in)
7. **Peer Flooding Prevention**: Rate limit transactions per peer to prevent DoS

## Additional Spam Mitigation

### Already Implemented

- **Input/Output Limits**: Consensus-level limits (MAX_INPUTS = 1000, MAX_OUTPUTS = 1000) prevent transactions with excessive inputs/outputs
- **Ancestor/Descendant Limits**: Package limits prevent transaction package spam (default: 25 transactions, 101 kB)
- **DoS Protection**: Automatic peer banning for connection rate violations
- **Per-Peer Byte Rate Limiting**: Limits bytes per second per peer (default: 100 KB/s, 1 MB burst)
- **Fee Rate Requirements for Large Transactions**: Requires higher fees for large transactions (default: 2 sat/vB for transactions >1000 bytes)
- **Spam-Aware Eviction**: Evict spam transactions first when mempool is full (eviction strategy: `SpamFirst`)
- **Spam-Specific Peer Banning**: Auto-ban peers that repeatedly send spam transactions (default: ban after 10 spam transactions, 1 hour duration)

### Per-Peer Byte Rate Limiting

Prevents large transaction flooding by limiting bytes per second per peer:

```toml
[mempool_policy]
tx_byte_rate_limit = 100000  # 100 KB/s
tx_byte_rate_burst = 1000000 # 1 MB burst
```

### Fee Rate Requirements for Large Transactions

Large transactions must pay higher fees to discourage spam:

```toml
[mempool]
min_fee_rate_large_tx = 2      # 2 sat/vB (higher than standard 1 sat/vB)
large_tx_threshold_bytes = 1000 # Transactions >1 KB require higher fees
```

### Spam-Aware Eviction Strategy

When mempool is full, spam transactions are evicted first:

```toml
[mempool_policy]
eviction_strategy = "spamfirst"  # Evict spam transactions first
```

**Note**: Requires `utxo-commitments` feature. Falls back to `lowest_fee_rate` if feature is disabled.

### Spam-Specific Peer Banning

Tracks spam violations per peer and auto-bans repeat offenders:

```toml
[spam_ban]
spam_ban_threshold = 10           # Ban after 10 spam transactions
spam_ban_duration_seconds = 3600  # Ban for 1 hour
```

Peers that repeatedly send spam transactions are automatically banned for the configured duration.

## See Also

- [UTXO Commitments](utxo-commitments.md) - How spam filtering integrates with UTXO commitments
- [Consensus Overview](overview.md) - Consensus layer introduction
- [Network Protocol](../protocol/network-protocol.md) - Network protocol details

