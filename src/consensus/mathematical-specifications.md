# Mathematical Specifications

**Canonical spec:** The [Orange Paper](../reference/orange-paper.md) on [thebitcoincommons.org](https://thebitcoincommons.org/orange-paper.html) ([Consensus Spec](https://thebitcoincommons.org/spec.html)). **This page** is an in-book digest of formal properties and notation used when reasoning about **blvm-consensus**, checked by tests and **BLVM Specification Lock**, not a substitute for the full commons spec.

## Overview

Bitcoin Commons documents **Orange Paper-aligned** mathematical specifications for consensus behavior. The Rust code implements this spec, checked by tests and **BLVM Specification Lock** on spec-locked functions. Proof scope: [proof limitations](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

## Specification Format

Mathematical specifications use formal notation to define consensus rules:

- **Quantifiers**: Universal (∀) and existential (∃) quantifiers
- **Functions**: Mathematical function definitions
- **Invariants**: Properties that must always hold
- **Constraints**: Bounds and limits


## Core Specifications

### Chain Selection

**Mathematical Specification**:
```
∀ chains C₁, C₂: work(C₁) > work(C₂) ⇒ select(C₁)
```

**Invariants**:
- Selected chain has maximum cumulative work
- Work calculation is deterministic
- Empty chains are rejected
- Chain work is always non-negative

**Key functions:**
- `should_reorganize`: Longest-work selection
- `calculate_chain_work`: Cumulative work calculation
- `expand_target`: Difficulty target edge cases (see also PoW specs)


### Block Subsidy

**Mathematical Specification**:
```
∀ h ∈ ℕ: subsidy(h) = 50 * 10^8 * 2^(-⌊h/210000⌋) if ⌊h/210000⌋ < 64 else 0
```

**Invariants**:
- Subsidy halves every 210,000 blocks
- Subsidy is non-negative
- Subsidy decreases monotonically
- Total supply converges to 21 million BTC


### Total Supply

**Mathematical Specification**:
```
∀ h ∈ ℕ: total_supply(h) = Σ(i=0 to h) subsidy(i)
```

**Invariants**:
- Total supply is monotonic (never decreases)
- Total supply is bounded (≤ 21 * 10^6 * 10^8 satoshis)
- Total supply converges to 21 million BTC


### Difficulty Adjustment

**Mathematical Specification**:
```
target_new = target_old * (timespan / expected_timespan)
timespan_clamped = clamp(timespan, expected/4, expected*4)
```

**Invariants**:
- Target is always positive
- Timespan is clamped to [expected/4, expected*4]
- Difficulty adjustment is deterministic


### Consensus Threshold

**Mathematical Specification**:
```
required_agreement_count = ceil(total_peers * threshold)
consensus_met ⟺ agreement_count >= required_agreement_count
```

**Invariants**:
- `1 <= required_agreement_count <= total_peers`
- `agreement_count >= required` ⟺ `ratio >= threshold`
- Integer comparison is deterministic


### Median Calculation

**Mathematical Specification**:
```
median(tips) = {
 tips[n/2] if n is odd,
 (tips[n/2-1] + tips[n/2]) / 2 if n is even
}
```

**Invariants**:
- `min(tips) <= median <= max(tips)`
- Median is deterministic
- Checkpoint = max(0, median - safety_margin)


### Proof of Work

**Mathematical Specification**:
```
∀ header H: CheckProofOfWork(H) = SHA256(SHA256(H)) < ExpandTarget(H.bits)
```

**Target compression/expansion**:
```
∀ bits ∈ [0x03000000, 0x1d00ffff]:
 Let expanded = expand_target(bits)
 Let compressed = compress_target(expanded)
 Let re_expanded = expand_target(compressed)

 Then:
 - re_expanded ≤ expanded (compression truncates, never increases)
 - re_expanded.0[2] = expanded.0[2] ∧ re_expanded.0[3] = expanded.0[3]
 - Precision loss in words 0, 1 is acceptable (compact format limitation)
```

**Invariants**:
- Hash must be less than target for valid proof of work
- Target expansion handles edge cases correctly
- Target compression preserves significant bits (words 2, 3) exactly
- Difficulty adjustment respects bounds [0.25, 4.0]
- Work calculation is deterministic

**Key functions:**
- `check_proof_of_work`: hash vs target
- `expand_target` / `compress_target`: compact difficulty encoding
- `get_next_work_required`: difficulty adjustment bounds


### Transaction Validation

**Mathematical Specification**:
```
∀ tx ∈ 𝒯𝒳: CheckTransaction(tx) = valid ⟺
 (|tx.inputs| > 0 ∧ |tx.outputs| > 0 ∧
 ∀o ∈ tx.outputs: 0 ≤ o.value ≤ M_max ∧
 |tx.inputs| ≤ M_max_inputs ∧ |tx.outputs| ≤ M_max_outputs ∧
 |tx| ≤ M_max_tx_size)
```

**Invariants**:
- Valid transactions have non-empty inputs and outputs
- Output values are bounded [0, MAX_MONEY]
- Input/output counts and transaction size respect limits
- Coinbase transactions have special validation rules

**Key functions:**
- `check_transaction`: structural validity
- `check_tx_inputs`: input checks including coinbase
- `is_coinbase`: coinbase detection


### Block Connection

**Mathematical Specification**:
```
∀ block B, UTXO set US, height h: ConnectBlock(B, US, h) = (valid, US') ⟺
 (ValidateHeader(B.header) ∧
 ∀ tx ∈ B.transactions: CheckTransaction(tx) ∧ CheckTxInputs(tx, US, h) ∧
 VerifyScripts(tx, US) ∧
 CoinbaseOutput ≤ TotalFees + GetBlockSubsidy(h) ∧
 US' = ApplyTransactions(B.transactions, US))
```

**Invariants**:
- Valid blocks have valid headers and transactions
- UTXO set consistency is preserved
- Coinbase output respects economic rules
- Transaction application is atomic

**Key functions:**
- `connect_block`: full block validation
- `apply_transaction`: UTXO updates
- `calculate_tx_id`: transaction id


## Specification Coverage

### Functions with Specifications

Multiple functions have formal mathematical specifications:

- Chain selection (`should_reorganize`, `calculate_chain_work`)
- Block subsidy (`get_block_subsidy`)
- Total supply (`total_supply`)
- Difficulty adjustment (`get_next_work_required`, `expand_target`)
- Transaction validation (`check_transaction`, `check_tx_inputs`)
- Block validation (`connect_block`, `apply_transaction`)
- Script execution (`eval_script`, `verify_script`)
- Consensus threshold (`find_consensus`)
- Median calculation (`determine_checkpoint_height`)


## Mathematical Protections

### Integer-Based Arithmetic

Floating-point arithmetic replaced with integer-based calculations:

```rust
// Integer-based threshold calculation
let required_agreement_count = ((total_peers as f64) * threshold).ceil() as usize;
if agreement_count >= required_agreement_count {
 // Consensus met
}
```


### Runtime Assertions

Runtime assertions verify mathematical invariants:

- Threshold calculation bounds
- Consensus result invariants
- Median calculation bounds
- Checkpoint bounds


### Checked Arithmetic

Checked arithmetic prevents overflow/underflow:

```rust
// Median calculation with overflow protection
let median_tip = if sorted_tips.len() % 2 == 0 {
 let mid = sorted_tips.len() / 2;
 let lower = sorted_tips[mid - 1];
 let upper = sorted_tips[mid];
 (lower + upper) / 2 // Safe: Natural type prevents overflow
} else {
 sorted_tips[sorted_tips.len() / 2]
};
```


## How verification applies

**BLVM Specification Lock** uses Z3 to prove spec-locked functions against Orange Paper contracts. The symbolic specs on this page are not each a separate Z3 theorem; methodology, CI, and tooling live on [Formal Verification](formal-verification.md). Proof bounds: [proof limitations](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

Property-based tests and runtime assertions (below) complement spec-lock on the same invariants.

## Documentation

Consensus repository references (see [consensus docs index](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/README.md)):

- **[verification policy](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)**: how to run verification and what is in scope
- **[proof limitations](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)**: proof bounds, coverage, and protections beyond formal verification

## Components

The mathematical specifications system includes formal notation, invariants, integer-based arithmetic, runtime assertions, and checked arithmetic on consensus paths. Verification tooling and CI: [Formal Verification](formal-verification.md) and [Testing Infrastructure](../development/testing.md).


## Source

- [verification policy](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)
- [proof limitations](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)
- [repository docs](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/README.md)

## See Also

- [Consensus Overview](overview.md): Consensus layer introduction
- [Formal Verification](formal-verification.md): BLVM Specification Lock methodology
- [Orange Paper](../reference/orange-paper.md): Normative specification on Bitcoin Commons
- [Property-Based Testing](../development/property-based-testing.md): Property-based testing
