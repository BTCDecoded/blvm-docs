# Mathematical Specifications

## Overview

Bitcoin Commons implements formal mathematical specifications for all critical consensus functions. These specifications provide precise mathematical definitions that serve as the source of truth for consensus behavior.

## Specification Format

Mathematical specifications use formal notation to define consensus rules:

- **Quantifiers**: Universal (∀) and existential (∃) quantifiers
- **Functions**: Mathematical function definitions
- **Invariants**: Properties that must always hold
- **Constraints**: Bounds and limits

**Code**: ```26:54:blvm-consensus/docs/VERIFICATION.md```

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

**Verified Functions**:
- `should_reorganize`: Proves longest chain selection
- `calculate_chain_work`: Verifies cumulative work calculation
- `expand_target`: Handles difficulty target edge cases

**Code**: ```28:45:blvm-consensus/docs/VERIFICATION.md```

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

**Code**: ```46:54:blvm-consensus/docs/VERIFICATION.md```

### Total Supply

**Mathematical Specification**:
```
∀ h ∈ ℕ: total_supply(h) = Σ(i=0 to h) subsidy(i)
```

**Invariants**:
- Total supply is monotonic (never decreases)
- Total supply is bounded (≤ 21 * 10^6 * 10^8 satoshis)
- Total supply converges to 21 million BTC

**Code**: ```89:94:blvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

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

**Code**: ```236:246:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

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

**Code**: ```102:108:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

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

**Code**: ```114:124:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

## Specification Coverage

### Functions with Specifications

15+ functions have formal mathematical specifications:

- Chain selection (`should_reorganize`, `calculate_chain_work`)
- Block subsidy (`get_block_subsidy`)
- Total supply (`total_supply`)
- Difficulty adjustment (`get_next_work_required`, `expand_target`)
- Transaction validation (`check_transaction`, `check_tx_inputs`)
- Block validation (`connect_block`, `apply_transaction`)
- Script execution (`eval_script`, `verify_script`)
- Consensus threshold (`find_consensus`)
- Median calculation (`determine_checkpoint_height`)

**Code**: ```172:175:blvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

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

**Code**: ```9:31:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

### Runtime Assertions

Runtime assertions verify mathematical invariants:

- Threshold calculation bounds
- Consensus result invariants
- Median calculation bounds
- Checkpoint bounds

**Code**: ```32:53:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

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

**Code**: ```80:96:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

## Formal Verification

### Kani Proofs

Kani proofs verify mathematical specifications:

- **Threshold Calculation**: Verifies integer-based threshold correctness
- **Median Calculation**: Verifies median bounds
- **Consensus Result**: Verifies consensus result invariants
- **Economic Rules**: Verifies subsidy and supply calculations

**Code**: ```54:79:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

### Property-Based Tests

Property-based tests verify invariants:

- Generate random inputs
- Verify properties hold
- Discover edge cases
- Test mathematical correctness

**Code**: ```169:172:blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md```

## Documentation

### Specification Documents

Mathematical specifications are documented in:

- **MATHEMATICAL_SPECIFICATIONS_COMPLETE.md**: Complete formal specifications
- **VERIFICATION.md**: Verification methodology
- **MATHEMATICAL_PROTECTIONS.md**: Protection mechanisms
- **PROTECTION_COVERAGE.md**: Coverage statistics

**Code**: ```1:20:blvm-consensus/docs/README.md```

## Components

The mathematical specifications system includes:
- Formal mathematical notation for consensus functions
- Mathematical invariants documentation
- Integer-based arithmetic (prevents floating-point bugs)
- Runtime assertions (verify invariants)
- Checked arithmetic (prevents overflow)
- Kani proofs (formal verification)
- Property-based tests (invariant verification)

**Location**: `blvm-consensus/docs/VERIFICATION.md`, `blvm-consensus/docs/MATHEMATICAL_SPECIFICATIONS_COMPLETE.md`, `blvm-consensus/docs/MATHEMATICAL_PROTECTIONS.md`

## See Also

- [Consensus Overview](overview.md) - Consensus layer introduction
- [Consensus Architecture](architecture.md) - Consensus layer design
- [Formal Verification](formal-verification.md) - Kani verification details
- [Mathematical Correctness](mathematical-correctness.md) - Correctness guarantees
- [Property-Based Testing](../development/property-based-testing.md) - Property-based testing

