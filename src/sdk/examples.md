# SDK Examples

The SDK provides examples for common governance operations and module development.

## Governance Examples

### Key Generation

```rust
use bllvm_sdk::governance::GovernanceKeypair;

let keypair = GovernanceKeypair::generate()?;
println!("Public key: {}", keypair.public_key());
```

### Message Signing

```rust
use bllvm_sdk::governance::{GovernanceKeypair, GovernanceMessage};

let keypair = GovernanceKeypair::generate()?;
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123".to_string(),
};

let signature = keypair.sign(&message.to_signing_bytes())?;
```

### Multisig Verification

```rust
use bllvm_sdk::governance::Multisig;

let multisig = Multisig::new(6, 7, maintainer_keys)?;
let valid = multisig.verify(&message.to_signing_bytes(), &signatures)?;
```

For more examples, see the [bllvm-sdk examples](../../modules/bllvm-sdk/examples/) directory.

