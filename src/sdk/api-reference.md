# SDK API Reference

Complete API documentation for the BLVM Developer SDK, including governance primitives and composition framework.

## Overview

The BLVM SDK provides two main API categories:
- **Governance Primitives**: Cryptographic operations for governance (keys, signatures, multisig)
- **Composition Framework**: Module registry and node composition APIs

For detailed Rust API documentation, see [blvm-sdk on docs.rs](https://docs.rs/blvm-sdk).

## Governance Primitives

### Core Types

#### `GovernanceKeypair`

Cryptographic keypair for signing governance messages.

```rust
pub struct GovernanceKeypair {
    // Private fields
}
```

**Methods:**
- `generate() -> GovernanceResult<Self>` - Generate a new random keypair
- `from_secret_key(secret_bytes: &[u8]) -> GovernanceResult<Self>` - Create from secret key bytes
- `public_key(&self) -> PublicKey` - Get the public key
- `secret_key_bytes(&self) -> [u8; 32]` - Get the secret key bytes (32 bytes)
- `public_key_bytes(&self) -> [u8; 33]` - Get the compressed public key bytes (33 bytes)

**Example:**
```rust
use blvm_sdk::GovernanceKeypair;

let keypair = GovernanceKeypair::generate()?;
let pubkey = keypair.public_key();
```

#### `PublicKey`

Public key for governance operations (Bitcoin-compatible secp256k1).

```rust
pub struct PublicKey {
    // Private fields
}
```

**Methods:**
- `from_bytes(bytes: &[u8]) -> GovernanceResult<Self>` - Create from bytes
- `to_bytes(&self) -> [u8; 33]` - Get compressed public key bytes
- `to_compressed_bytes(&self) -> [u8; 33]` - Get compressed format
- `to_uncompressed_bytes(&self) -> [u8; 65]` - Get uncompressed format

#### `Signature`

Cryptographic signature for governance messages.

```rust
pub struct Signature {
    // Private fields
}
```

**Methods:**
- `from_bytes(bytes: &[u8]) -> GovernanceResult<Self>` - Create from bytes
- `to_bytes(&self) -> [u8; 64]` - Get signature bytes (64 bytes)
- `to_der_bytes(&self) -> Vec<u8>` - Get signature in DER format

#### `GovernanceMessage`

Message types that can be signed for governance decisions.

```rust
pub enum GovernanceMessage {
    Release {
        version: String,
        commit_hash: String,
    },
    ModuleApproval {
        module_name: String,
        version: String,
    },
    BudgetDecision {
        amount: u64,
        purpose: String,
    },
}
```

**Methods:**
- `to_signing_bytes(&self) -> Vec<u8>` - Convert to bytes for signing
- `description(&self) -> String` - Get human-readable description

#### `Multisig`

Multisig configuration for threshold signatures.

```rust
pub struct Multisig {
    // Private fields
}
```

**Methods:**
- `new(threshold: usize, total: usize, public_keys: Vec<PublicKey>) -> GovernanceResult<Self>` - Create new multisig (e.g., 3-of-5)
- `verify(&self, message: &[u8], signatures: &[Signature]) -> GovernanceResult<bool>` - Verify signatures meet threshold
- `collect_valid_signatures(&self, message: &[u8], signatures: &[Signature]) -> GovernanceResult<Vec<usize>>` - Get indices of valid signatures
- `threshold(&self) -> usize` - Get threshold (e.g., 3)
- `total(&self) -> usize` - Get total number of keys (e.g., 5)
- `public_keys(&self) -> &[PublicKey]` - Get all public keys
- `is_valid_signature(&self, signature: &Signature, message: &[u8]) -> GovernanceResult<Option<usize>>` - Check if signature is valid and return key index

**Example:**
```rust
use blvm_sdk::{Multisig, PublicKey};

let multisig = Multisig::new(3, 5, public_keys)?;
let valid = multisig.verify(&message_bytes, &signatures)?;
```

### Functions

#### `sign_message`

Sign a message with a secret key.

```rust
pub fn sign_message(secret_key: &SecretKey, message: &[u8]) -> GovernanceResult<Signature>
```

**Parameters:**
- `secret_key` - The secret key to sign with
- `message` - The message bytes to sign

**Returns:** `GovernanceResult<Signature>` - The signature or an error

#### `verify_signature`

Verify a signature against a message and public key.

```rust
pub fn verify_signature(
    signature: &Signature,
    message: &[u8],
    public_key: &PublicKey,
) -> GovernanceResult<bool>
```

**Parameters:**
- `signature` - The signature to verify
- `message` - The message that was signed
- `public_key` - The public key to verify against

**Returns:** `GovernanceResult<bool>` - `true` if signature is valid

### Error Types

#### `GovernanceError`

Errors that can occur during governance operations.

```rust
pub enum GovernanceError {
    InvalidKey(String),
    SignatureVerification(String),
    InvalidMultisig(String),
    MessageFormat(String),
    Cryptographic(String),
    Serialization(String),
    InvalidThreshold { threshold: usize, total: usize },
    InsufficientSignatures { got: usize, need: usize },
    InvalidSignatureFormat(String),
}
```

#### `GovernanceResult<T>`

Result type alias for governance operations.

```rust
pub type GovernanceResult<T> = Result<T, GovernanceError>;
```

## Composition Framework

### Module Registry

#### `ModuleRegistry`

Manages module discovery, installation, and dependency resolution.

```rust
pub struct ModuleRegistry {
    // Private fields
}
```

**Methods:**
- `new<P: AsRef<Path>>(modules_dir: P) -> Self` - Create registry for modules directory
- `discover_modules(&mut self) -> Result<Vec<ModuleInfo>>` - Discover all modules in directory
- `get_module(&self, name: &str, version: Option<&str>) -> Result<ModuleInfo>` - Get module by name/version
- `install_module(&mut self, source: ModuleSource) -> Result<ModuleInfo>` - Install module from source
- `update_module(&mut self, name: &str, new_version: &str) -> Result<ModuleInfo>` - Update module to new version
- `remove_module(&mut self, name: &str) -> Result<()>` - Remove module
- `list_modules(&self) -> Vec<ModuleInfo>` - List all installed modules
- `resolve_dependencies(&self, module_names: &[String]) -> Result<Vec<ModuleInfo>>` - Resolve module dependencies

**Example:**
```rust
use blvm_sdk::ModuleRegistry;

let mut registry = ModuleRegistry::new("modules");
let modules = registry.discover_modules()?;
let module = registry.get_module("lightning-module", Some("1.0.0"))?;
```

#### `ModuleInfo`

Information about a discovered module.

```rust
pub struct ModuleInfo {
    pub name: String,
    pub version: String,
    pub description: String,
    pub author: String,
    pub capabilities: Vec<String>,
    pub dependencies: HashMap<String, String>,
    pub entry_point: String,
    pub source: ModuleSource,
    pub status: ModuleStatus,
    pub health: ModuleHealth,
}
```

### Node Composition

#### `NodeComposer`

Composes nodes from module specifications.

```rust
pub struct NodeComposer {
    // Private fields
}
```

**Methods:**
- `new<P: AsRef<Path>>(modules_dir: P) -> Self` - Create composer with module registry
- `validate_composition(&self, spec: &NodeSpec) -> Result<ValidationResult>` - Validate node composition
- `generate_config(&self) -> String` - Generate node configuration from composition
- `registry(&self) -> &ModuleRegistry` - Get module registry
- `registry_mut(&mut self) -> &mut ModuleRegistry` - Get mutable registry

#### `NodeSpec`

Specification for a composed node.

```rust
pub struct NodeSpec {
    pub network_type: NetworkType,
    pub modules: Vec<ModuleSpec>,
    pub metadata: NodeMetadata,
}
```

#### `ModuleSpec`

Specification for a module in a composed node.

```rust
pub struct ModuleSpec {
    pub name: String,
    pub version: Option<String>,
    pub config: HashMap<String, String>,
    pub enabled: bool,
}
```

### Module Lifecycle

#### `ModuleLifecycle`

Manages module lifecycle (start, stop, restart, health checks).

```rust
pub struct ModuleLifecycle {
    // Private fields
}
```

**Methods:**
- `new(registry: ModuleRegistry) -> Self` - Create lifecycle manager
- `with_module_manager(mut self, manager: Arc<Mutex<ModuleManager>>) -> Self` - Attach module manager
- `start_module(&mut self, name: &str) -> Result<()>` - Start a module
- `stop_module(&mut self, name: &str) -> Result<()>` - Stop a module
- `restart_module(&mut self, name: &str) -> Result<()>` - Restart a module
- `module_status(&self, name: &str) -> Result<ModuleStatus>` - Get module status
- `module_health(&self, name: &str) -> Result<ModuleHealth>` - Get module health
- `registry(&self) -> &ModuleRegistry` - Get module registry

#### `ModuleStatus`

Module runtime status.

```rust
pub enum ModuleStatus {
    Stopped,
    Starting,
    Running,
    Stopping,
    Error(String),
}
```

#### `ModuleHealth`

Module health information.

```rust
pub struct ModuleHealth {
    pub is_healthy: bool,
    pub last_heartbeat: Option<SystemTime>,
    pub error_count: u64,
    pub last_error: Option<String>,
}
```

## CLI Tools

### `blvm-keygen`

Generate governance keypairs.

```bash
blvm-keygen [OPTIONS]

Options:
    -o, --output <OUTPUT>    Output file [default: governance.key]
    -f, --format <FORMAT>    Output format (text, json) [default: text]
    --seed <SEED>            Generate deterministic keypair from seed
    --show-private          Show private key in output
```

### `blvm-sign`

Sign governance messages.

```bash
blvm-sign [OPTIONS] <COMMAND>

Options:
    -o, --output <OUTPUT>    Output file [default: signature.txt]
    -f, --format <FORMAT>    Output format (text, json) [default: text]
    -k, --key <KEY>          Private key file

Commands:
    release                 Sign a release message
    module                  Sign a module approval message
    budget                  Sign a budget decision message
```

### `blvm-verify`

Verify governance signatures and multisig thresholds.

```bash
blvm-verify [OPTIONS] <COMMAND>

Options:
    -f, --format <FORMAT>    Output format (text, json) [default: text]
    -s, --signatures <SIGS>  Signature files (comma-separated)
    --threshold <THRESHOLD>  Threshold (e.g., "3-of-5")
    --pubkeys <PUBKEYS>      Public key files (comma-separated)

Commands:
    release                 Verify a release message
    module                  Verify a module approval message
    budget                  Verify a budget decision message
```

## Usage Examples

### Basic Governance Operations

```rust
use blvm_sdk::{GovernanceKeypair, GovernanceMessage, sign_message, verify_signature};

// Generate keypair
let keypair = GovernanceKeypair::generate()?;

// Create message
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123".to_string(),
};

// Sign message
let message_bytes = message.to_signing_bytes();
let signature = sign_message(&keypair.secret_key, &message_bytes)?;

// Verify signature
let verified = verify_signature(&signature, &message_bytes, &keypair.public_key())?;
assert!(verified);
```

### Multisig Operations

```rust
use blvm_sdk::{GovernanceKeypair, GovernanceMessage, Multisig, sign_message};

// Generate 5 keypairs for 3-of-5 multisig
let keypairs: Vec<_> = (0..5)
    .map(|_| GovernanceKeypair::generate().unwrap())
    .collect();
let public_keys: Vec<_> = keypairs.iter()
    .map(|kp| kp.public_key())
    .collect();

// Create multisig
let multisig = Multisig::new(3, 5, public_keys)?;

// Create message
let message = GovernanceMessage::Release {
    version: "v1.0.0".to_string(),
    commit_hash: "abc123".to_string(),
};
let message_bytes = message.to_signing_bytes();

// Sign with 3 keys
let signatures: Vec<_> = keypairs[0..3]
    .iter()
    .map(|kp| sign_message(&kp.secret_key_bytes(), &message_bytes).unwrap())
    .collect();

// Verify multisig threshold
let verified = multisig.verify(&message_bytes, &signatures)?;
assert!(verified);
```

### Module Registry Usage

```rust
use blvm_sdk::ModuleRegistry;

// Create registry
let mut registry = ModuleRegistry::new("modules");

// Discover modules
let modules = registry.discover_modules()?;
println!("Found {} modules", modules.len());

// Get specific module
let module = registry.get_module("lightning-module", Some("1.0.0"))?;
println!("Module: {} v{}", module.name, module.version);

// Resolve dependencies
let deps = registry.resolve_dependencies(&["lightning-module".to_string()])?;
```

## See Also

- [Module Development](../sdk/module-development.md) - Building modules that use these APIs
- [SDK Examples](../sdk/examples.md) - More usage examples
- [API Index](../reference/api-index.md) - Cross-reference to all APIs
- [docs.rs/blvm-sdk](https://docs.rs/blvm-sdk) - Complete Rust API documentation
