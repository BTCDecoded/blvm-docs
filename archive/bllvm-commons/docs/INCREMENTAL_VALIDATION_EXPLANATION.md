# Incremental Validation with Pruning - How It Works

## The Question

**Can we validate the full blockchain if we never have all blocks in storage or memory?**

**Answer: Yes, but validation happens incrementally as blocks arrive, not all at once.**

## How Bitcoin Validation Works

### What Each Block Needs to Validate

When validating a block at height `N`, we need:

1. **The block itself** (being validated)
2. **Previous block header** (for chain linkage via `prev_block_hash`)
3. **Current UTXO set** (for transaction input validation)
4. **Recent headers** (for median time-past, BIP113 - optional)

### What We DON'T Need

- ❌ All previous block bodies
- ❌ All previous transactions
- ❌ Historical UTXO sets
- ❌ Full blockchain history

## Incremental Validation Flow

### During IBD (No Peers - Case B)

```
Block 0 arrives:
  → Validate block 0 (genesis)
  → Update UTXO set: {coinbase_0}
  → Store block 0
  → Generate commitment for block 0
  → Prune? (No, not enough blocks yet)

Block 1 arrives:
  → Get previous header (block 0 header - we keep all headers)
  → Validate block 1:
    - Check PoW (from header)
    - Check prev_block_hash matches block 0 header hash
    - Validate transactions against current UTXO set
  → Update UTXO set: {coinbase_0, coinbase_1, outputs_1}
  → Store block 1
  → Generate commitment for block 1
  → Prune? (No, not enough blocks yet)

Block 2 arrives:
  → Get previous header (block 1 header)
  → Validate block 2:
    - Check PoW
    - Check prev_block_hash matches block 1 header hash
    - Validate transactions against current UTXO set
  → Update UTXO set
  → Store block 2
  → Generate commitment
  → Prune? (Maybe, if window exceeded)

... continues for all blocks ...

Block N arrives:
  → Get previous header (block N-1 header - still have it!)
  → Validate block N:
    - Check PoW
    - Check prev_block_hash matches block N-1 header hash
    - Validate transactions against current UTXO set
  → Update UTXO set
  → Store block N
  → Generate commitment
  → Prune old blocks (beyond window)
```

### Key Points

1. **Headers are always kept**: We keep ALL block headers for:
   - PoW verification
   - Chain linkage verification (`prev_block_hash`)
   - Median time-past calculation

2. **UTXO set is maintained incrementally**: 
   - Starts empty (genesis)
   - Updated as each block is processed
   - Always reflects current state
   - Never needs to be reconstructed from blocks

3. **Each block is validated when it arrives**:
   - We have everything needed: the block, previous header, current UTXO set
   - Validation is complete and correct
   - Once validated, we don't need to re-validate

4. **Pruning happens after validation**:
   - Block is validated first
   - UTXO set is updated
   - Commitment is generated
   - Then old blocks are pruned (beyond window)

## What We Keep vs What We Prune

### Always Kept (Required for Validation)

- ✅ **All block headers** (~80 bytes each, ~40MB total for full chain)
  - Needed for: PoW verification, chain linkage, median time-past
- ✅ **Current UTXO set** (~13GB for full UTXO set)
  - Needed for: Transaction validation
- ✅ **UTXO commitments** (84 bytes each, ~1MB for full chain)
  - Needed for: State verification without full blocks
- ✅ **Recent N blocks** (sliding window, e.g., 144 blocks = ~144MB)
  - Needed for: Recent history, reorganization handling

### Pruned (Not Needed for Ongoing Validation)

- ❌ **Old block bodies** (beyond window)
  - Not needed: Already validated, headers kept for PoW
- ❌ **Old witnesses** (beyond window)
  - Not needed: Already validated, can't re-validate anyway
- ❌ **Old transaction data** (beyond window)
  - Not needed: UTXO set captures current state

## Validation Guarantees

### What We Can Validate

