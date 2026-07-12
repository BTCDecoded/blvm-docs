# Rust MSRV and pinned CI toolchains

Published **`blvm-*`** crates declare **`rust-version`** and **`edition`** in **`Cargo.toml`**. For any **`cargo build`** / **`cargo check`** graph, the compiler must satisfy the **maximum** `rust-version` among packages that graph actually compiles.

## Representative graphs (re-audit before releases)

| Role | Typical crates | Effective MSRV (max of declares in graph) |
|------|----------------|------------------------------------------|
| Consensus development | `blvm-consensus` + deps | **1.85** |
| Protocol + consensus | `blvm-protocol` → `blvm-consensus` | **1.85** (consensus dominates) |
| Node / `blvm` binary | `blvm-node`, `blvm`, SDK integration tests | **1.85** (pulls `blvm-consensus`) |
| Crypto-only | `blvm-secp256k1` alone | Check crate `Cargo.toml` |

**Edition:** workspace crates on the node/consensus path use **Rust edition 2024**.

**Inventory command** (multi-repo workspace):

```bash
rg '^rust-version' --glob 'Cargo.toml'
rg '^edition' --glob 'Cargo.toml'
```

## CI vs MSRV

The **`blvm`** repository pins CI via **`rust-toolchain.toml`** (currently **1.88.0**). CI green **does not** prove builds on the oldest supported compiler unless you run **`cargo +<msrv> check`** (below).

## Release checklist

Before publishing or bumping MSRV:

1. **`cargo +<MSRV> check -p <crate>`** on the narrowest graph you claim to support (add **`--features`** as needed).
2. Update **`Cargo.toml`** **`rust-version`** when language features require it.
3. Record MSRV changes in changelog / release notes.

Operator-facing summary when policy shifts: **[Deployment posture](https://docs.thebitcoincommons.org/security/deployment-posture.html)** and repo **[Contributing](../development/contributing.md)**.
