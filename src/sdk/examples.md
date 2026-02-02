# SDK Examples

The SDK provides examples for common governance operations and module development.

## Complete Governance Workflow

### Step 1: Generate Keypairs

**Using CLI:**
```bash
# Generate a keypair
blvm-keygen --output alice.key --format pem

# Generate multiple keypairs for a team
blvm-keygen --output bob.key --format pem
blvm-keygen --output charlie.key --format pem
```

**Using Rust:**
```rust
use blvm_sdk::governance::GovernanceKeypair;

// Generate a keypair
let keypair = GovernanceKeypair::generate()?;

// Save to file
keypair.save_to_file("alice.key", blvm_sdk::governance::KeyFormat::Pem)?;

// Get public key
let public_key = keypair.public_key();
println!("Public key: {}", public_key);
```

### Step 2: Create a Release Message

**Using CLI:**
```bash
blvm-sign release \
  --version v1.0.0 \
  --commit abc123def456 \
  --key alice.key \
  --output alice-signature.txt
```

**Using Rust:**
```rust
use blvm_sdk::governance::{GovernanceKeypair, GovernanceMessage};

// Load keypair
let keypair = GovernanceKeypair::load_from_file("alice.key")?;

// Create release message
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123def456".to_string(),
};

// Sign the message
let signature = keypair.sign(&message.to_signing_bytes())?;

// Save signature
std::fs::write("alice-signature.txt", signature.to_string())?;
```

### Step 3: Collect Multiple Signatures

```bash
# Each maintainer signs independently
blvm-sign release --version v1.0.0 --commit abc123 --key alice.key --output sig1.txt
blvm-sign release --version v1.0.0 --commit abc123 --key bob.key --output sig2.txt
blvm-sign release --version v1.0.0 --commit abc123 --key charlie.key --output sig3.txt
```

### Step 4: Verify Multisig Threshold

**Using CLI:**
```bash
blvm-verify release \
  --version v1.0.0 \
  --commit abc123 \
  --signatures sig1.txt,sig2.txt,sig3.txt \
  --threshold 3-of-5 \
  --pubkeys maintainers.json
```

**Using Rust:**
```rust
use blvm_sdk::governance::{Multisig, GovernanceMessage, PublicKey};

// Load public keys
let pubkeys = vec![
    PublicKey::from_file("alice.pub")?,
    PublicKey::from_file("bob.pub")?,
    PublicKey::from_file("charlie.pub")?,
    PublicKey::from_file("dave.pub")?,
    PublicKey::from_file("eve.pub")?,
];

// Create multisig (3 of 5 threshold)
let multisig = Multisig::new(3, 5, pubkeys)?;

// Load signatures
let signatures = vec![
    load_signature("sig1.txt")?,
    load_signature("sig2.txt")?,
    load_signature("sig3.txt")?,
];

// Verify
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123".to_string(),
};

let valid = multisig.verify(&message.to_signing_bytes(), &signatures)?;
if valid {
    println!("✓ Multisig verification passed (3/5 signatures)");
} else {
    println!("✗ Multisig verification failed");
}
```

## Nested Multisig Example

For team-based governance with hierarchical structure:

```rust
use blvm_sdk::governance::{Multisig, NestedMultisig};

// Team 1: 2 of 3 members
let team1_keys = vec![alice_key, bob_key, charlie_key];
let team1 = Multisig::new(2, 3, team1_keys)?;

// Team 2: 2 of 3 members
let team2_keys = vec![dave_key, eve_key, frank_key];
let team2 = Multisig::new(2, 3, team2_keys)?;

// Organization: 2 of 2 teams
let nested = NestedMultisig::new(2, 2, vec![team1, team2])?;

// Verify with signatures from both teams
let valid = nested.verify(&message.to_signing_bytes(), &all_signatures)?;
```

## Binary Signing Example

Sign and verify binary files for release verification:

```bash
# Sign a binary
blvm-sign-binary \
  --file target/release/blvm \
  --key maintainer.key \
  --output blvm.sig

# Verify binary signature
blvm-verify-binary \
  --file target/release/blvm \
  --signature blvm.sig \
  --pubkey maintainer.pub
```

For more examples, see the [blvm-sdk examples](../../blvm-sdk/examples/) directory.

## See Also

- [SDK Overview](overview.md) - SDK introduction and architecture
- [SDK Getting Started](getting-started.md) - Quick start guide
- [API Reference](api-reference.md) - Complete SDK API documentation
- [Module Development](module-development.md) - Building modules with the SDK
- [Module System Architecture](../architecture/module-system.md) - Module system design
- [Modules Overview](../modules/overview.md) - Available modules
