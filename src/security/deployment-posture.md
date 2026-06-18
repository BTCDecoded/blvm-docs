# Deployment posture

Canonical operator-facing guidance for running **`blvm`** / **`blvm-node`**: exposure classes, minimum controls, and **[RPC transport × authentication](rpc-transport-auth-matrix.md)**.

Published copy: [Deployment posture (BLVM docs)](https://docs.thebitcoincommons.org/security/deployment-posture.html).

## How to read this page

| Term | Meaning |
|------|---------|
| **Required** | Omitting this on the stated network / bind pattern materially increases risk of unauthorized RPC abuse, fund theft adjacent systems, or confidentiality loss. |
| **Recommended** | Strongly advised operational hygiene; omissions reduce resilience or auditability. |
| **Unsupported** | Not a supported safety combination in current code — do not rely on it as a security boundary. |

## Supported contexts

- **Regtest / local development** — **Supported** for day-to-day work when P2P and RPC are unreachable from untrusted networks (typical loopback defaults). **`rpc_auth.required = false`** is acceptable **only** while RPC stays on **`127.0.0.1`**, **`::1`**, or equivalent loopback.
- **Testnet** — Treat as **internet-adjacent**: peer set is untrusted; apply **Recommended** items below before exposing RPC beyond loopback. (Signet is not yet a supported network in BLVM.)
- **Mainnet** — **High assurance**: assume global attackers on P2P and opportunistic scanning on RPC-shaped ports. Meet **Required** items for any non-loopback control plane.

## Critical deployment concerns

### Control plane (JSON-RPC, REST, QUIC RPC)

- **Required (non-loopback):** **`[rpc_auth]`** with **`required = true`**. Use **Bearer tokens** (`tokens`, `admin_tokens`, `token_file`, **`RPC_AUTH_TOKENS`**) and/or **HTTP Basic** (`username`, `password` for ckpool / Core-style clients). TLS client certificates remain supported when configured. See **[Configuration reference](../reference/configuration-reference.md)** and **[RPC transport × authentication](rpc-transport-auth-matrix.md)**.
- **REST note:** `/api/v1/*` requires compile-time **`rest-api`** and **`[rest_api].enabled = true`** (separate bind; off by default). Uses the same **`RpcAuthManager`** as JSON-RPC when auth is configured.
- **Recommended:** Bind RPC to **loopback** when using HTTP Basic — credentials are cleartext on the wire. Use a reverse proxy or firewall allowlists when exposing RPC beyond localhost; server-side rate limits do not replace edge policy.
- **Recommended:** Grant **admin** access only to operators and mining tooling (`getblocktemplate`, `submitblock`, `generatetoaddress`, destructive control methods). Bearer tokens in `tokens` alone are read-only unless also listed in `admin_tokens`; `[rpc_auth].password` is registered as admin automatically when set.
- **Note (QUIC):** JSON-RPC over QUIC uses **HTTP/3** (ALPN **`h3`**) and shares the same **`RpcAuthManager`** as TCP HTTP (Bearer and Basic). Treat the **UDP listener** as its own exposure surface. See **[RPC transport × authentication](rpc-transport-auth-matrix.md)**.

### Peer layer (P2P)

- **Required (mainnet/testnet):** Run maintained releases; keep **`listen_addr`** bound intentionally (avoid accidental **`0.0.0.0`** without firewall intent).
- **Recommended:** Monitor peer bans / DoS logs; cap LAN peer assumptions using documented LAN-peering rules (**[Threat models](threat-models.md)**).

### Data directory, backups, integrity

- **Required:** Protect the configured **`data_dir`** with host filesystem permissions (only the node OS user).
- **Recommended:** Encrypted backups of wallet-adjacent artifacts **elsewhere** — the node is **not** a wallet, but keys or module secrets on the same host still warrant backup hygiene.
- **Recommended:** Snapshot **`data_dir`** only when the node is stopped or via backend-specific backup guidance (**[Storage backends](../node/storage-backends.md)**) to avoid torn pages.

### Modules, WASM, IPC

- **Required:** Treat third-party modules as **supply-chain code**: verify signatures / maintainer policy before production enablement.
- **Recommended:** For **`wasm-modules`**, set embedder budget keys documented in **`blvm-node`** [`docs/CONFIGURATION_GUIDE.md`](https://github.com/BTCDecoded/blvm-node/blob/main/docs/CONFIGURATION_GUIDE.md); prefer process-isolated modules when in-process WASM is unnecessary.

### Supply chain and patching

- **Recommended:** Run **`cargo audit`** (or distributor SBOM process) on lockfiles you ship; reconcile **`blvm-node`** **`AUDIT_SUPPRESSIONS`** when upgrading **`iroh`**, **`quinn`**, **`hickory`**, or **`time`**.
- **Recommended:** Prefer **`--locked`** builds where your repo policy commits a lockfile (**`blvm`** umbrella does; library-style crates may not — see workspace **`Cargo.lock`** policy).

### Secrets and logging

- **Required:** Never commit **`RPC_AUTH_TOKENS`**, **`[rpc_auth].password`**, TLS keys, or **`token_file`** paths into config repos; restrict log forwarding so Bearer tokens and Basic credentials are not captured in HTTP access logs.
- **Recommended:** Rotate tokens after operational incidents.

### Software maturity

- **Required acknowledgment:** BLVM remains **pre-production for mainnet high assurance** unless your organization has independently validated releases — see **[Threat models](threat-models.md)** and **[SECURITY.md](https://github.com/BTCDecoded/blvm-node/blob/main/SECURITY.md)**.

## Before mainnet (first sync checklist)

Complete before running a mainnet node or exposing RPC beyond loopback:

1. **Release verification** — Download from [btcdecoded.org/install](https://btcdecoded.org/install) or [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest); verify `checksums.sha256` ([Installation](../getting-started/installation.md)).
2. **Sync path** — Use [Mainnet initial sync](../getting-started/mainnet-sync.md) (`start-ibd-mainnet.sh` or bundled example TOML), not bare `blvm --network mainnet`.
3. **Data directory** — Dedicated path (e.g. `~/.local/share/blvm-mainnet`); restrict filesystem permissions to the node OS user.
4. **IBD tuning** — Review bundled `blvm-mainnet-ibd.toml.example`; optional `BLVM_IBD_ENGINE` per [IBD UTXO engine](../node/ibd-engine.md).
5. **Modules** — Keep third-party modules disabled during first sync; verify maintainer policy before production enablement.
6. **Backups** — Plan snapshot/backup policy; snapshot `data_dir` when stopped or per [Storage backends](../node/storage-backends.md).
7. **RPC exposure** — Before binding RPC off loopback, complete the [Minimum checklist (non-loopback RPC)](#minimum-checklist-non-loopback-rpc) below.

Then meet **Required** items under **Supported contexts → Mainnet** above.

## Minimum checklist (non-loopback RPC)

1. Set **`rpc_auth.required = true`** (or equivalent env) **unless** RPC listens only on **`127.0.0.1`** / **`::1`** (loopback).
2. Provide **Bearer tokens** (`tokens`, `admin_tokens`, `token_file`, **`RPC_AUTH_TOKENS`**) and/or **HTTP Basic** (`username` / `password`) or TLS client certificates as documented in **[Configuration reference](../reference/configuration-reference.md)**.
3. Prefer **`transport_preference = "tcponly"`** until QUIC RPC + strong auth is explicitly required — see **[RPC transport × authentication](rpc-transport-auth-matrix.md)**.

## Relationship to other docs

- **[Threat models](threat-models.md)** — Attack surfaces and boundaries (developer + operator framing).
- **[First node](../getting-started/first-node.md)** — Hands-on regtest path; links here for production-facing posture.
