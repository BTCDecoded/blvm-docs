# BIP119 CTV (OP_CHECKTEMPLATEVERIFY) - Complete Implementation Plan

**Status**: Planning Phase  
**Priority**: High (Already tracked in codebase, growing community support)

## Executive Summary

This document outlines a comprehensive implementation plan for BIP119 (OP_CHECKTEMPLATEVERIFY), going beyond the original proposal to ensure:
- **Complete mathematical specification** in Orange Paper
- **Formal verification** with Kani proofs
- **Comprehensive testing** (unit, integration, property-based, fuzz)
- **Security analysis** and edge case coverage
- **Performance optimization** considerations
- **Production readiness** with extensive validation

## 1. Specification Review and Analysis

### 1.1 BIP119 Specification Review

**Objective**: Thoroughly understand BIP119 specification and all edge cases.

**Actions**:
1. Study [BIP119 proposal](https://bip119.com/) in detail
2. Review [Bitcoin Optech Newsletter #348](https://bitcoinops.org/en/newsletters/2025/04/04/) for critiques
3. Review reference implementations (if available)
4. Document all edge cases and potential issues
5. Identify areas where we can go beyond the proposal

**Deliverables**:
- Specification analysis document
- Edge case catalog
- Security considerations document

### 1.2 Template Hash Algorithm

**BIP119 Template Hash Specification**:
- Template hash = SHA256(SHA256(template_preimage))
- Template preimage includes:
  - Transaction version (4 bytes, little-endian)
  - Input count (varint)
  - For each input:
    - Previous output hash (32 bytes)
    - Previous output index (4 bytes, little-endian)
    - Sequence (4 bytes, little-endian)
  - Output count (varint)
  - For each output:
    - Value (8 bytes, little-endian)
    - Script length (varint)
    - Script bytes
  - Locktime (4 bytes, little-endian)
  - Input index (4 bytes, little-endian) - **critical: which input is being verified**

**Key Differences from Sighash**:
- No scriptSig in template
- Includes input index
- No sighash type (always uses template format)
- No witness data (SegWit transactions use witness commitment)

**Mathematical Specification** (for Orange Paper):

$$\text{TemplateHash}(tx, input\_index) = \text{SHA256}(\text{SHA256}(\text{TemplatePreimage}(tx, input\_index)))$$

Where:
$$\text{TemplatePreimage}(tx, input\_index) = \text{Version} || \text{Inputs} || \text{Outputs} || \text{Locktime} || input\_index$$

## 2. Implementation Architecture

### 2.1 File Structure

```
bllvm-consensus/src/
├── bip119.rs                    # New: CTV implementation
├── script.rs                    # Modified: Add opcode 0xba
├── transaction_hash.rs          # Modified: Add template hash calculation
└── ...

bllvm-consensus/tests/
├── engineering/
│   └── bip119_integration_tests.rs  # New: Comprehensive integration tests
└── ...

bllvm-spec/
└── THE_ORANGE_PAPER.md          # Modified: Add Section 5.4.6 (BIP119)
```

### 2.2 Core Components

#### 2.2.1 Template Hash Calculation (`transaction_hash.rs`)

```rust
/// Calculate transaction template hash for BIP119 CTV
///
/// Template hash is SHA256(SHA256(template_preimage)) where template_preimage
/// includes version, inputs, outputs, locktime, and input index.
///
/// Mathematical specification: Orange Paper Section 5.4.6
///
/// **TemplateHash**: 𝒯𝒳 × ℕ → ℍ
///
/// For transaction tx and input index i:
/// - TemplateHash(tx, i) = SHA256(SHA256(TemplatePreimage(tx, i)))
pub fn calculate_template_hash(
    tx: &Transaction,
    input_index: usize,
) -> Result<Hash> {
    // Implementation details below
}
```

**Implementation Details**:
1. Serialize transaction version (4 bytes, little-endian)
2. Serialize input count (varint)
3. For each input:
   - Serialize prevout hash (32 bytes)
   - Serialize prevout index (4 bytes, little-endian)
   - Serialize sequence (4 bytes, little-endian)
   - **Note**: scriptSig is NOT included in template
4. Serialize output count (varint)
5. For each output:
   - Serialize value (8 bytes, little-endian)
   - Serialize script length (varint)
   - Serialize script bytes
6. Serialize locktime (4 bytes, little-endian)
7. Serialize input index (4 bytes, little-endian)
8. Double SHA256: SHA256(SHA256(preimage))

**Edge Cases**:
- Empty inputs (should fail - CTV requires at least one input)
- Empty outputs (should fail - CTV requires at least one output)
- Input index out of bounds
- Very large transactions (ensure no overflow)
- Varint encoding edge cases

#### 2.2.2 OP_CHECKTEMPLATEVERIFY Opcode (`script.rs`)

**Opcode**: 0xba

**Stack Behavior**:
- Consumes: [template_hash] (32 bytes)
- Produces: Nothing (fails if template doesn't match)

**Implementation**:

```rust
// OP_CHECKTEMPLATEVERIFY (BIP119) - 0xba
// Verifies that the current transaction matches the template hash
// Stack: [template_hash]
0xba => {
    use crate::transaction_hash::calculate_template_hash;
    
    // Need template hash on stack
    if stack.is_empty() {
        return Ok(false);
    }
    
    let template_hash_bytes = stack.pop().unwrap();
    
    // Template hash must be exactly 32 bytes
    if template_hash_bytes.len() != 32 {
        return Ok(false);
    }
    
    // Convert to Hash type
    let mut template_hash = [0u8; 32];
    template_hash.copy_from_slice(&template_hash_bytes);
    
    // Calculate actual template hash for this transaction and input
    let actual_template_hash = calculate_template_hash(tx, input_index)?;
    
    // Verify template hash matches
    if actual_template_hash != template_hash {
        return Ok(false);
    }
    
    // CTV verification passed
    Ok(true)
}
```

**Integration Points**:
- Must be in `execute_opcode_with_context_full()` (requires transaction context)
- Basic `execute_opcode()` should return false (no context)
- Requires full transaction context (tx, input_index, prevouts)

#### 2.2.3 BIP119 Validation Module (`bip119.rs`)

**Purpose**: Centralized CTV validation logic and utilities.

**Functions**:
1. `calculate_template_hash()` - Template hash calculation
2. `validate_template_hash()` - Template hash validation
3. `extract_template_hash_from_script()` - Extract template hash from scriptPubkey
4. `is_ctv_script()` - Check if script uses CTV

**Constants**:
- `CTV_OPCODE: u8 = 0xba`
- `TEMPLATE_HASH_SIZE: usize = 32`

### 2.3 Integration Points

#### 2.3.1 Script Execution
- Add opcode 0xba to `execute_opcode_with_context_full()`
- Ensure proper error handling
- Add debug assertions

#### 2.3.2 Transaction Validation
- CTV scripts must be in scriptPubkey (not scriptSig)
- Template hash must match transaction structure
- No additional validation needed (CTV is self-contained)

#### 2.3.3 Block Validation
- CTV transactions validated during script execution
- No special block-level checks required

## 3. Mathematical Specification (Orange Paper)

### 3.1 Section 5.4.6: BIP119 CTV Specification

**Location**: `bllvm-spec/THE_ORANGE_PAPER.md` after Section 5.4.5

**Content**:

```markdown
#### 5.4.6 BIP119: OP_CHECKTEMPLATEVERIFY (CTV)

**BIP119Check**: 𝒯𝒳 × ℕ × ℍ → {valid, invalid}

For transaction tx, input index i, and template hash h:

$$\text{BIP119Check}(tx, i, h) = \begin{cases}
\text{valid} & \text{if } \text{TemplateHash}(tx, i) = h \\
\text{invalid} & \text{otherwise}
\end{cases}$$

**Template Hash Calculation**:

$$\text{TemplateHash}(tx, i) = \text{SHA256}(\text{SHA256}(\text{TemplatePreimage}(tx, i)))$$

Where TemplatePreimage is:

$$\text{TemplatePreimage}(tx, i) = \text{Version}(tx) || \text{Inputs}(tx) || \text{Outputs}(tx) || \text{Locktime}(tx) || i$$

**Input Serialization** (for each input):
- Previous output hash (32 bytes)
- Previous output index (4 bytes, little-endian)
- Sequence (4 bytes, little-endian)
- **Note**: scriptSig is NOT included

**Output Serialization** (for each output):
- Value (8 bytes, little-endian)
- Script length (varint)
- Script bytes

**Mathematical Properties**:

**Theorem 5.4.6.1** (CTV Determinism): Template hash is deterministic:
$$\forall tx \in \mathcal{TX}, i \in \mathbb{N} : \text{TemplateHash}(tx, i) \text{ is unique}$$

**Theorem 5.4.6.2** (CTV Uniqueness): Different transactions produce different template hashes:
$$\forall tx_1, tx_2 \in \mathcal{TX}, tx_1 \neq tx_2 : \text{TemplateHash}(tx_1, i) \neq \text{TemplateHash}(tx_2, i)$$

**Theorem 5.4.6.3** (CTV Input-Specific): Template hash depends on input index:
$$\forall tx \in \mathcal{TX}, i_1, i_2 \in \mathbb{N}, i_1 \neq i_2 : \text{TemplateHash}(tx, i_1) \neq \text{TemplateHash}(tx, i_2)$$

**Activation Heights**:
- Mainnet: TBD (BIP9 activation)
- Testnet: TBD
- Regtest: Block 0 (always active for testing)
```

## 4. Formal Verification (Kani Proofs)

### 4.1 Kani Proof Requirements

**Location**: `bllvm-consensus/src/bip119.rs` (in `#[cfg(kani)]` module)

**Proofs to Implement**:

#### 4.1.1 Template Hash Determinism

```rust
/// Kani proof: Template hash is deterministic
///
/// Mathematical specification (Orange Paper Section 5.4.6, Theorem 5.4.6.1):
/// ∀ tx ∈ TX, i ∈ N:
/// - TemplateHash(tx, i) is deterministic (same inputs → same output)
#[kani::proof]
fn kani_template_hash_determinism() {
    let tx: Transaction = kani::any();
    let input_index: usize = kani::any();
    
    // Bound for tractability
    kani::assume(tx.inputs.len() > 0);
    kani::assume(input_index < tx.inputs.len());
    kani::assume(tx.outputs.len() > 0);
    kani::assume(tx.inputs.len() <= 10);
    kani::assume(tx.outputs.len() <= 10);
    
    // Calculate template hash twice
    let hash1 = calculate_template_hash(&tx, input_index);
    let hash2 = calculate_template_hash(&tx, input_index);
    
    // Should be identical
    assert_eq!(hash1, hash2, "Template hash must be deterministic");
}
```

#### 4.1.2 Template Hash Uniqueness

```rust
/// Kani proof: Different transactions produce different template hashes
///
/// Mathematical specification (Orange Paper Section 5.4.6, Theorem 5.4.6.2):
/// ∀ tx1, tx2 ∈ TX, tx1 ≠ tx2:
/// - TemplateHash(tx1, i) ≠ TemplateHash(tx2, i)
#[kani::proof]
fn kani_template_hash_uniqueness() {
    let tx1: Transaction = kani::any();
    let tx2: Transaction = kani::any();
    let input_index: usize = kani::any();
    
    // Bound for tractability
    kani::assume(tx1.inputs.len() > 0);
    kani::assume(tx2.inputs.len() > 0);
    kani::assume(input_index < tx1.inputs.len());
    kani::assume(input_index < tx2.inputs.len());
    kani::assume(tx1.outputs.len() > 0);
    kani::assume(tx2.outputs.len() > 0);
    
    // If transactions are different, hashes should be different
    if tx1 != tx2 {
        let hash1 = calculate_template_hash(&tx1, input_index).unwrap_or([0; 32]);
        let hash2 = calculate_template_hash(&tx2, input_index).unwrap_or([0; 32]);
        
        // Collision probability is negligible (2^-256)
        // This proof verifies the implementation doesn't introduce collisions
        assert!(hash1 != hash2 || tx1 == tx2, 
            "Different transactions must produce different template hashes");
    }
}
```

#### 4.1.3 Input Index Dependency

```rust
/// Kani proof: Template hash depends on input index
///
/// Mathematical specification (Orange Paper Section 5.4.6, Theorem 5.4.6.3):
/// ∀ tx ∈ TX, i1, i2 ∈ N, i1 ≠ i2:
/// - TemplateHash(tx, i1) ≠ TemplateHash(tx, i2)
#[kani::proof]
fn kani_template_hash_input_dependency() {
    let tx: Transaction = kani::any();
    let i1: usize = kani::any();
    let i2: usize = kani::any();
    
    // Bound for tractability
    kani::assume(tx.inputs.len() > 1);
    kani::assume(i1 < tx.inputs.len());
    kani::assume(i2 < tx.inputs.len());
    kani::assume(i1 != i2);
    kani::assume(tx.outputs.len() > 0);
    
    let hash1 = calculate_template_hash(&tx, i1).unwrap_or([0; 32]);
    let hash2 = calculate_template_hash(&tx, i2).unwrap_or([0; 32]);
    
    // Different input indices must produce different hashes
    assert!(hash1 != hash2, "Template hash must depend on input index");
}
```

#### 4.1.4 CTV Opcode Correctness

```rust
/// Kani proof: OP_CHECKTEMPLATEVERIFY correctness
///
/// Mathematical specification (Orange Paper Section 5.4.6):
/// ∀ tx ∈ TX, i ∈ N, h ∈ H:
/// - OP_CHECKTEMPLATEVERIFY(tx, i, h) = true ⟹ TemplateHash(tx, i) = h
#[kani::proof]
fn kani_ctv_opcode_correctness() {
    let tx: Transaction = kani::any();
    let input_index: usize = kani::any();
    let template_hash: [u8; 32] = kani::any();
    
    // Bound for tractability
    kani::assume(tx.inputs.len() > 0);
    kani::assume(input_index < tx.inputs.len());
    kani::assume(tx.outputs.len() > 0);
    
    // Calculate actual template hash
    let actual_hash = calculate_template_hash(&tx, input_index);
    
    if let Ok(actual) = actual_hash {
        // If hashes match, CTV should pass
        if actual == template_hash {
            // Execute CTV opcode
            let mut stack = vec![template_hash.to_vec()];
            let prevouts: Vec<TransactionOutput> = (0..tx.inputs.len())
                .map(|_| TransactionOutput {
                    value: kani::any(),
                    script_pubkey: kani::any(),
                })
                .collect();
            
            let result = execute_opcode_with_context_full(
                0xba, // OP_CHECKTEMPLATEVERIFY
                &mut stack,
                0, // flags
                &tx,
                input_index,
                &prevouts,
                None, // block_height
                None, // median_time_past
            );
            
            assert!(result.is_ok() && result.unwrap(), 
                "CTV should pass when template hash matches");
        }
    }
}
```

#### 4.1.5 Template Hash Bounds

```rust
/// Kani proof: Template hash calculation handles all valid inputs
///
/// Verifies that template hash calculation never panics on valid inputs
#[kani::proof]
fn kani_template_hash_bounds() {
    let tx: Transaction = kani::any();
    let input_index: usize = kani::any();
    
    // Bound for tractability
    kani::assume(tx.inputs.len() > 0);
    kani::assume(input_index < tx.inputs.len());
    kani::assume(tx.outputs.len() > 0);
    kani::assume(tx.inputs.len() <= 100);
    kani::assume(tx.outputs.len() <= 100);
    
    // Should never panic
    let result = calculate_template_hash(&tx, input_index);
    
    // Result should be Ok for valid inputs
    assert!(result.is_ok(), "Template hash calculation should never panic");
    
    // Hash should always be 32 bytes
    if let Ok(hash) = result {
        assert_eq!(hash.len(), 32, "Template hash must be 32 bytes");
    }
}
```

**Total Kani Proofs**: 5 proofs covering:
- Determinism
- Uniqueness
- Input index dependency
- Opcode correctness
- Bounds checking

## 5. Comprehensive Testing

### 5.1 Unit Tests

**Location**: `bllvm-consensus/src/bip119.rs` (in `#[cfg(test)]` module)

**Test Categories**:

#### 5.1.1 Template Hash Calculation Tests

1. **Basic Template Hash**
   - Single input, single output
   - Multiple inputs, multiple outputs
   - Different transaction versions
   - Different locktimes

2. **Edge Cases**
   - Maximum inputs (verify no overflow)
   - Maximum outputs (verify no overflow)
   - Zero-value outputs
   - Large script sizes
   - Varint encoding edge cases

3. **Input Index Tests**
   - First input (index 0)
   - Last input (index n-1)
   - Middle input
   - Verify different indices produce different hashes

4. **Serialization Tests**
   - Verify exact byte-by-byte serialization
   - Compare with reference implementation (if available)
   - Test little-endian encoding
   - Test varint encoding

#### 5.1.2 OP_CHECKTEMPLATEVERIFY Opcode Tests

1. **Valid CTV Scripts**
   - Template hash matches transaction
   - Different input indices
   - Different transaction structures

2. **Invalid CTV Scripts**
   - Template hash doesn't match
   - Wrong hash size (not 32 bytes)
   - Empty stack
   - Missing transaction context

3. **Edge Cases**
   - Template hash matches but transaction structure changed
   - Multiple CTV opcodes in same script
   - CTV combined with other opcodes

### 5.2 Integration Tests

**Location**: `bllvm-consensus/tests/engineering/bip119_integration_tests.rs`

**Test Structure** (following existing BIP test patterns):

```rust
//! BIP119 CTV Integration Tests
//!
//! Comprehensive integration tests for OP_CHECKTEMPLATEVERIFY.
//! Tests CTV in full transaction validation context.

use bllvm_consensus::*;
use bllvm_consensus::bip119::*;
use bllvm_consensus::transaction_hash::calculate_template_hash;

mod template_hash_tests {
    // Template hash calculation tests
}

mod ctv_opcode_tests {
    // OP_CHECKTEMPLATEVERIFY opcode tests
}

mod transaction_validation_tests {
    // Full transaction validation with CTV
}

mod block_validation_tests {
    // Block validation with CTV transactions
}

mod edge_case_tests {
    // Edge cases and error conditions
}

mod use_case_tests {
    // Real-world use cases (vaults, payment channels, etc.)
}
```

**Test Count Target**: 30+ integration tests covering:
- Template hash calculation (10 tests)
- CTV opcode execution (10 tests)
- Transaction validation (5 tests)
- Block validation (3 tests)
- Edge cases (5 tests)
- Use cases (5 tests)

### 5.3 Property-Based Tests

**Tool**: Use `proptest` crate for property-based testing

**Properties to Test**:

1. **Template Hash Properties**
   - Determinism: same inputs → same output
   - Uniqueness: different inputs → different outputs
   - Input index dependency: different indices → different hashes

2. **CTV Validation Properties**
   - Valid template → CTV passes
   - Invalid template → CTV fails
   - Template hash size must be 32 bytes

3. **Transaction Properties**
   - CTV transactions can be included in blocks
   - CTV transactions follow normal validation rules
   - CTV doesn't affect other transaction validation

### 5.4 Fuzz Testing

**Tool**: Use `cargo fuzz` with libFuzzer

**Fuzz Targets**:

1. **Template Hash Calculation**
   - Fuzz transaction structure
   - Fuzz input index
   - Verify no panics, no crashes

2. **CTV Opcode Execution**
   - Fuzz stack contents
   - Fuzz transaction structure
   - Fuzz input index
   - Verify proper error handling

3. **Transaction Validation**
   - Fuzz complete transactions with CTV
   - Verify validation correctness
   - Verify no consensus violations

### 5.5 Bitcoin Core Compatibility Tests

**Objective**: Verify our implementation matches Bitcoin Core behavior (when available)

**Actions**:
1. Create test vectors from Bitcoin Core (if CTV is implemented there)
2. Compare template hash calculations
3. Compare CTV validation results
4. Verify edge case handling matches

### 5.6 Use Case Tests

**Real-World Scenarios**:

1. **Vault Contracts**
   - Time-locked vault with CTV
   - Emergency withdrawal with CTV
   - Multi-signature vault with CTV

2. **Payment Channels**
   - CTV-based payment channels
   - Channel state updates
   - Channel closure

3. **Congestion Control**
   - Transaction batching with CTV
   - Fee optimization with CTV
   - Mempool management with CTV

4. **Smart Contracts**
   - CTV-based covenants
   - State machines with CTV
   - Complex contract logic

## 6. Debug Assertions

### 6.1 Assertions to Add

**Location**: Throughout implementation

**Assertions**:

1. **Template Hash Calculation**
   ```rust
   debug_assert!(input_index < tx.inputs.len(), 
       "Input index must be within bounds");
   debug_assert!(!tx.inputs.is_empty(), 
       "Transaction must have at least one input");
   debug_assert!(!tx.outputs.is_empty(), 
       "Transaction must have at least one output");
   ```

2. **CTV Opcode**
   ```rust
   debug_assert!(template_hash_bytes.len() == 32, 
       "Template hash must be exactly 32 bytes");
   debug_assert!(input_index < tx.inputs.len(), 
       "Input index must be within bounds");
   ```

3. **Transaction Validation**
   ```rust
   debug_assert!(calculate_template_hash(tx, input_index).is_ok(), 
       "Template hash calculation should succeed for valid transaction");
   ```

## 7. Security Analysis

### 7.1 Security Considerations

1. **Template Hash Collisions**
   - Probability: 2^-256 (negligible)
   - Verify implementation doesn't introduce collisions
   - Test with Kani proofs

2. **Input Index Manipulation**
   - Verify input index is correctly included in template
   - Test that different indices produce different hashes
   - Verify input index bounds checking

3. **Transaction Malleability**
   - CTV prevents certain types of malleability
   - Verify template doesn't include malleable fields
   - Test that scriptSig changes don't affect template

4. **DoS Prevention**
   - Verify template hash calculation is efficient
   - Test with very large transactions
   - Verify no quadratic complexity

5. **Script Execution**
   - Verify CTV opcode doesn't leak information
   - Test error handling doesn't reveal internal state
   - Verify stack manipulation is safe

### 7.2 Security Audit Checklist

- [ ] Template hash calculation is correct
- [ ] Input index is properly included
- [ ] No information leakage in error messages
- [ ] No DoS vulnerabilities
- [ ] Proper bounds checking
- [ ] No integer overflows
- [ ] Proper error handling
- [ ] No consensus violations

## 8. Performance Optimization

### 8.1 Optimization Opportunities

1. **Template Hash Caching**
   - Cache template hashes for repeated calculations
   - Useful for mempool validation
   - Cache key: transaction + input index

2. **Batch Template Hash Calculation**
   - Calculate multiple template hashes in parallel
   - Useful for block validation
   - Use Rayon for parallelization

3. **Early Exit Optimizations**
   - Fail fast on invalid template hash size
   - Fail fast on invalid input index
   - Optimize common cases (single input/output)

### 8.2 Performance Benchmarks

**Benchmark Targets**:
- Template hash calculation: < 1μs per transaction
- CTV opcode execution: < 2μs per opcode
- Block validation with CTV: < 10ms per block

**Tools**: Use `criterion` crate for benchmarking

## 9. Documentation

### 9.1 Code Documentation

1. **Function Documentation**
   - Complete doc comments for all public functions
   - Include mathematical specifications
   - Include examples
   - Include error conditions

2. **Module Documentation**
   - Module-level documentation
   - Usage examples
   - Architecture overview

### 9.2 User Documentation

1. **BIP119 Usage Guide**
   - How to create CTV scripts
   - Use case examples
   - Best practices
   - Common pitfalls

2. **API Documentation**
   - Public API reference
   - Function signatures
   - Return types
   - Error types

### 9.3 Developer Documentation

1. **Implementation Details**
   - Design decisions
   - Architecture choices
   - Performance considerations
   - Testing strategy

## 10. Implementation Phases

### Phase 1: Core Implementation (Week 1)

**Deliverables**:
- [ ] Template hash calculation function
- [ ] OP_CHECKTEMPLATEVERIFY opcode implementation
- [ ] Basic unit tests
- [ ] Integration into script execution

**Estimated Time**: 3-4 days

### Phase 2: Mathematical Specification (Week 1-2)

**Deliverables**:
- [ ] Orange Paper Section 5.4.6
- [ ] Mathematical proofs and theorems
- [ ] Specification validation

**Estimated Time**: 2-3 days

### Phase 3: Formal Verification (Week 2)

**Deliverables**:
- [ ] All 5 Kani proofs
- [ ] Proof validation
- [ ] Edge case coverage

**Estimated Time**: 3-4 days

### Phase 4: Comprehensive Testing (Week 2-3)

**Deliverables**:
- [ ] 30+ integration tests
- [ ] Property-based tests
- [ ] Fuzz tests
- [ ] Use case tests
- [ ] Bitcoin Core compatibility tests

**Estimated Time**: 5-7 days

### Phase 5: Security & Performance (Week 3-4)

**Deliverables**:
- [ ] Security analysis
- [ ] Performance benchmarks
- [ ] Optimization implementation
- [ ] Security audit checklist

**Estimated Time**: 3-4 days

### Phase 6: Documentation & Polish (Week 4)

**Deliverables**:
- [ ] Complete code documentation
- [ ] User documentation
- [ ] Developer documentation
- [ ] Final review and polish

**Estimated Time**: 2-3 days

**Total Estimated Time**: 18-25 days (~3.5-5 weeks)

## 11. Success Criteria

### 11.1 Functional Requirements

- [ ] Template hash calculation matches BIP119 specification exactly
- [ ] OP_CHECKTEMPLATEVERIFY opcode works correctly
- [ ] All edge cases handled properly
- [ ] No consensus violations
- [ ] Compatible with existing Bitcoin protocol

### 11.2 Quality Requirements

- [ ] All Kani proofs pass
- [ ] 30+ integration tests pass
- [ ] Property-based tests pass
- [ ] Fuzz tests find no issues
- [ ] Performance benchmarks meet targets
- [ ] Security audit passes

### 11.3 Documentation Requirements

- [ ] Orange Paper specification complete
- [ ] Code documentation complete
- [ ] User documentation complete
- [ ] Developer documentation complete

## 12. Going Beyond the Proposal

### 12.1 Enhanced Features

1. **Extended Template Hash Options**
   - Consider future extensions (if needed)
   - Design for extensibility
   - Document extension points

2. **Enhanced Error Messages**
   - More descriptive error messages
   - Better debugging information
   - Helpful error context

3. **Performance Monitoring**
   - Metrics for template hash calculation
   - Performance profiling hooks
   - Benchmarking infrastructure

4. **Advanced Testing**
   - More comprehensive edge case coverage
   - Additional property-based tests
   - Extended fuzz testing

### 12.2 Research Contributions

1. **Formal Verification**
   - Contribute Kani proofs to community
   - Share verification methodology
   - Document verification process

2. **Security Analysis**
   - Independent security review
   - Vulnerability disclosure process
   - Security best practices

3. **Performance Analysis**
   - Benchmark results
   - Optimization techniques
   - Performance best practices

## 13. Risk Mitigation

### 13.1 Technical Risks

1. **Specification Ambiguity**
   - **Risk**: BIP119 specification may have ambiguities
   - **Mitigation**: Document all assumptions, seek clarification from BIP authors

2. **Implementation Bugs**
   - **Risk**: Bugs in template hash calculation or opcode
   - **Mitigation**: Extensive testing, formal verification, code review

3. **Performance Issues**
   - **Risk**: Template hash calculation may be slow
   - **Mitigation**: Benchmarking, optimization, caching

### 13.2 Process Risks

1. **Timeline Delays**
   - **Risk**: Implementation takes longer than estimated
   - **Mitigation**: Phased approach, prioritize critical features

2. **Testing Gaps**
   - **Risk**: Missing edge cases or use cases
   - **Mitigation**: Comprehensive test plan, community review

## 14. Dependencies

### 14.1 External Dependencies

- `sha2` crate (already in use) - for SHA256
- `kani` (already in use) - for formal verification
- `proptest` (may need to add) - for property-based testing
- `criterion` (may need to add) - for benchmarking

### 14.2 Internal Dependencies

- Transaction serialization (`serialization/transaction.rs`)
- Script execution (`script.rs`)
- Error handling (`error.rs`)
- Types (`types.rs`)

## 15. Post-Implementation

### 15.1 Monitoring

- Monitor CTV usage in production
- Track performance metrics
- Collect error reports
- Gather user feedback

### 15.2 Maintenance

- Keep implementation up-to-date with BIP119 changes
- Address any discovered issues
- Optimize based on usage patterns
- Update documentation as needed

## 16. References

- [BIP119 Specification](https://bip119.com/)
- [Bitcoin Optech Newsletter #348](https://bitcoinops.org/en/newsletters/2025/04/04/)
- [Bitcoin BIPs Repository](https://github.com/bitcoin/bips)
- [Kani Rust Verifier](https://model-checking.github.io/kani/)

---

## Implementation Checklist

### Phase 1: Core Implementation
- [ ] Create `bip119.rs` module
- [ ] Implement `calculate_template_hash()`
- [ ] Implement OP_CHECKTEMPLATEVERIFY opcode (0xba)
- [ ] Add to `execute_opcode_with_context_full()`
- [ ] Basic unit tests
- [ ] Integration into script execution

### Phase 2: Mathematical Specification
- [ ] Add Section 5.4.6 to Orange Paper
- [ ] Define TemplateHash function
- [ ] Define TemplatePreimage function
- [ ] Add theorems and proofs
- [ ] Validate specification

### Phase 3: Formal Verification
- [ ] Kani proof: Template hash determinism
- [ ] Kani proof: Template hash uniqueness
- [ ] Kani proof: Input index dependency
- [ ] Kani proof: CTV opcode correctness
- [ ] Kani proof: Template hash bounds

### Phase 4: Comprehensive Testing
- [ ] 10+ template hash calculation tests
- [ ] 10+ CTV opcode execution tests
- [ ] 5+ transaction validation tests
- [ ] 3+ block validation tests
- [ ] 5+ edge case tests
- [ ] 5+ use case tests
- [ ] Property-based tests
- [ ] Fuzz tests

### Phase 5: Security & Performance
- [ ] Security analysis
- [ ] Performance benchmarks
- [ ] Optimization implementation
- [ ] Security audit

### Phase 6: Documentation
- [ ] Code documentation
- [ ] User documentation
- [ ] Developer documentation
- [ ] Final review

---

**Status**: Ready for implementation  
**Next Step**: Begin Phase 1 - Core Implementation


