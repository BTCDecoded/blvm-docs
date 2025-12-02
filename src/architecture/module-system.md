# Module System

## Overview

The module system enables optional features (Lightning Network, merge mining, privacy enhancements) without affecting consensus or base node stability. Modules run in separate processes with IPC communication, providing security through isolation.

## Available Modules

The following modules are available for bllvm-node:

- **[Lightning Network Module](../modules/lightning.md)** - Lightning Network payment processing, invoice verification, payment routing, and channel management
- **[Commons Mesh Module](../modules/mesh.md)** - Payment-gated mesh networking with routing fees, traffic classification, and anti-monopoly protection
- **[Governance Module](../modules/governance.md)** - Governance webhook integration, economic node tracking, and veto system integration
- **[Stratum V2 Module](../modules/stratum-v2.md)** - Stratum V2 mining protocol support, mining pool management, and merge mining coordination

For detailed documentation on each module, see the [Modules](../modules/overview.md) section.

## Architecture

### Process Isolation

Each module runs in a separate process with isolated memory. The base node consensus state is protected and read-only to modules.

```
┌─────────────────────────────────────┐
│         bllvm-node Process          │
│  ┌───────────────────────────────┐ │
│  │    Consensus State             │ │
│  │    (Protected, Read-Only)      │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │    Module Manager             │ │
│  │    (Orchestration)            │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
              │ IPC (Unix Sockets)
              │
┌─────────────┴─────────────────────┐
│      Module Process (Isolated)     │
│  ┌───────────────────────────────┐ │
│  │    Module State               │ │
│  │    (Separate Memory Space)    │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │    Sandbox                    │ │
│  │    (Resource Limits)          │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Code**: ```1:37:bllvm-node/src/module/mod.rs```

## Core Components

### ModuleManager

Orchestrates all modules, handling lifecycle, runtime loading/unloading/reloading, and coordination.

**Features:**
- Module discovery and loading
- Process spawning and monitoring
- IPC server management
- Event subscription management
- Dependency resolution
- Registry integration

**Code**: ```1:520:bllvm-node/src/module/manager.rs```

### Process Isolation

Modules run in separate processes via `ModuleProcessSpawner`:

- Separate memory space
- Isolated execution environment
- Resource limits enforced
- Crash containment

**Code**: ```1:132:bllvm-node/src/module/process/spawner.rs```

### IPC Communication

Modules communicate with the base node via Unix domain sockets (Unix) or named pipes (Windows):

- Request/response protocol
- Event subscription system
- Correlation IDs for async operations
- Type-safe message serialization

**Code**: ```1:234:bllvm-node/src/module/ipc/protocol.rs```

### Security Sandbox

Modules run in sandboxed environments with:

- Resource limits (CPU, memory, file descriptors)
- Filesystem restrictions
- Network restrictions
- Permission-based API access

**Code**: ```1:60:bllvm-node/src/module/sandbox/network.rs```

### Permission System

Modules request capabilities that are validated before API access:

- `ReadBlockchain` - Read-only blockchain access
- `ReadUTXO` - Query UTXO set (read-only)
- `ReadChainState` - Query chain state (height, tip)
- `SubscribeEvents` - Subscribe to node events
- `SendTransactions` - Submit transactions to mempool

**Code**: ```1:184:bllvm-node/src/module/security/permissions.rs```

## Module Lifecycle

```
Discovery → Verification → Loading → Execution → Monitoring
    │            │            │           │            │
    │            │            │           │            │
    ▼            ▼            ▼           ▼            ▼
Registry    Signer      Loader      Process      Monitor
```

### Discovery

Modules discovered through:
- Local filesystem (`modules/` directory)
- Module registry (REST API)
- Manual installation

**Code**: ```1:200:bllvm-node/src/module/registry/discovery.rs```

### Verification

Each module verified through:
- Hash verification (binary integrity)
- Signature verification (multisig maintainer signatures)
- Permission checking (capability validation)
- Compatibility checking (version requirements)

**Code**: ```1:200:bllvm-node/src/module/validation/manifest_validator.rs```

### Loading

Module loaded into isolated process:
- Sandbox creation (resource limits)
- IPC connection establishment
- API subscription setup

**Code**: ```159:235:bllvm-node/src/module/manager.rs```

### Execution

Module runs in isolated process:
- Separate memory space
- Resource limits enforced
- IPC communication only
- Event subscription active

### Monitoring

Module health monitored:
- Process status tracking
- Resource usage monitoring
- Error tracking
- Crash isolation

**Code**: ```1:100:bllvm-node/src/module/process/monitor.rs```

## Security Model

### Consensus Isolation

Modules cannot:
- Modify consensus rules
- Modify UTXO set
- Access node private keys
- Bypass security boundaries
- Affect other modules

**Guarantee**: Module failures are isolated and cannot affect consensus.

### Crash Containment

Module crashes are isolated and do not affect the base node. The `ModuleProcessMonitor` detects crashes and automatically removes failed modules.

**Code**: ```144:153:bllvm-node/src/module/manager.rs```

### Security Flow

```
Module Binary
    │
    ├─→ Hash Verification ──→ Integrity Check
    │
    ├─→ Signature Verification ──→ Multisig Check ──→ Maintainer Verification
    │
    ├─→ Permission Check ──→ Capability Validation
    │
    └─→ Sandbox Creation ──→ Resource Limits ──→ Isolation
