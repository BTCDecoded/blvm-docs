# RPC transport × authentication matrix

Operator reference for **which JSON-RPC surface supports which auth model**. P2P transport comparison (**TCP vs QUIC**) lives under **[Transport abstraction](../node/transport-abstraction.md)** — different scope.

## Matrix

| Surface | Feature / bind | Bearer / token auth (`[rpc_auth]`) | TLS client certs | Notes |
|---------|----------------|--------------------------------------|------------------|--------|
| **JSON-RPC over TCP (HTTP)** | Default **`blvm`** RPC | **Supported** — **`Authorization: Bearer`** | **Supported** (when configured) | Primary interoperable path for authenticated RPC. |
| **JSON-RPC over QUIC (HTTP/3)** | **`quinn`** QUIC RPC listener | **Supported** — same **`RpcAuthManager`** as TCP HTTP; send **`Authorization: Bearer`** on HTTP/3 request headers | QUIC presents a server TLS identity on the UDP listener (**distinct certificate lifecycle** from TCP HTTP TLS unless you terminate equivalently at a proxy) | **ALPN `h3`**. **POST** with **`Content-Type: application/json`** and the same JSON-RPC body as TCP HTTP. Shares the live **`Arc<RpcServer>`** so handlers and limits align with TCP HTTP. |
| **REST (`/api/v1/`)** | **`rest-api`** feature | **Supported** via shared **`RpcAuthManager`** when REST server built **`with_auth`** | Same stack as RPC auth layer | REST ships alongside JSON-RPC; enable **`rest-api`** and supply the same auth configuration patterns as RPC. |

## Practical guidance

- **Strict RPC auth (`rpc_auth.required = true`):** Bearer enforcement applies on **both** TCP HTTP JSON-RPC and **HTTP/3 JSON-RPC over QUIC** — configure **`[rpc_auth]`** once; semantics match (**same **`RpcAuthManager`**, shared **`dispatch_json_rpc_post_body`** path).
- **QUIC JSON-RPC:** Requires an HTTP/3-capable client (QUIC + ALPN **`h3`**). **[Deployment posture](deployment-posture.md)** still governs exposure class (UDP firewall rules differ from TCP).
- **Non-loopback RPC:** Same posture doc + **[First node](../getting-started/first-node.md)** production notes.

## Historical note (**G2.3**, QUIC × strict auth)

Earlier builds exposed JSON-RPC on QUIC **without** HTTP headers and therefore **skipped** the QUIC RPC listener when **`rpc_auth.required`** was **`true`**. Current **`quinn`** RPC uses **HTTP/3**, so **`Authorization`** and rate limits match TCP HTTP. Proxy / mutual-TLS termination remains deployment-specific.

## Source anchors

- QUIC RPC + **`Arc<RpcServer>`**: `blvm-node/src/rpc/mod.rs`, `blvm-node/src/rpc/quinn_server.rs`.
- Shared POST dispatch: `blvm-node/src/rpc/server.rs` (`dispatch_json_rpc_post_body`).
- **`RpcAuthConfig::default()`**: `required: false` — local-dev friendly; tighten for LAN/WAN.
