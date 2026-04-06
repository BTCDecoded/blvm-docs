# Mathematical Specifications

## Overview

Bitcoin Commons documents **Orange Paper–aligned** mathematical specifications for consensus behavior. The Rust code implements this spec, checked by tests and **BLVM Specification Lock** on spec-locked functions. Proof scope: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

## Specification Format

Mathematical specifications use formal notation to define consensus rules:

- **Quantifiers**: Universal (∀) and existential (∃) quantifiers
- **Functions**: Mathematical function definitions
- **Invariants**: Properties that must always hold
- **Constraints**: Bounds and limits

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

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

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

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

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

### Total Supply

**Mathematical Specification**:
```
∀ h ∈ ℕ: total_supply(h) = Σ(i=0 to h) subsidy(i)
```

**Invariants**:
- Total supply is monotonic (never decreases)
- Total supply is bounded (≤ 21 * 10^6 * 10^8 satoshis)
- Total supply converges to 21 million BTC

**Code**: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)

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

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

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

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

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

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

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

**Code**: [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)

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

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

### Runtime Assertions

Runtime assertions verify mathematical invariants:

- Threshold calculation bounds
- Consensus result invariants
- Median calculation bounds
- Checkpoint bounds

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

### Checked Arithmetic

Checked arithmetic prevents overflow/underflow:

```rust
// Median calculation with overflow protection
let median_tip = if sorted_tips.len() % 2 == 0 {
    let mid = sorted_tips.len() / 2;
    let lower = sorted_tips[mid - 1];
    let upper = sorted_tips[mid];
    (lower + upper) / 2  // Safe: Natural type prevents overflow
} else {
    sorted_tips[sorted_tips.len() / 2]
};
```

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

## Formal Verification

### Z3 Proofs

**BLVM Specification Lock** uses Z3 to prove spec-locked functions against Orange Paper contracts. The symbolic specs above are not each a separate Z3 theorem; see [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md).

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

### Property-Based Tests

Property-based tests verify invariants:

- Generate random inputs
- Verify properties hold
- Discover edge cases
- Test mathematical correctness

**Code**: [VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)

## Documentation

### Specification Documents

Mathematical specifications and verification are documented in the consensus repository (see [docs/README.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/README.md)):

- **[VERIFICATION.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md)** — how to run verification and what is in scope
- **[PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)** — proof bounds, coverage, and protections beyond formal verification

**Code**: [README.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/README.md)

## Components

The mathematical specifications system includes:
- Formal mathematical notation for consensus functions
- Mathematical invariants documentation
- Integer-based arithmetic (prevents floating-point bugs)
- Runtime assertions (verify invariants)
- Checked arithmetic (prevents overflow)
- BLVM Specification Lock / Z3 where enabled on annotated functions
- Property-based tests (invariant verification)

**Location**: `blvm-consensus/docs/VERIFICATION.md`, `blvm-consensus/docs/PROOF_LIMITATIONS.md`, `blvm-consensus/docs/README.md` (index)

## See Also

- [Consensus Overview](overview.md) - Consensus layer introduction
- [Consensus Architecture](architecture.md) - Consensus layer design
- [Formal Verification](formal-verification.md) - BLVM Specification Lock verification details
- [Mathematical Correctness](mathematical-correctness.md) - Correctness guarantees
- [Property-Based Testing](../development/property-based-testing.md) - Property-based testing

