# Developer SDK Overview

The developer SDK (`blvm-sdk`) provides governance infrastructure and a composition framework for Bitcoin. It includes reusable governance primitives and a composition framework for building alternative Bitcoin implementations.

## Architecture Position

**Stack layer 5** of the six-layer Bitcoin Commons architecture (technology stack):

```
1. Orange Paper (mathematical foundation)
2. blvm-consensus (pure math implementation)
3. blvm-protocol (Bitcoin abstraction)
4. blvm-node (full node implementation)
5. blvm-sdk (governance + composition) ← THIS LAYER
6. blvm-commons (governance enforcement)
```

## Core Components

### Module authoring (blvm-sdk + macros)

For **node modules** (process-isolated extensions), blvm-sdk provides:

- **`blvm_sdk::module::prelude`** and **`run_module!` / `run_module_main!`** — bootstrap, DB, IPC main loop without hand-written event plumbing.
- **`blvm-sdk-macros`** — `#[module]`, `#[command]`, `#[rpc_method]`, `#[on_event]`, `#[config]`, `#[migration]`, etc., to declare CLI, RPC, events, and config in one place.

Requires the **`node`** feature on `blvm-sdk`. See [Building modules](module-development.md) (especially [SDK declarative style](module-development.md#sdk-declarative-style-recommended)) and the [hello-module](https://github.com/BTCDecoded/blvm-sdk/tree/main/examples/hello-module) example.

### Governance Primitives

Cryptographic primitives for governance operations:

- **Key Management**: Generate and manage governance keypairs
- **Signature Creation**: Sign governance messages using [Bitcoin-compatible secp256k1 keys](api-reference.md#publickey)
- **Signature Verification**: Verify signatures and [multisig thresholds](../governance/multisig-configuration.md)
- **Multisig Logic**: Threshold-based collective decision making
- **Nested Multisig**: Team-based governance with hierarchical multisig support
- **Message Formats**: Structured messages for releases, approvals, decisions


### CLI Tools

Command-line tools for governance operations:

- **`blvm-keygen`**: Generate governance keypairs (PEM, JSON formats)
- **`blvm-sign`**: Sign governance messages (releases, approvals)
- **`blvm-verify`**: Verify signatures and multisig thresholds
- **`blvm-compose`**: Declarative node composition from modules
- **`blvm-sign-binary`**: Sign binary files for release verification
- **`blvm-verify-binary`**: Verify binary file signatures
- **`blvm-aggregate-signatures`**: Aggregate multiple signatures


### Composition Framework

Declarative node composition from modules:

- **Module Registry**: Discover and manage available modules
- **Lifecycle Management**: Load, unload, reload modules at runtime
- **Dependency Resolution**: Automatic module dependency handling


## Key Features

### Governance Primitives

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
let multisig = Multisig::new([[gov:layer_1_sig_required]], [[gov:layer_1_sig_total]], maintainer_keys)?;
let valid = multisig.verify(&message.to_signing_bytes(), &[signature])?;
```

### Multisig Support

Threshold-based signature verification:

- **N-of-M Thresholds**: Configurable signature requirements (policy thresholds: [Multisig Configuration](../governance/multisig-configuration.md))
- **Key Management**: [Maintainer key registration](../governance/keyholder-procedures.md) and rotation
- **Signature Aggregation**: Combine multiple signatures
- **Verification**: Cryptographic verification of threshold satisfaction


### Bitcoin-Compatible Signing

Uses Bitcoin message signing standards:

- **Message Format**: Bitcoin message signing format
- **Signature Algorithm**: secp256k1 ECDSA
- **Hash Function**: Double SHA256
- **Compatibility**: Works with common PSBT/signing workflows used across the ecosystem


## Design Principles

1. **Governance Crypto is Reusable**: Clean library API for external consumers
2. **No GitHub Logic**: SDK is pure cryptography + composition, not enforcement
3. **Bitcoin-Compatible**: Uses Bitcoin message signing standards
4. **Test coverage**: Treat governance crypto as security-critical—target exhaustive unit and integration tests before release
5. **Document for Consumers**: Governance app developers are the customer

## What This Is NOT

- NOT a general-purpose Bitcoin library
- NOT the GitHub enforcement engine (that's [blvm-commons](../governance/overview.md))
- NOT handling wallet keys or user funds
- NOT competing with rust-bitcoin or BDK

## Usage Examples

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
  --threshold [[gov:layer_1_signatures]] \
  --pubkeys keys.json
```

### Library Usage

```rust
use blvm_sdk::governance::{GovernanceKeypair, GovernanceMessage};

// Generate keypair
let keypair = GovernanceKeypair::generate()?;

// Sign message
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123".to_string(),
};
let signature = keypair.sign(&message.to_signing_bytes())?;
```

## Quick start

### Author a node module

1. Add **`blvm-sdk`** with the **`node`** feature and use the [SDK declarative style](module-development.md#sdk-declarative-style-recommended) (`#[module]`, `run_module!`). For subprocess **ModuleAPI** modules, use **`run_module_with_setup_and_api`** instead of plain **`run_module!`**.
2. Ship a binary + **`module.toml`** under the node’s modules directory (see [Building modules](module-development.md)).
3. Optional: register **CLI subcommands** so users invoke your module via **`blvm <your-cli-group> …`** when loaded ([Module CLI under blvm](module-development.md#module-cli-under-the-blvm-binary)).

For more detail, see the [blvm-sdk README](https://github.com/BTCDecoded/blvm-sdk/blob/main/README.md).

## Source

- [signatures.rs](https://github.com/BTCDecoded/blvm-sdk/blob/main/src/governance/signatures.rs)
- [blvm-keygen.rs](https://github.com/BTCDecoded/blvm-sdk/blob/main/src/bin/blvm-keygen.rs)
- [mod.rs](https://github.com/BTCDecoded/blvm-sdk/blob/main/src/composition/mod.rs)
- [multisig.rs](https://github.com/BTCDecoded/blvm-sdk/blob/main/src/governance/multisig.rs)
## See Also

- [Building modules](module-development.md) - Module development guide
- [API Reference](api-reference.md) - Complete SDK API documentation
- [SDK Examples](examples.md) - Usage examples
- [Governance Overview](../governance/overview.md) - Governance system
