# Remaining 2% Incompatibilities with Bitcoin Core

**Date**: 2025-01-XX  
**Status**: Identified and Documented

## Summary

After implementing full SegWit support for `testmempoolaccept`, we've identified the remaining ~2% of incompatibilities with Bitcoin Core's RPC API.

---

## 1. getrawtransaction - hash field for SegWit transactions

### Issue
In `getrawtransaction`, the `hash` field is always set to `txid`, but for SegWit transactions, Core sets `hash` to `wtxid` (witness transaction hash).

**Current Implementation** (`bllvm-node/src/rpc/rawtx.rs:720`):
```rust
"hash": hex::encode(calculated_txid),  // Always txid
```

**Core Behavior**:
- For non-SegWit transactions: `hash == txid`
- For SegWit transactions: `hash == wtxid` (witness hash)

### Impact
- **Severity**: Low-Medium
- **Affects**: SegWit transaction queries via `getrawtransaction`
- **User Impact**: Wallets expecting `hash` to be wtxid for SegWit transactions may have issues

### Fix Required
1. Detect if transaction is SegWit (has witness data)
2. Calculate wtxid for SegWit transactions
3. Set `hash` field to wtxid for SegWit, txid for non-SegWit

### Location
- File: `bllvm-node/src/rpc/rawtx.rs`
- Function: `getrawtransaction` (line ~692)
- Lines: ~718-720

---

## 2. getrawtransaction - vsize and weight calculation for SegWit

### Issue
`vsize` and `weight` are calculated incorrectly for SegWit transactions. Currently using simplified calculation (`size * 4` for weight).

**Current Implementation** (`bllvm-node/src/rpc/rawtx.rs:722-724`):
```rust
"size": serialize_transaction(&tx).len(),
"vsize": serialize_transaction(&tx).len(),  // Wrong for SegWit
"weight": serialize_transaction(&tx).len() * 4,  // Wrong for SegWit
```

**Core Behavior**:
- `weight = 4 * base_size + total_size` (BIP141)
- `vsize = ceil(weight / 4)` (BIP141)
- `base_size` = transaction size without witness data
- `total_size` = transaction size with witness data

### Impact
- **Severity**: Medium
- **Affects**: Fee rate calculations, transaction size estimates
- **User Impact**: Incorrect fee estimates for SegWit transactions

### Fix Required
1. Parse witness data from transaction hex (if available)
2. Calculate `base_size` (without witness)
3. Calculate `total_size` (with witness)
4. Calculate `weight = 4 * base_size + total_size`
5. Calculate `vsize = ceil(weight / 4)`

### Location
- File: `bllvm-node/src/rpc/rawtx.rs`
- Function: `getrawtransaction` (line ~692)
- Lines: ~722-724

---

## 3. getblock - strippedsize calculation

### Issue
`strippedsize` is set to the same value as `size`, but it should exclude witness data for SegWit blocks.

**Current Implementation** (`bllvm-node/src/rpc/blockchain.rs:430`):
```rust
"strippedsize": block_size, // Same as size for now (no witness stripping)
```

**Core Behavior**:
- `strippedsize` = block size excluding witness data (TX_NO_WITNESS)
- `size` = block size including witness data (TX_WITH_WITNESS)
- For non-SegWit blocks: `strippedsize == size`
- For SegWit blocks: `strippedsize < size`

### Impact
- **Severity**: Low
- **Affects**: Block size statistics, historical data analysis
- **User Impact**: Minor - mainly affects analytics tools

### Fix Required
1. Serialize block without witness data (TX_NO_WITNESS format)
2. Calculate `strippedsize` from non-witness serialization
3. Calculate `size` from witness serialization
4. Calculate `weight` properly (BIP141: `4 * base_size + total_size`)

### Location
- File: `bllvm-node/src/rpc/blockchain.rs`
- Function: `get_block` (line ~309)
- Line: ~430

---

## 4. getrawtransaction - Missing witness data in hex output

### Issue
When returning transaction hex in `getrawtransaction`, witness data may not be included if the transaction is SegWit.

**Current Implementation** (`bllvm-node/src/rpc/rawtx.rs:713`):
```rust
let tx_hex = hex::encode(serialize_transaction(&tx));  // May not include witness
```

**Core Behavior**:
- For SegWit transactions, hex should include witness data
- Format: `version + marker(0x00) + flag(0x01) + inputs + outputs + locktime + witness_data`

### Impact
- **Severity**: Medium
- **Affects**: Transaction broadcasting, verification
- **User Impact**: SegWit transactions may fail to broadcast if witness data missing

### Fix Required
1. Check if transaction has witness data in storage
2. Serialize with witness data if SegWit transaction
3. Use proper SegWit serialization format

### Location
- File: `bllvm-node/src/rpc/rawtx.rs`
- Function: `getrawtransaction` (line ~692)
- Line: ~713

---

## 5. Minor Field Differences

### getblockchaininfo.softforks structure
- **Issue**: Structure may not match Core's exact format
- **Severity**: Low
- **Impact**: Minor compatibility issues with some tools

### Field ordering in JSON responses
- **Issue**: Field order may differ from Core
- **Severity**: Very Low
- **Impact**: None (JSON parsers don't care about order)

---

## Priority Ranking

1. **High Priority**:
   - ✅ `testmempoolaccept` SegWit support (COMPLETED)
   - `getrawtransaction` vsize/weight calculation for SegWit
   - `getrawtransaction` witness data in hex output

2. **Medium Priority**:
   - `getrawtransaction` hash field for SegWit (wtxid)
   - `getblock` strippedsize calculation

3. **Low Priority**:
   - `getblockchaininfo.softforks` structure verification
   - Field ordering (cosmetic)

---

## Testing Requirements

For each fix, we should:
1. Add unit tests verifying Core-compatible output
2. Test with real SegWit transactions from mainnet
3. Compare output with Core's RPC output
4. Add to compatibility test suite

---

## Estimated Remaining Work

- ✅ **getrawtransaction fixes**: **COMPLETED**
  - ✅ Hash field now uses wtxid for SegWit transactions
  - ✅ vsize/weight calculation uses proper BIP141 formula
  - ✅ Witness data included in hex output for SegWit transactions
- ✅ **getblock strippedsize**: **COMPLETED**
  - ✅ strippedsize now excludes witness data
  - ✅ Proper weight calculation (4 * base_size + total_size)
- **Testing and verification**: ~1-2 hours
- **Total**: ~1-2 hours remaining to reach 100% compatibility

---

## References

- **Core RPC Documentation**: `/home/acolyte/src/node-comparison/core/src/rpc/`
- **BLLVM RPC Implementation**: `bllvm-node/src/rpc/`
- **Compatibility Analysis**: `CORE_COMPATIBILITY_ANALYSIS.md`
- **Compatibility Summary**: `CORE_COMPATIBILITY_SUMMARY.md`

