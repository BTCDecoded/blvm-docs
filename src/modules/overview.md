# Modules Overview

## Introduction

BLVM node uses a modular architecture where optional features run as separate, process-isolated modules. This extends node functionality without affecting consensus or base node stability.

## Available Modules

The following modules are available for bllvm-node:

### Core Modules

- **[Lightning Network Module](lightning.md)** - Lightning Network payment processing, invoice verification, payment routing, and channel management
- **[Commons Mesh Module](mesh.md)** - Payment-gated mesh networking with routing fees, traffic classification, and anti-monopoly protection
- **[Governance Module](governance.md)** - Governance webhook integration, economic node tracking, and veto system integration
- **[Stratum V2 Module](stratum-v2.md)** - Stratum V2 mining protocol support, mining pool management, and merge mining coordination

## Module System Architecture

All modules run in separate processes with IPC communication (see [Module System Architecture](../architecture/module-system.md) for details), providing:

- **Process Isolation**: Each module runs in isolated memory space
- **Crash Containment**: Module failures don't affect the base node
- **Consensus Isolation**: Modules cannot modify consensus rules or UTXO set
- **Security**: Modules communicate only through well-defined APIs

For detailed information about the module system architecture, see [Module System](../architecture/module-system.md).

## Installing Modules

Modules can be installed in several ways:

### Via Cargo

```bash
cargo install bllvm-lightning
cargo install bllvm-mesh
cargo install bllvm-governance
cargo install bllvm-stratum-v2
```

### Via Module Installer

```bash
cargo install cargo-bllvm-module
cargo bllvm-module install bllvm-lightning
cargo bllvm-module install bllvm-mesh
cargo bllvm-module install bllvm-governance
cargo bllvm-module install bllvm-stratum-v2
```

### Manual Installation

1. Build the module: `cargo build --release`
2. Copy the binary to `modules/<module-name>/target/release/`
3. Create `module.toml` manifest in the module directory
4. Restart the node or use runtime module loading

## Module Configuration

Each module requires a `config.toml` file in its module directory. See individual module documentation ([Lightning](lightning.md), [Mesh](mesh.md), [Governance](governance.md), [Stratum V2](stratum-v2.md)) for configuration options.

## Module Lifecycle

Modules can be:
- **Loaded** at node startup (if enabled in configuration)
- **Loaded** at runtime via RPC or module manager API
- **Unloaded** at runtime without affecting the base node
- **Reloaded** (hot reload) for configuration updates

## See Also

- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [SDK API Reference](../sdk/api-reference.md) - Complete SDK API documentation
- [SDK Examples](../sdk/examples.md) - Module development examples
- [Node Configuration](../node/configuration.md) - Node-level module configuration


