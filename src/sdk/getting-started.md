# SDK Getting Started

The developer SDK (`blvm-sdk`) provides governance infrastructure and cryptographic primitives for Bitcoin governance operations, plus **module authoring** (process-isolated node modules with CLI, RPC, and events). See [Module Development](module-development.md#sdk-declarative-style-recommended) for the declarative style.

## Quick Start

### As a Library

```rust
use blvm_sdk::governance::{
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
blvm-keygen --output alice.key --format pem

# Sign a release
blvm-sign release \
  --version v1.0.0 \
  --commit abc123 \
  --key alice.key \
  --output signature.txt

# Verify signatures
blvm-verify release \
  --version v1.0.0 \
  --commit abc123 \
  --signatures sig1.txt,sig2.txt,sig3.txt,sig4.txt,sig5.txt,sig6.txt \
  --threshold 6-of-7 \
  --pubkeys keys.json
```

For more details, see the [blvm-sdk README](../../../blvm-sdk/README.md).

### Authoring a node module

1. Add **`blvm-sdk`** with the **`node`** feature and use the [SDK declarative style](module-development.md#sdk-declarative-style-recommended) (`#[module]`, `run_module!`).
2. Ship a binary + **`module.toml`** under the node’s modules directory (see [Module Development](module-development.md)).
3. Optional: register **CLI subcommands** so users invoke your module via **`blvm <your-cli-group> …`** when the module is loaded ([Module CLI under blvm](module-development.md#module-cli-under-the-blvm-binary)).

## See Also

- [SDK Overview](overview.md) - SDK introduction and architecture
- [API Reference](api-reference.md) - Complete SDK API documentation
- [Module Development](module-development.md) - Building modules with the SDK
- [SDK Examples](examples.md) - More usage examples
- [Governance Overview](../governance/overview.md) - Governance system details

