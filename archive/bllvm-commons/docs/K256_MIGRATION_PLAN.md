# k256 Pure Rust secp256k1 Migration Plan (Phase 3.2)

## Overview
Migrate from FFI-based `secp256k1` (0.28.2) to pure Rust `k256` crate for signature verification. This removes FFI dependencies, improves audit surface, and maintains performance.

## Current Implementation

**Location**: `bllvm-consensus/src/script.rs`

**Current Usage**:
- `secp256k1::Secp256k1` context (thread-local in production)
- `secp256k1::PublicKey` - parse from bytes
- `secp256k1::ecdsa::Signature` - parse DER format
- `secp256k1::Message` - from digest slice
- Verification: `secp.verify_ecdsa(&message, &signature, &pubkey)`

**Function**: `verify_signature<C: Context + Verification>()`

## k256 API Mapping

### Public Key
- **secp256k1**: `PublicKey::from_slice(pubkey_bytes)`
- **k256**: `k256::PublicKey::from_sec1_bytes(pubkey_bytes)` or `from_encoded_point()`

### Signature
- **secp256k1**: `Signature::from_der(signature_bytes)`
- **k256**: `k256::ecdsa::Signature::from_bytes()` or `from_der()`

### Message/Digest
- **secp256k1**: `Message::from_digest_slice(sighash)`
- **k256**: Use `k256::ecdsa::VerifyingKey::verify()` with raw bytes

### Verification
- **secp256k1**: `secp.verify_ecdsa(&message, &signature, &pubkey)`
- **k256**: `verifying_key.verify(msg, &signature)` where `VerifyingKey` is derived from `PublicKey`

## Migration Strategy

### Phase 1: Add k256 as Optional Dependency
- Add `k256` with `ecdsa` feature
- Keep `secp256k1` for now (backward compatibility)
- Feature flag: `k256` feature to enable new implementation

### Phase 2: Create k256 Adapter
- Create `k256_verify_signature()` function
- Implement same interface as current `verify_signature()`
- Add feature flag to switch between implementations

### Phase 3: Performance Testing
- Benchmark both implementations
- Verify correctness with test vectors
- Ensure no performance regression

### Phase 4: Migration
- Switch default to k256
- Remove secp256k1 dependency
- Update all references

## API Compatibility Notes

**k256 ECDSA API**:
```rust
use k256::{
    ecdsa::{VerifyingKey, Signature, signature::Verifier},
    PublicKey,
};

// Public key
let verifying_key = VerifyingKey::from_public_key_bytes(pubkey_bytes)?;

// Signature (DER format)
let signature = Signature::from_bytes(signature_bytes)?;

// Verification
verifying_key.verify(msg_bytes, &signature)?;
```

**Key Differences**:
1. k256 uses `VerifyingKey` instead of separate `PublicKey` + context
2. Signature parsing might differ (DER vs compact)
3. Message verification takes raw bytes directly

## Testing Requirements

1. **Unit Tests**: All existing signature verification tests
2. **Integration Tests**: Transaction validation with real signatures
3. **Performance Tests**: Ensure no regression
4. **Test Vectors**: Bitcoin Core test vectors for signature verification

## Risks

1. **API Differences**: k256 API may handle edge cases differently
2. **Performance**: Need to verify k256 performance is acceptable
3. **DER Parsing**: Signature format parsing might need adjustment
4. **Compatibility**: Ensure consensus correctness maintained

## Implementation Files

- `bllvm-consensus/Cargo.toml` - Add k256 dependency
- `bllvm-consensus/src/script.rs` - Update `verify_signature()`
- `bllvm-consensus/src/lib.rs` - Add k256 feature flag
- `bllvm-consensus/tests/unit/k256_migration_tests.rs` - Migration tests

## Success Criteria

- [ ] All signature verification tests pass with k256
- [ ] No performance regression (within 5%)
- [ ] Consensus correctness maintained (vs Bitcoin Core)
- [ ] FFI dependency removed
- [ ] Clean migration path documented

