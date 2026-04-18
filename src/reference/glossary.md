# Glossary

Key terms and concepts used throughout the BLVM documentation.

## BLVM Components

**BLVM** (Bitcoin Low-Level Virtual Machine) - Compiler-like infrastructure for Bitcoin implementations. The [Orange Paper](orange-paper.md) is the mathematical specification (IR); the implementation is **validated against** it via [formal verification](../consensus/formal-verification.md) (blvm-spec-lock), not generated or transformed from the IR. Similar to how LLVM provides compiler infrastructure, BLVM provides Bitcoin implementation infrastructure.

**Orange Paper** - Mathematical specification of Bitcoin's consensus protocol, serving as the "intermediate representation" (IR) in BLVM's compiler-like architecture. The implementation is **validated against** this spec via formal verification; code is not generated or transformed from the IR. See [Orange Paper](orange-paper.md).

**Optimization Passes** - Runtime optimizations applied to the [blvm-consensus](../consensus/overview.md) implementation (e.g. constant folding, memory layout, SIMD vectorization, bounds check optimization, dead code elimination). They optimize the implementation code; the implementation is validated against the Orange Paper, not generated from it. See [Optimization Passes](../consensus/architecture.md#optimization-passes).

**blvm-primitives** - Shared foundation crate: Bitcoin types, serialization, crypto, opcodes, constants. Used by blvm-consensus and blvm-protocol; consensus re-exports for API compatibility. See [API Index](api-index.md#foundation-blvm-primitives).

**blvm-consensus** - Optimized mathematical implementation of Bitcoin consensus rules with [formal verification](../consensus/formal-verification.md). Builds on **blvm-primitives**; block/script logic in `block/` and `script/` submodules. See [Consensus Overview](../consensus/overview.md).

**blvm-protocol** - Protocol abstraction layer for multiple Bitcoin variants (mainnet, testnet, regtest) while maintaining consensus compatibility. Uses **blvm-primitives**. See [Protocol Overview](../protocol/overview.md).

**blvm-node** - Bitcoin node implementation with [storage](../node/storage-backends.md), [networking](../node/transport-abstraction.md), [RPC](../node/rpc-api.md), and [mining](../node/mining.md) capabilities. Intended as the reference full node; treat production deployment like any consensus-adjacent system (hardening, monitoring, [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md)). See [Node Overview](../node/overview.md).

**blvm-sdk** - Developer toolkit: [governance primitives](../governance/overview.md), [node module authoring](../sdk/module-development.md) (macros, `run_module!`, `node` feature), [composition](../architecture/module-system.md), and CLI tools (keygen, sign, compose, etc.). See [SDK Overview](../sdk/overview.md).

## Governance

**Bitcoin Commons** - Forkable governance framework applying Elinor Ostrom's commons management principles through cryptographic enforcement. See [Governance Overview](../governance/overview.md).

**5-Tier Governance Model** - Constitutional governance system with graduated signature thresholds (3-of-5 to 6-of-7) and review periods (7 days to 365 days) based on change impact. See [Layer-Tier Model](../governance/layer-tier-model.md).

**Forkable Governance** - Governance rules can be forked by users if they disagree with decisions, creating exit competition and preventing capture. See [Governance Fork](../governance/governance-fork.md).

**Cryptographic Enforcement** - All governance actions require cryptographic signatures from maintainers, making power visible and accountable. See [Keyholder Procedures](../governance/keyholder-procedures.md).


## Technical Concepts

**Formal Verification** - **BLVM Specification Lock**: Z3-backed proofs tying spec-locked consensus code to Orange Paper contracts. See [Formal Verification](../consensus/formal-verification.md).

**Proofs Locked to Code** - Spec-lock proofs live with the functions they verify; code changes require proof updates. See [Formal Verification](../consensus/formal-verification.md).

**Spec Drift Detection** - Automated detection when implementation code diverges from the [Orange Paper](orange-paper.md) mathematical specification.

**Compiler-Like Architecture** - The [Orange Paper](orange-paper.md) is the spec (IR); [blvm-consensus](../consensus/overview.md) is the implementation, **validated against** that spec through tests, review, and [BLVM Specification Lock](../consensus/formal-verification.md). [Optimization passes](../consensus/architecture.md#optimization-passes) optimize the implementation. No code is generated from the IR. See [System Overview](../architecture/system-overview.md).

**Process Isolation** - [Module system](../architecture/module-system.md) design where each module runs in a separate process with isolated memory, preventing failures from propagating to the base node.

**IPC** (Inter-Process Communication) - Communication mechanism between modules and the node using Unix domain sockets with length-delimited binary messages. See [Module IPC Protocol](../architecture/module-ipc-protocol.md).

## Storage & Networking

**Storage Backends** - Database backends for blockchain data. **`database_backend = auto`** selects by build features (RocksDB when enabled, then TidesDB, Redb, Sled). See [Storage Backends](../node/storage-backends.md) and [Configuration Reference](configuration-reference.md).

**Pruning** - Storage optimization that removes old block data while keeping the UTXO set. Configurable to keep last N blocks.

**Transport Abstraction** - Unified abstraction supporting multiple transport protocols: **TCP** (default, Bitcoin P2P compatible) and **Iroh/QUIC** (experimental). See [Transport Abstraction](../node/transport-abstraction.md).

**Network Variants** - Bitcoin network types: **Mainnet** (BitcoinV1, production), **Testnet3** (test network), **Regtest** (regression testing, isolated).

## Consensus & Protocol

**Consensus Rules** - Mathematical rules that all Bitcoin nodes must follow to maintain network consensus. Defined in the [Orange Paper](orange-paper.md) and implemented in [blvm-consensus](../consensus/overview.md).

**BIP** (Bitcoin Improvement Proposal) - Standards for Bitcoin protocol changes. BLVM implements numerous BIPs including BIP30, BIP34, BIP66, BIP90, BIP147, BIP141/143, BIP340/341/342. See [Protocol Specifications](protocol-specifications.md).

**SegWit** (Segregated Witness) - [BIP141/143](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki) implementation separating witness data from transaction data, enabling transaction malleability fixes and capacity improvements.

**Taproot** - [BIP340/341/342](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) implementation providing Schnorr signatures, Merkle tree scripts, and improved privacy.

**RBF** (Replace-By-Fee) - BIP125 implementation allowing transaction replacement with higher fees before confirmation.

## Development

**Module System** - [Process-isolated system](../architecture/module-system.md) supporting optional features ([Lightning](../modules/lightning.md), [merge mining](../node/mining-stratum-v2.md), privacy enhancements) without affecting consensus or base node stability.

**Module Manifest** (`module.toml`) - Configuration file defining module metadata, capabilities, dependencies, and entry point.

**Capabilities** - Permissions system for modules. Capabilities use snake_case in `module.toml` and map to `Permission` enum variants. Core capabilities include: `read_blockchain`, `read_utxo`, `read_chain_state`, `subscribe_events`, `send_transactions`, `read_mempool`, `read_network`, `network_access`, `read_lightning`, `read_payment`, `read_storage`, `write_storage`, `manage_storage`, `read_filesystem`, `write_filesystem`, `manage_filesystem`, `register_rpc_endpoint`, `manage_timers`, `report_metrics`, `read_metrics`, `discover_modules`, `publish_events`, `call_module`, `register_module_api`. See [Permission System](../architecture/module-system.md#permission-system) for complete list.

**RPC** (Remote Procedure Call) - [JSON-RPC 2.0 interface](../node/rpc-api.md) for interacting with the node. Methods follow conventions widely used by Bitcoin node RPC documentation.

## Governance Status

**Governance activation** - Governance rules are not yet activated; test keys are used. When activated, real cryptographic keys and keyholder onboarding enforce governance. The system is experimental until then. See [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md).
