# Protocol Constants

<!-- Auto-generated from source code -->
<!-- Regenerate: cd bllvm-docs && python3 tools/extract-constants.py -->

Bitcoin protocol constants extracted from `bllvm-consensus` source code.

## Block Limits

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| `MAX_BLOCK_SERIALIZED_SIZE` | `usize` | 4,000,000 | Maximum block serialized size in bytes (network rule) This is the maximum size of a block when serialized without witness data |
| `MAX_BLOCK_SIGOPS_COST` | `u64` | 80,000 | Maximum block sigop cost (network rule)  Total sigop cost for a block must not exceed this value. Sigop cost = (legacy sigops × 4) + (P2SH sigops × 4) + witness sigops  Reference: Bitcoin Core `consensus.h` MAX_BLOCK_SIGOPS_COST = 80000 |
| `MAX_BLOCK_SIZE` | `usize` | MAX_BLOCK_WEIGHT |  |
| `MAX_BLOCK_WEIGHT` | `usize` | 4,000,000 | Maximum block weight in weight units (network rule, BIP141) Weight = (stripped_size × 4) + witness_size This is the primary limit for SegWit blocks |
| `MAX_SCRIPT_ELEMENT_SIZE` | `usize` | 520 | Maximum script element size (BIP141: witness elements can be up to 520 bytes) |
| `MAX_SCRIPT_SIZE` | `usize` | 10,000 | Maximum script length |
| `MAX_STACK_SIZE` | `usize` | 1,000 | Maximum stack size during script execution |
| `MAX_TX_SIZE` | `usize` | 1,000,000 | Maximum transaction size: 1MB |
| `TARGET_TIME_PER_BLOCK` | `u64` | 600 | Target time per block: 10 minutes |

## Script Limits

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| `MAX_SCRIPT_OPS` | `usize` | 201 | Maximum number of operations in script |
| `TAPROOT_SCRIPT_LENGTH` | `usize` | 34 | Taproot script length (BIP341)  Taproot P2TR script format: OP_1 <32-byte-program> - OP_1 (0x51): 1 byte - Push opcode (0x20): 1 byte - Program hash: 32 bytes Total: 34 bytes |
| `WITNESS_COMMITMENT_SCRIPT_LENGTH` | `usize` | 34 | Witness commitment script length (BIP141)  Total length of witness commitment script: - OP_RETURN (0x6a): 1 byte - Push opcode (0x24): 1 byte - Commitment hash: 32 bytes Total: 34 bytes |

## Monetary Policy

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| `HALVING_INTERVAL` | `u64` | 210,000 | Halving interval: 210,000 blocks |
| `INITIAL_SUBSIDY` | `i64` | 5,000,000,000 | Initial block subsidy: 50 BTC |
| `MAX_MONEY` | `i64` | 2,100,000,000,000,000 | Bitcoin consensus constants from Orange Paper Maximum money supply: 21,000,000 BTC in satoshis |

## Difficulty Adjustment

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| `DIFFICULTY_ADJUSTMENT_INTERVAL` | `u64` | 2,016 | Difficulty adjustment interval: 2016 blocks |
| `LOCKTIME_THRESHOLD` | `u32` | 500,000,000 | Lock time threshold: transactions with lock time < this are block height |
| `MAX_TARGET` | `u32` | 0x1d00ffff | Maximum target (minimum difficulty) |

## Units

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| `SATOSHIS_PER_BTC` | `i64` | 100,000,000 | Satoshis per BTC |

## Other

| Constant | Type | Value | Description |
|----------|------|-------|-------------|
| `COINBASE_MATURITY` | `u64` | 100 | Coinbase maturity requirement: 100 blocks  Coinbase outputs cannot be spent until 100 blocks deep. This prevents miners from spending coinbase immediately and helps secure the network against deep reorgs. |
| `MAX_INPUTS` | `usize` | 1,000 | Maximum number of inputs per transaction |
| `MAX_OUTPUTS` | `usize` | 1,000 | Maximum number of outputs per transaction |
| `MIN_RELAY_FEE` | `i64` | 1,000 | Minimum relay fee for RBF replacement (BIP125)  A replacement transaction must pay at least this much more in fees than the transaction it replaces. This prevents spam replacements with minimal fee increases. |
| `SEGWIT_P2WPKH_LENGTH` | `usize` | 20 | SegWit witness program lengths (BIP141)  SegWit v0 programs: - P2WPKH: 20 bytes - P2WSH: 32 bytes |
| `SEGWIT_P2WSH_LENGTH` | `usize` | 32 |  |
| `SEQUENCE_FINAL` | `u32` | 0xffffffff | Sequence number for final transaction |
| `SEQUENCE_RBF` | `u32` | 0xfffffffe | Sequence number for RBF |
| `TAPROOT_PROGRAM_LENGTH` | `usize` | 32 | Taproot program hash length (BIP341)  Taproot witness program (P2TR) is 32 bytes |
| `WITNESS_COMMITMENT_HASH_LENGTH` | `usize` | 32 | Witness commitment hash length (BIP141)  The witness commitment in the coinbase transaction contains: - OP_RETURN (0x6a): 1 byte - Push opcode (0x24): 1 byte - Commitment hash: 32 bytes Total: 34 bytes  Reference: BIP141 - Witness commitment format |

[Source: bllvm-consensus/src/constants.rs](../../bllvm-consensus/src/constants.rs)
