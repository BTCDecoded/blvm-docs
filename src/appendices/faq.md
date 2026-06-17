# Frequently Asked Questions

Short answers for operators and developers. Governance philosophy and tier mechanics: [Governance Overview](../governance/overview.md) and [Governance Model](../governance/governance-model.md).

## General

### What is BLVM?

BLVM (Bitcoin Low-Level Virtual Machine) is compiler-like infrastructure for Bitcoin: the [Orange Paper](../reference/orange-paper.md) spec, **blvm-consensus**, **blvm-protocol**, **blvm-node**, and **blvm-sdk**. See [Introduction](../introduction.md).

### Is this a fork of Bitcoin?

No. BLVM does not fork Bitcoin’s chain or consensus rules. It implements the same consensus rules as mainnet Bitcoin.

### Is the system production ready?

BLVM ships a full node stack with tests and formal verification tooling, but **readiness depends on your deployment**: apply your own security review, RPC hardening, and monitoring. Governance is not universally activated. See [Deployment posture](../security/deployment-posture.md) and [System Status](https://github.com/BTCDecoded/.github/blob/main/SYSTEM_STATUS.md).

### Where is the code?

Repositories under [BTCDecoded](https://github.com/BTCDecoded) (e.g. `blvm`, `blvm-node`, `blvm-consensus`). The umbrella release binary is built from the `blvm` crate.

## Running a node

### How do I install BLVM?

Pre-built packages and binaries: [Installation](../getting-started/installation.md). Verify checksums on every download.

### How do I run my first node?

[Quick Start](../getting-started/quick-start.md) (regtest, ~5 minutes) or [First Node Setup (regtest)](../getting-started/first-node.md) (config file). **Mainnet:** [Mainnet initial sync](../getting-started/mainnet-sync.md) — not bare `blvm --network mainnet`.

### What must I do before mainnet?

See [Deployment posture](../security/deployment-posture.md) — RPC auth, bind addresses, release verification, backups, and module supply chain.

### How do I configure the node?

`blvm.toml`, CLI flags, and `BLVM_*` environment variables. Precedence: CLI > ENV > file > defaults. [Node Configuration](../node/configuration.md), [Configuration Reference](../reference/configuration-reference.md).

### Can I start from an existing Bitcoin Core datadir?

Yes, with the **`rocksdb`** feature (default release binaries): stop **`bitcoind`**, point **`--datadir`** at a synced Core tree, migrate once to **`<datadir>/blvm/`**. See [Operations — Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir).

### What storage backends are supported?

`database_backend = "auto"` (usually **heed3** in default builds), or explicit **rocksdb**, **redb**, **sled**, **tidesdb**. See [Storage Backends](../node/storage-backends.md).

### What experimental compile-time features exist?

Stable GitHub Releases ship the **base** binary (`production` features). UTXO commitments, Dandelion++, CTV, Stratum V2, Iroh, and related flags need an experimental/source build. See [Installation — experimental variant](../getting-started/installation.md#experimental-build-variant).

### What RPC methods are available?

JSON-RPC aligned with common Bitcoin node docs, plus BLVM-specific and module-extended methods. See [RPC API Reference](../node/rpc-api.md) and the parity table there.

### How do I troubleshoot?

[Appendix — Troubleshooting](troubleshooting.md). Mainnet IBD: [Troubleshooting — Mainnet IBD](troubleshooting.md#mainnet-ibd).

## Governance

Questions operators and new contributors often ask before reading the full governance docs.

### Do I need governance to run a node?

No. Running a BLVM node does not require tiers, multisig, or governance tooling. Use the [Operator guide](../getting-started/operator-guide.md) and [Deployment posture](../security/deployment-posture.md). Governance applies when you contribute code, review PRs, or sign releases.

### What is Bitcoin Commons vs BLVM?

BLVM is the technical stack (spec, node, SDK). Bitcoin Commons is the governance framework (tiers, signatures, fork rules). They are related but serve different roles. See [Governance Overview](../governance/overview.md).

### What are layers, tiers, and signatures?

**Layers** map repo areas (consensus, protocol, node, modules). **Tiers** set how many signatures a change needs. **Signatures** are cryptographic approvals from registered keyholders. Constitutional layers need more signatures than extension layers. Details: [Governance Model](../governance/governance-model.md), [Layer-Tier Model](../governance/layer-tier-model.md).

### Why “6x harder to capture”?

Bitcoin Commons applies graduated signature thresholds and review periods so capturing governance requires compromising many independent keyholders across layers—not a single maintainer group. See [Governance Model](../governance/governance-model.md).

## Modules and development

### How does the module system work?

Optional features run in isolated processes with IPC. See [Module catalog](../modules/overview.md) and [Building modules](../sdk/module-development.md).

### Can I build my own module?

Yes. Start with [Building your first module](../getting-started/first-module.md), then [Building modules](../sdk/module-development.md).

### How can I contribute?

[Contributing](../development/contributing.md), [Contributing to Documentation](contributing-docs.md).

### What documentation should I read?

Use the [Introduction — Who is this for](../introduction.md#who-is-this-for) paths. Operators: Getting Started + Node + Security. Developers: SDK + Modules. Researchers: Orange Paper + Formal Verification.

## Spec and verification

### What is the Orange Paper?

The normative mathematical specification of Bitcoin consensus—the reference “IR” for BLVM. [Orange Paper](../reference/orange-paper.md).

### How does formal verification work?

**BLVM Specification Lock** links spec-locked Rust code to Orange Paper properties; Z3 proofs and tests complement differential and integration testing. [Formal Verification](../consensus/formal-verification.md).
