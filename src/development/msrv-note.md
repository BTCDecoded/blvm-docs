# Rust MSRV and pinned CI toolchains

Published **`blvm-*`** crates declare **`rust-version`** in **`Cargo.toml`**. For any **`cargo build`** / **`cargo check`** graph, the compiler must satisfy the **maximum** `rust-version` among packages that graph actually compiles.

## Representative graphs (snapshot — re-audit before releases)

| Role | Typical crates | Effective MSRV (max of declares in graph) |
|------|----------------|------------------------------------------|
| Consensus development | `blvm-consensus` + deps | **1.83** |
| Protocol + consensus | `blvm-protocol` → `blvm-consensus` | **1.83** (consensus dominates) |
| Node / `blvm` binary | `blvm-node`, `blvm`, SDK integration tests | **1.83** (pulls `blvm-consensus`) |
| Crypto-only | `blvm-secp256k1` alone | **1.82** |

**Inventory command** (multi-repo workspace):

```bash
rg '^rust-version' --glob 'Cargo.toml'
```

## CI vs MSRV

Repositories pin CI via **`rust-toolchain.toml`**; that toolchain is often **newer** than every crate’s declared MSRV. CI green **does not** prove builds on the oldest supported compiler unless you run **`cargo +<msrv> check`** (below).

## Release checklist (**F4**)

Before publishing or bumping MSRV:

1. **`cargo +<MSRV> check -p <crate>`** on the narrowest graph you claim to support (add **`--features`** as needed).
2. Update **`Cargo.toml`** **`rust-version`** when language features require it.
3. Record MSRV changes in changelog / release notes.

Operator-facing summary when policy shifts: **[Deployment posture](https://docs.thebitcoincommons.org/security/deployment-posture.html)** and repo **`CONTRIBUTING.md`**.
