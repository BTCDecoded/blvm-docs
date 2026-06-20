# RPC transport × authentication matrix

Operator reference for **which JSON-RPC surface supports which auth model**. P2P transport comparison (**TCP vs QUIC**) lives under **[Transport abstraction](../node/transport-abstraction.md)** — different scope.

## Matrix

| Surface | Feature / bind | Bearer (`[rpc_auth]`) | HTTP Basic | TLS client certs | Notes |
|---------|----------------|----------------------|------------|------------------|-------|
| **JSON-RPC (TCP HTTP)** | Default **`blvm`** RPC | **Yes** — `Authorization: Bearer` | **Yes** — `Authorization: Basic` (ckpool; password auto-admin) | When configured | Prefer **loopback** for Basic (cleartext on wire). |
| **JSON-RPC (QUIC HTTP/3)** | **`quinn`** listener; ALPN **`h3`** | **Yes** — same **`RpcAuthManager`** as TCP | **Yes** — HTTP/3 request headers | Server TLS on UDP listener | Shares live **`Arc<RpcServer>`** with TCP HTTP. UDP TLS cert lifecycle may differ from TCP unless you terminate at a proxy. |
| **REST (`/api/v1/`)** | **`rest-api`** feature; **`[rest_api].enabled`** | **Yes** — when REST server built **`with_auth`** | Same auth stack; **admin RBAC** via `rest/rbac.rs` | Off by default | Separate bind (default **8080** / **18080** / **28443**). See [RPC API — REST](../node/rpc-api.md#rest-api). |

## Practical guidance

- **Strict RPC auth (`rpc_auth.required = true`):** Bearer and HTTP Basic enforcement apply on **both** TCP HTTP JSON-RPC and **HTTP/3 JSON-RPC over QUIC** — configure **`[rpc_auth]`** once; semantics match (**same **`RpcAuthManager`**, shared **`dispatch_json_rpc_post_body`** path). Mining pools (ckpool) typically use **Basic** on loopback.
- **QUIC JSON-RPC:** Requires an HTTP/3-capable client (QUIC + ALPN **`h3`**). **[Deployment posture](deployment-posture.md)** still governs exposure class (UDP firewall rules differ from TCP).
- **Non-loopback RPC:** Same posture doc + **[First node](../getting-started/first-node.md)** production notes.

## Historical note (**G2.3**, QUIC × strict auth)

Earlier builds exposed JSON-RPC on QUIC **without** HTTP headers and therefore **skipped** the QUIC RPC listener when **`rpc_auth.required`** was **`true`**. Current **`quinn`** RPC uses **HTTP/3**, so **`Authorization`** and rate limits match TCP HTTP. Proxy / mutual-TLS termination remains deployment-specific.

## Source anchors

- QUIC RPC + **`Arc<RpcServer>`**: `blvm-node/src/rpc/mod.rs`, `blvm-node/src/rpc/quinn_server.rs`.
- Shared POST dispatch: `blvm-node/src/rpc/server.rs` (`dispatch_json_rpc_post_body`).
- **`RpcAuthConfig::default()`**: `required: false` — local-dev friendly; tighten for LAN/WAN.
