# Developer Security Checklist

Use this checklist when writing new code or modifying existing code to ensure security best practices.

## Before Writing Code

- [ ] Understand the security implications of your changes
- [ ] Identify affected security controls (check `governance/config/security-control-mapping.yml`)
- [ ] Review relevant security documentation
- [ ] Consider threat model for your changes

## Input Validation

- [ ] Validate all user inputs at boundaries
- [ ] Sanitize inputs before processing
- [ ] Use type-safe APIs (Rust's type system)
- [ ] Reject invalid inputs early
- [ ] Validate data from external sources (network, files, databases)

**Examples:**
```rust
// ✅ Good: Validate input
fn process_amount(amount: u64) -> Result<u64, Error> {
    if amount > MAX_AMOUNT {
        return Err(Error::AmountTooLarge);
    }
    Ok(amount)
}

// ❌ Bad: No validation
fn process_amount(amount: u64) -> u64 {
    amount // Could overflow
}
```

## Authentication & Authorization

- [ ] Implement proper authentication (if applicable)
- [ ] Check authorization before sensitive operations
- [ ] Use principle of least privilege
- [ ] Verify permissions at every boundary
- [ ] Don't trust client-side authorization checks

**Examples:**
```rust
// ✅ Good: Check authorization
fn transfer_funds(from: Account, to: Account, amount: u64) -> Result<(), Error> {
    if !from.has_permission(Permission::Transfer) {
        return Err(Error::Unauthorized);
    }
    // ... transfer logic
}

// ❌ Bad: No authorization check
fn transfer_funds(from: Account, to: Account, amount: u64) {
    // ... transfer logic without checking permissions
}
```

## Cryptographic Operations

- [ ] Use well-tested cryptographic libraries (secp256k1, bitcoin_hashes)
- [ ] Never hardcode keys or secrets
- [ ] Use cryptographically secure random number generation
- [ ] Follow Bitcoin standards (BIP32, BIP39, BIP44)
- [ ] Verify signatures completely
- [ ] Use constant-time operations where needed (avoid timing attacks)

**Examples:**
```rust
// ✅ Good: Use secure random
use rand::rngs::OsRng;
let mut rng = OsRng;
let key = secp256k1::SecretKey::new(&mut rng);

// ❌ Bad: Insecure random
let key = secp256k1::SecretKey::from_slice(&[1, 2, 3, ...])?;
```

## Consensus & Protocol

- [ ] Implement consensus rules exactly as specified
- [ ] Validate all protocol messages
- [ ] Handle network errors gracefully
- [ ] Prevent DoS attacks (rate limiting, resource limits)
- [ ] Don't bypass consensus validation

**Examples:**
```rust
// ✅ Good: Validate consensus rules
fn validate_block(block: &Block) -> Result<(), ConsensusError> {
    if !block.verify_merkle_root() {
        return Err(ConsensusError::InvalidMerkleRoot);
    }
    // ... more validation
}

// ❌ Bad: Skip validation
fn validate_block(block: &Block) -> Result<(), ConsensusError> {
    Ok(()) // No validation!
}
```

## Memory Safety

- [ ] Prefer safe Rust code
- [ ] Document and justify any `unsafe` code
- [ ] Ensure proper resource cleanup (Drop trait)
- [ ] Avoid memory leaks (use RAII patterns)
- [ ] Check bounds before array/vector access

**Examples:**
```rust
// ✅ Good: Safe Rust
let value = vec.get(index).ok_or(Error::OutOfBounds)?;

// ❌ Bad: Unsafe indexing
let value = vec[index]; // Could panic
```

## Error Handling

- [ ] Don't leak sensitive information in errors
- [ ] Use specific error types
- [ ] Handle all error cases
- [ ] Fail securely (default deny)
- [ ] Log errors appropriately (no sensitive data)

**Examples:**
```rust
// ✅ Good: Generic error message
return Err(Error::AuthenticationFailed); // Doesn't reveal why

// ❌ Bad: Leaks information
return Err(Error::InvalidPassword("user123")); // Reveals username
```

## Dependencies

- [ ] Use minimal dependencies
- [ ] Keep dependencies up-to-date
- [ ] Pin consensus-critical dependencies to exact versions
- [ ] Check for known vulnerabilities (cargo audit)
- [ ] Review dependency licenses

**Examples:**
```toml
# ✅ Good: Pin critical dependencies
[dependencies]
secp256k1 = "=0.28.0"  # Exact version for consensus-critical

# ❌ Bad: Allow version ranges for critical code
[dependencies]
secp256k1 = "^0.28"  # Could break consensus
```

## Testing

- [ ] Write security-focused tests
- [ ] Test edge cases and boundary conditions
- [ ] Test error handling paths
- [ ] Include fuzzing for consensus/protocol code
- [ ] Test with malicious inputs
- [ ] Achieve adequate test coverage

**Examples:**
```rust
#[test]
fn test_amount_overflow() {
    assert!(process_amount(u64::MAX).is_err());
}

#[test]
fn test_invalid_signature() {
    let invalid_sig = vec![0u8; 64];
    assert!(verify_signature(&invalid_sig).is_err());
}
```

## Documentation

- [ ] Document security assumptions
- [ ] Document threat model considerations
- [ ] Document security implications of design decisions
- [ ] Update security documentation if adding new controls
- [ ] Document configuration security requirements

## Code Review

- [ ] Request security review for security-sensitive code
- [ ] Address security review feedback
- [ ] Update security control mapping if needed
- [ ] Ensure appropriate governance tier is selected

## Post-Implementation

- [ ] Verify security tests pass
- [ ] Check for new security advisories
- [ ] Update threat model if needed
- [ ] Document any security trade-offs

## Security Control Categories

### Category A: Consensus Integrity
- Genesis block implementation
- SegWit witness verification
- Taproot support
- Script execution limits
- UTXO set validation

### Category B: Cryptographic
- Maintainer key management
- Emergency signature verification
- Multisig threshold enforcement
- Key derivation and storage

### Category C: Governance
- Tier classification logic
- Economic node veto system
- Database query implementation
- Cross-layer file verification

### Category D: Data Integrity
- Audit log hash chain
- OTS timestamping
- State synchronization

### Category E: Input Validation
- GitHub webhook signature verification
- Input sanitization
- SQL injection prevention
- API rate limiting

## Resources

- [Security Controls System](security-controls.md)
- [Threat Models](threat-models.md)
- [Security Review Checklist](https://github.com/BTCDecoded/BTCDecoded/blob/main/.github/SECURITY_REVIEW_CHECKLIST.md) (in main repo)

