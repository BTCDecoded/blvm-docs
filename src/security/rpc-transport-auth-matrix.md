# RPC transport × authentication matrix

Operator reference for **which JSON-RPC surface supports which auth model**. P2P transport comparison (**TCP vs QUIC**) lives under **[Transport abstraction](../node/transport-abstraction.md)** — different scope.

## Matrix

| Surface | Feature / bind | Bearer / token auth (`[rpc_auth]`) | HTTP Basic (`username` / `password`) | TLS client certs | Notes |
|---------|----------------|--------------------------------------|--------------------------------------|------------------|--------|
| **JSON-RPC over TCP (HTTP)** | Default **`blvm`** RPC | **Supported** — **`Authorization: Bearer`** | **Supported** — **`Authorization: Basic`** (ckpool; password auto-admin) | **Supported** (when configured) | Prefer **loopback** bind for Basic auth (cleartext). |
| **JSON-RPC over QUIC (HTTP/3)** | **`quinn`** QUIC RPC listener | **Supported** — same **`RpcAuthManager`** as TCP HTTP | **Supported** on HTTP/3 request headers | QUIC presents a server TLS identity on the UDP listener (**distinct certificate lifecycle** from TCP HTTP TLS unless you terminate equivalently at a proxy) | **ALPN `h3`**. Shares the live **`Arc<RpcServer>`** so handlers and limits align with TCP HTTP. |
| **REST (`/api/v1/`)** | **`rest-api`** feature; **`[rest_api].enabled`** at startup | **Supported** via shared **`RpcAuthManager`** when REST server built **`with_auth`** | Same stack as RPC auth layer; **admin RBAC** via `rest/rbac.rs` (maps paths → `admin_rpc_methods()`) | Off by default; separate bind (default **8080** / **18080**). See [RPC API — REST](../node/rpc-api.md#rest-api). |

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