1. **Each block as it arrives**: ✅ Complete validation
   - PoW verification (from header)
   - Chain linkage (from previous header)
   - Transaction validation (from current UTXO set)
   - Script verification (from block + witnesses)

2. **Chain integrity**: ✅ Maintained
   - Headers form valid PoW chain
   - `prev_block_hash` links are verified
   - UTXO set is consistent

3. **State verification**: ✅ Via commitments
   - UTXO commitments verify state at each height
   - Can verify state without full blocks

### What We Can't Do

1. **Re-validate pruned blocks**: ❌ Can't re-validate blocks we've pruned
   - But we don't need to: we validated them when they arrived
   - Headers are kept (PoW verification)
   - Commitments verify state

2. **Replay from genesis**: ❌ Can't replay all blocks from genesis
   - But we don't need to: UTXO set is maintained incrementally
   - Commitments provide state checkpoints

3. **Historical transaction lookup**: ❌ Can't look up old transactions
   - But this is expected with pruning
   - Recent transactions are in the window

## Comparison: Full Node vs Pruned Node

### Full Node (No Pruning)

```
Storage: ~600GB
- All block bodies
- All witnesses
- All transactions
- UTXO set
- Headers

Validation:
- Can validate any block at any time
- Can replay from genesis
- Can look up any transaction
```

### Pruned Node (Incremental Pruning)

```
Storage: ~200MB (with 144 block window)
- All headers (~40MB)
- Current UTXO set (~13GB)
- Recent N blocks (~144MB)
- UTXO commitments (~1MB)

Validation:
- Validates each block as it arrives ✅
- Can't re-validate pruned blocks ❌ (but don't need to)
- Can't replay from genesis ❌ (but don't need to)
- Can verify state via commitments ✅
```

## Why This Works

### Bitcoin's Validation Model

Bitcoin validation is **incremental by design**:

1. **Each block is independent**: A block only needs:
   - Its own data
   - Previous header (for linkage)
   - Current UTXO set (for inputs)

2. **State is maintained, not reconstructed**: 
   - UTXO set is updated incrementally
   - Never needs to be rebuilt from blocks
   - This is why pruning works

3. **Headers provide chain integrity**:
   - PoW in headers proves chain validity
   - `prev_block_hash` links prove chain continuity
   - Don't need block bodies for chain verification

### UTXO Commitments Enable Pruning

Without UTXO commitments:
- Need full blocks to verify state
- Can't prune without losing verification ability

With UTXO commitments:
- Commitments verify state at each height
- Can prune blocks, keep commitments
- State verification without full blocks

## Example: Validating Block 100,000

### With Full Blockchain

```
1. Load block 100,000
2. Get previous header (block 99,999)
3. Get UTXO set (from storage or reconstruct)
4. Validate block
```

### With Incremental Pruning (Block 100,000 Already Validated)

```
1. Block 100,000 was already validated when it arrived
2. Header is kept (for PoW verification)
3. UTXO set was updated when block was processed
4. Commitment was generated and stored
5. Block body was pruned (beyond window)

To verify state at height 100,000:
- Get commitment for block 100,000
- Verify commitment matches expected state
- Don't need block body
```

### If We Need to Re-validate Block 100,000

**We can't** - the block body is pruned. But:

1. **We don't need to**: We validated it when it arrived
2. **Headers prove PoW**: Header is kept, PoW is verified
3. **Commitments prove state**: Commitment verifies UTXO set state
4. **Chain linkage is verified**: `prev_block_hash` in header proves chain continuity

## Conclusion

**Yes, we can validate the full blockchain incrementally without storing it all.**

- ✅ Each block is validated when it arrives
- ✅ Validation is complete and correct
- ✅ Headers provide chain integrity
- ✅ UTXO set is maintained incrementally
- ✅ Commitments verify state
- ❌ Can't re-validate pruned blocks (but don't need to)
- ❌ Can't replay from genesis (but don't need to)

This is exactly how Bitcoin Core's pruning mode works - you validate incrementally, then prune old blocks. The key insight is that **validation is incremental by nature**, so pruning doesn't break validation.

