# Developer SDK Overview

The developer SDK (`bllvm-sdk`) provides governance infrastructure and composition framework for Bitcoin. It offers reusable governance primitives and a composition framework for building alternative Bitcoin implementations.

## Architecture Position

Tier 5 of the 6-tier Bitcoin Commons architecture:

```
1. Orange Paper (mathematical foundation)
2. bllvm-consensus (pure math implementation)
3. bllvm-protocol (Bitcoin abstraction)
4. bllvm-node (full node implementation)
5. bllvm-sdk (governance + composition) ← THIS LAYER
6. bllvm-commons (governance enforcement)
```

## Core Components

### Governance Primitives

Cryptographic primitives for governance operations:

- **Key Management**: Generate and manage governance keypairs
- **Signature Creation**: Sign governance messages using Bitcoin-compatible standards
- **Signature Verification**: Verify signatures and multisig thresholds
- **Multisig Logic**: Threshold-based collective decision making
- **Message Formats**: Structured messages for releases, approvals, decisions

**Code**: ```1:200:bllvm-sdk/src/governance/signatures.rs```

### CLI Tools

Command-line tools for governance operations:

- **`bllvm-keygen`**: Generate governance keypairs (PEM, JSON formats)
- **`bllvm-sign`**: Sign governance messages (releases, approvals)
- **`bllvm-verify`**: Verify signatures and multisig thresholds
- **`bllvm-compose`**: Declarative node composition from modules
- **`bllvm-sign-binary`**: Sign binary files for release verification
- **`bllvm-verify-binary`**: Verify binary file signatures
- **`bllvm-aggregate-signatures`**: Aggregate multiple signatures

**Code**: ```1:100:bllvm-sdk/src/bin/bllvm-keygen.rs```

### Composition Framework

Declarative node composition from modules:

- **Module Registry**: Discover and manage available modules
- **Lifecycle Management**: Load, unload, reload modules at runtime
- **Economic Integration**: Merge mining revenue distribution
- **Dependency Resolution**: Automatic module dependency handling

**Code**: ```1:200:bllvm-sdk/src/composition/mod.rs```

## Key Features

### Governance Primitives

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

### Multisig Support

Threshold-based signature verification:

- **N-of-M Thresholds**: Configurable signature requirements (e.g., 6-of-7)
- **Key Management**: Maintainer key registration and rotation
- **Signature Aggregation**: Combine multiple signatures
- **Verification**: Cryptographic verification of threshold satisfaction

**Code**: ```1:200:bllvm-sdk/src/governance/multisig.rs```

### Bitcoin-Compatible Signing

Uses Bitcoin message signing standards:

- **Message Format**: Bitcoin message signing format
- **Signature Algorithm**: secp256k1 ECDSA
- **Hash Function**: Double SHA256
- **Compatibility**: Compatible with Bitcoin Core signing

**Code**: ```1:200:bllvm-sdk/src/governance/signatures.rs```

## Design Principles

1. **Governance Crypto is Reusable**: Clean library API for external consumers
2. **No GitHub Logic**: SDK is pure cryptography + composition, not enforcement
3. **Bitcoin-Compatible**: Uses Bitcoin message signing standards
4. **Test Everything**: Governance crypto needs 100% test coverage
5. **Document for Consumers**: Governance app developers are the customer

## What This Is NOT

- NOT a general-purpose Bitcoin library
- NOT the GitHub enforcement engine (that's bllvm-commons)
- NOT handling wallet keys or user funds
- NOT competing with rust-bitcoin or BDK

## Usage Examples

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

### Library Usage

```rust
use bllvm_sdk::governance::{GovernanceKeypair, GovernanceMessage};

// Generate keypair
let keypair = GovernanceKeypair::generate()?;

// Sign message
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123".to_string(),
};
let signature = keypair.sign(&message.to_signing_bytes())?;
```

## See Also

- [SDK Getting Started](getting-started.md) - Quick start guide
- [API Reference](api-reference.md) - Complete SDK API documentation
- [Module Development](module-development.md) - Building modules
- [SDK Examples](examples.md) - Usage examples
- [Governance Overview](../governance/overview.md) - Governance system