```

## Module Manifest

Module manifests use TOML format:

```toml
# Module Identity
name = "lightning-network"
version = "1.2.3"
description = "Lightning Network implementation"
author = "Alice <alice@example.com>"

# Governance
[governance]
tier = "application"
maintainers = ["alice", "bob", "charlie"]
threshold = "2-of-3"
review_period_days = 14

# Signatures
[signatures]
maintainers = [
    { name = "alice", key = "02abc...", signature = "..." },
    { name = "bob", key = "03def...", signature = "..." }
]
threshold = "2-of-3"

# Binary
[binary]
hash = "sha256:abc123..."
size = 1234567
download_url = "https://registry.bitcoincommons.org/modules/lightning-network/1.2.3"

# Dependencies
[dependencies]
"bllvm-node" = ">=1.0.0"
"another-module" = ">=0.5.0"

# Compatibility
[compatibility]
min_consensus_version = "1.0.0"
min_protocol_version = "1.0.0"
min_node_version = "1.0.0"
tested_with = ["1.0.0", "1.1.0"]

# Capabilities
capabilities = [
    "read_blockchain",
    "subscribe_events"
]
```

**Code**: ```1:200:bllvm-node/src/module/registry/manifest.rs```

## API Hub

The `ModuleApiHub` routes API requests from modules to the appropriate handlers:

- Blockchain API (blocks, headers, transactions)
- Governance API (proposals, votes)
- Communication API (P2P messaging)

**Code**: ```1:200:bllvm-node/src/module/api/hub.rs```

## Event System

Modules can subscribe to node events:

- Block connected/disconnected
- Transaction added/removed
- Chain reorganization
- Governance events

**Code**: ```1:200:bllvm-node/src/module/api/events.rs```

## Module Registry

Modules can be discovered and installed from a module registry:

- REST API client for module discovery
- Binary download and verification
- Dependency resolution
- Signature verification

**Code**: ```1:200:bllvm-node/src/module/registry/client.rs```

## Usage

### Loading a Module

```rust
use bllvm_node::module::{ModuleManager, ModuleMetadata};

let mut manager = ModuleManager::new(
    modules_dir,
    data_dir,
    socket_dir,
);

manager.start(socket_path, node_api).await?;

manager.load_module(
    "lightning-network",
    binary_path,
    metadata,
    config,
).await?;
```

### Auto-Discovery

```rust
// Automatically discover and load all modules
manager.auto_load_modules().await?;
```

**Code**: ```306:391:bllvm-node/src/module/manager.rs```

## Benefits

1. **Consensus Isolation**: Modules cannot affect consensus rules
2. **Crash Containment**: Module failures don't affect base node
3. **Security**: Process isolation and permission system
4. **Extensibility**: Add features without consensus changes
5. **Flexibility**: Load/unload modules at runtime
6. **Governance**: Modules subject to governance approval

## Use Cases

- **Lightning Network**: Payment channel management
- **Merge Mining**: Auxiliary chain support
- **Privacy Enhancements**: Transaction mixing, coinjoin
- **Alternative Mempool Policies**: Custom transaction selection
- **Smart Contracts**: Layer 2 contract execution

## Components

The module system includes:
- Process isolation
- IPC communication
- Security sandboxing
- Permission system
- Module registry
- Event system
- API hub

**Location**: `bllvm-node/src/module/`

## IPC Communication

Modules communicate with the node via the Module IPC Protocol:

- **Protocol**: Length-delimited binary messages over Unix domain sockets
- **Message Types**: Requests, Responses, Events, Logs
- **Security**: Process isolation, permission-based API access, resource sandboxing
- **Performance**: Persistent connections, concurrent requests, correlation IDs

For detailed protocol documentation, see [Module IPC Protocol](module-ipc-protocol.md).

## See Also

- [Module IPC Protocol](module-ipc-protocol.md) - Complete IPC protocol documentation
- [Modules Overview](../modules/overview.md) - Overview of all available modules
- [Lightning Network Module](../modules/lightning.md) - Lightning Network payment processing
- [Commons Mesh Module](../modules/mesh.md) - Payment-gated mesh networking
- [Governance Module](../modules/governance.md) - Governance webhook integration
- [Stratum V2 Module](../modules/stratum-v2.md) - Stratum V2 mining protocol
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules

