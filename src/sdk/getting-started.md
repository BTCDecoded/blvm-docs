# SDK Getting Started

The developer SDK (`bllvm-sdk`) provides governance infrastructure and cryptographic primitives for Bitcoin governance operations.

## Quick Start

### As a Library

```rust
use bllvm_sdk::governance::{
    GovernanceKeypair, GovernanceMessage, Multisig
};

// Generate a keypair
let keypair = GovernanceKeypair::generate()?;

// Create a message to sign
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123".to_string(),
};

// Sign the message
let signature = keypair.sign(&message.to_signing_bytes())?;

// Verify with multisig
let multisig = Multisig::new(6, 7, maintainer_keys)?;
let valid = multisig.verify(&message.to_signing_bytes(), &[signature])?;
```

### CLI Usage

```bash
# Generate a keypair
bllvm-keygen --output alice.key --format pem

# Sign a release
bllvm-sign release \
  --version v1.0.0 \
  --commit abc123 \
  --key alice.key \
  --output signature.txt

# Verify signatures
bllvm-verify release \
  --version v1.0.0 \
  --commit abc123 \
  --signatures sig1.txt,sig2.txt,sig3.txt,sig4.txt,sig5.txt,sig6.txt \
  --threshold 6-of-7 \
  --pubkeys keys.json
```

For more details, see the [bllvm-sdk README](../../modules/bllvm-sdk/README.md).

## See Also

- [SDK Overview](overview.md) - SDK introduction and architecture
- [API Reference](api-reference.md) - Complete SDK API documentation
- [Module Development](module-development.md) - Building modules with the SDK
- [SDK Examples](examples.md) - More usage examples
- [Governance Overview](../governance/overview.md) - Governance system details

