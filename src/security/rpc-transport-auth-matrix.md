# RPC transport × authentication matrix

Operator reference for **which JSON-RPC surface supports which auth model**. P2P transport comparison (**TCP vs QUIC**) lives under **[Transport abstraction](../node/transport-abstraction.md)**: different scope.

## Matrix

<div class="locks">
<section>
<p class="lock-name">JSON-RPC (TCP HTTP)</p>
<p>Default <code>blvm</code> RPC.</p>
<p><strong>Bearer</strong> (<code>[rpc_auth]</code>). Yes: <code>Authorization: Bearer</code>.</p>
<p><strong>HTTP Basic.</strong> Yes: <code>Authorization: Basic</code> (ckpool; password auto-admin).</p>
<p><strong>TLS client certs.</strong> When configured.</p>
<p class="lock-where">Prefer loopback for Basic (cleartext on wire).</p>
</section>
<section>
<p class="lock-name">JSON-RPC (QUIC HTTP/3)</p>
<p><code>quinn</code> listener; ALPN <code>h3</code>.</p>
<p><strong>Bearer</strong> (<code>[rpc_auth]</code>). Yes: same <code>RpcAuthManager</code> as TCP.</p>
<p><strong>HTTP Basic.</strong> Yes: HTTP/3 request headers.</p>
<p><strong>TLS client certs.</strong> Server TLS on the UDP listener.</p>
<p class="lock-where">Shares live <code>Arc&lt;RpcServer&gt;</code> with TCP HTTP. UDP TLS cert lifecycle may differ from TCP unless you terminate at a proxy.</p>
</section>
<section>
<p class="lock-name">REST (<code>/api/v1/</code>)</p>
<p><code>rest-api</code> feature; <code>[rest_api].enabled</code>.</p>
<p><strong>Bearer</strong> (<code>[rpc_auth]</code>). Yes: when the REST server is built <code>with_auth</code>.</p>
<p><strong>HTTP Basic.</strong> Same auth stack; admin RBAC via <code>rest/rbac.rs</code>.</p>
<p><strong>TLS client certs.</strong> Off by default.</p>
<p class="lock-where">Separate bind (default 8080 / 18080 / 28443). See <a href="../node/rpc-api.html#rest-api">RPC API: REST</a>.</p>
</section>
</div>

## Practical guidance

- **Strict RPC auth (`rpc_auth.required = true`):** Bearer and HTTP Basic enforcement apply on **both** TCP HTTP JSON-RPC and **HTTP/3 JSON-RPC over QUIC**: configure **`[rpc_auth]`** once; semantics match (**same **`RpcAuthManager`**, shared **`dispatch_json_rpc_post_body`** path). Mining pools (ckpool) typically use **Basic** on loopback.
- **QUIC JSON-RPC:** Requires an HTTP/3-capable client (QUIC + ALPN **`h3`**). **[Deployment posture](deployment-posture.md)** still governs exposure class (UDP firewall rules differ from TCP).
- **Non-loopback RPC:** Same posture doc + **[First node](../getting-started/first-node.md)** production notes.

## Historical note (**G2.3**, QUIC × strict auth)

Earlier builds exposed JSON-RPC on QUIC **without** HTTP headers and therefore **skipped** the QUIC RPC listener when **`rpc_auth.required`** was **`true`**. Current **`quinn`** RPC uses **HTTP/3**, so **`Authorization`** and rate limits match TCP HTTP. Proxy / mutual-TLS termination remains deployment-specific.

## Source anchors

- QUIC RPC + **`Arc<RpcServer>`**: `blvm-node/src/rpc/mod.rs`, `blvm-node/src/rpc/quinn_server.rs`.
- Shared POST dispatch: `blvm-node/src/rpc/server.rs` (`dispatch_json_rpc_post_body`).
- **`RpcAuthConfig::default()`**: `required: false`: local-dev friendly; tighten for LAN/WAN.
