# RPC API Reference

BLVM node provides both a JSON-RPC 2.0 interface (conventional Bitcoin RPC surface) and a modern REST API for interacting with the node.

**On this page:** [API Overview](#api-overview) · [Connection](#connection) · [Authentication](#authentication) · [Methods operators use most](#methods-operators-use-most) · [Core parity matrix](#bitcoin-core-rpc-parity-selected) · [Available Methods](#available-methods) · [Errors](#error-codes) · [REST API](#rest-api)

## API Overview

- **JSON-RPC 2.0**: Methods aligned with widely documented Bitcoin node RPC docs. The **`blvm`** binary binds JSON-RPC to **`--rpc-addr`** / **`BLVM_RPC_ADDR`**. When omitted, RPC is **network-aware**: mainnet **`127.0.0.1:8332`**, testnet **`127.0.0.1:18332`**, regtest **`127.0.0.1:18443`** (Core-aligned).
- **REST API** (optional): Requires **`rest-api`** feature and **`[rest_api].enabled = true`** in `blvm.toml`. Binds a separate port (default **8080** when RPC is **8332**, **18080** when RPC is **18332**, otherwise RPC port **+ 10000**). See [REST API](#rest-api).

## Connection

Use the same **host:port** you configure as **`--rpc-addr`** / **`BLVM_RPC_ADDR`**. Defaults: mainnet `http://127.0.0.1:8332`, testnet `http://127.0.0.1:18332`, regtest `http://127.0.0.1:18443`. There is no separate RPC `port` key in **`NodeConfig`**. See [Node Configuration](configuration.md).

## Authentication

Configure RPC authentication with **`[rpc_auth]`**. Two common patterns:

**Bearer tokens** (wallets, automation):

```toml
[rpc_auth]
required = true
tokens = ["your-long-random-token"]
admin_tokens = ["admin-token-for-mining-rpcs"]  # optional; mining/destructive methods
```

Pass `Authorization: Bearer <token>` on each request. Tokens in `tokens` alone are **read-only** unless also listed in `admin_tokens`.

**HTTP Basic** (ckpool, Bitcoin Core–style tools, `curl -u`):

```toml
[rpc_auth]
required = true
username = "ckpool"
password = "your-long-random-secret"
```

The password is registered as **admin** automatically (required for `getblocktemplate` / `submitblock`). Bind RPC to **loopback** (`--rpc-addr 127.0.0.1:8332`) — Basic auth is cleartext on the wire.

Optional: `token_file`, `certificates`, `RPC_AUTH_TOKENS`. **`[rpc]`** in `NodeConfig` is only for **limits / rate limits**, not credentials.

**TLS client certificates** are supported when QUIC transport and certificate fingerprints are configured (`certificates` in `[rpc_auth]`).

See **[RPC transport × authentication](../security/rpc-transport-auth-matrix.md)** and **[Deployment posture](../security/deployment-posture.md)**.

## Example Requests

### Get Blockchain Info

```bash
# Mainnet 8332; testnet 18332; regtest 18443
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "getblockchaininfo",
    "params": [],
    "id": 1
  }'
```

### Get Block

```bash
# Mainnet 8332; testnet 18332; regtest 18443
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "getblock",
    "params": ["000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"],
    "id": 1
  }'
```

### Get Network Info

```bash
# Mainnet 8332; testnet 18332; regtest 18443
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "getnetworkinfo",
    "params": [],
    "id": 1
  }'
```

## Methods operators use most

Fifteen RPC methods cover most operator, wallet, and mining workflows. Full catalog: [Available Methods](#available-methods) below.

| Method | Purpose |
|--------|---------|
| `getblockchaininfo` | Chain, height, sync status |
| `getnetworkinfo` | P2P connections, protocol version |
| `getpeerinfo` | Per-peer details |
| `getrawtransaction` | Fetch tx by txid (with index when enabled) |
| `sendrawtransaction` | Broadcast signed tx to mempool |
| `testmempoolaccept` | Dry-run mempool acceptance |
| `getmempoolinfo` | Mempool size and limits |
| `getrawmempool` | List mempool txids |
| `validateaddress` | Decode / validate an address |
| `getblocktemplate` | Mining template (admin auth) |
| `submitblock` | Submit mined block (admin auth) |
| `getmininginfo` | Mining / chain mining state |
| `estimatesmartfee` | Fee estimation |
| `stop` | Stop the node (admin) |
| `uptime` | Node uptime seconds |

### `getblockchaininfo` (example response fields)

```json
{
  "chain": "regtest",
  "blocks": 1,
  "headers": 1,
  "bestblockhash": "...",
  "difficulty": 1.0,
  "chainwork": "...",
  "pruned": false
}
```

On regtest at genesis, `"blocks": 0`, `"difficulty": 1.0`, and `"initialblockdownload": true` are typical.

### `sendrawtransaction`

Submit hex-encoded signed transaction. Returns txid on success; errors if policy or consensus rejects the tx.

```bash
# Testnet example (18332); regtest uses 18443, mainnet 8332
curl -X POST http://127.0.0.1:18332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"sendrawtransaction","params":["<hex>"],"id":1}'
```

Requires valid auth when `[rpc_auth].required = true`.

## Bitcoin Core RPC parity (selected)

BLVM targets **common Bitcoin Core JSON-RPC** shapes for interoperability (ckpool, scripts, wallets). This is not a complete Core parity audit — verify critical paths for your deployment.

| Method | Core parity | Notes |
|--------|-------------|-------|
| `getblockchaininfo` | High | Standard fields; network names align with BLVM networks |
| `getblock` / `getblockheader` | High | Verbosity levels supported |
| `getrawtransaction` | High | Needs tx index or mempool/chain lookup context |
| `sendrawtransaction` | High | Standard policy + relay |
| `testmempoolaccept` | High | Multiple-tx batch where implemented |
| `getmempoolinfo` / `getrawmempool` | High | |
| `getnetworkinfo` / `getpeerinfo` | High | |
| `validateaddress` | High | |
| `getblocktemplate` | High | ckpool / Stratum workflows |
| `submitblock` | High | Mining submission |
| `generatetoaddress` | Regtest only | Not on mainnet; requires protocol engine |
| `savemempool` | Partial | Writes `mempool.dat` under datadir |
| `verifyonchainpayment` / `verifyonchainpaymentbytx` | BLVM-specific | BIP70 / payment state machine |
| `meshsendpacket` / `meshpollreceived` | Module | Requires `blvm-mesh` |
| REST `/api/v1/*` | BLVM-specific | `rest-api` feature + `[rest_api].enabled`; separate bind — see [REST API](#rest-api) |

**Ports:** BLVM defaults RPC to **`18332`** (testnet) and **`18443`** (regtest, Core-aligned). Set **`--rpc-addr`** / **`BLVM_RPC_ADDR`** when you need a different bind.

## Available Methods

**Core JSON-RPC:** **75** methods in `CORE_RPC_METHODS` (see `blvm-node/src/rpc/methods.rs`). Module RPC (mesh, miniscript overrides, etc.) registers at runtime.

### Blockchain Methods

| Method | Description |
|--------|-------------|
| `getblockchaininfo` | Chain, height, IBD flag, best block |
| `getblock` | Block by hash (verbosity levels) |
| `getblockhash` | Hash at height |
| `getblockheader` | Header by hash |
| `getbestblockhash` | Best block hash |
| `getblockcount` | Current height |
| `getdifficulty` | Current difficulty |
| `gettxoutsetinfo` | UTXO set statistics |
| `verifychain` | Verify blockchain database |
| `getblockfilter` | Block filter (BIP158) |
| `getindexinfo` | Index status |
| `getblockchainstate` | Extended chain state |
| `invalidateblock` / `reconsiderblock` | Mark block invalid / reconsider |
| `waitfornewblock` / `waitforblock` / `waitforblockheight` | Block wait helpers |
| `getchaintips` | All known tips |
| `getchaintxstats` | Confirmed tx statistics to height |
| `getblockstats` | Per-block fees, sizes, counts |
| `getpruneinfo` | Pruning state |
| `pruneblockchain` | Prune to height (**admin**) |
| `loadtxoutset` | Load UTXO snapshot from file |

### Raw Transaction Methods

| Method | Description |
|--------|-------------|
| `getrawtransaction` | Transaction by txid |
| `sendrawtransaction` | Submit to mempool |
| `testmempoolaccept` | Policy / consensus dry-run |
| `decoderawtransaction` / `createrawtransaction` | Decode / build raw hex |
| `gettxout` | UTXO by outpoint |
| `gettxoutproof` / `verifytxoutproof` | Merkle proof |
| `getdescriptorinfo` | Descriptor metadata (**needs `blvm-miniscript`**) |
| `analyzepsbt` | PSBT analysis (**needs `blvm-miniscript`**) |

### Mempool Methods

| Method | Description |
|--------|-------------|
| `getmempoolinfo` | Mempool statistics |
| `getrawmempool` | Txids or verbose entries |
| `savemempool` | Write `{datadir}/mempool.dat` |
| `getmempoolancestors` / `getmempooldescendants` | Dependency graph |
| `getmempoolentry` | Single mempool entry |

### Network Methods

| Method | Description |
|--------|-------------|
| `getnetworkinfo` | Network and client info |
| `getpeerinfo` / `getconnectioncount` | Peers |
| `ping` | Ping peers |
| `addnode` / `disconnectnode` | Manual peer control |
| `getnettotals` | Traffic totals |
| `setban` / `listbanned` / `clearbanned` | Ban management |
| `getaddednodeinfo` / `getnodeaddresses` | Manual / addrman entries |
| `setnetworkactive` | Enable/disable P2P |

### Mining Methods

| Method | Description |
|--------|-------------|
| `getmininginfo` | Mining status |
| `getblocktemplate` | Block template (**admin**; ckpool) |
| `submitblock` | Submit solved block (**admin**) |
| `estimatesmartfee` | Fee estimate |
| `prioritisetransaction` | Mempool priority (**admin**) |
| `generatetoaddress` | Regtest mine to address (**admin**, regtest only) |

### Module Methods

| Method | Description |
|--------|-------------|
| `loadmodule` / `unloadmodule` / `reloadmodule` | Lifecycle (**admin**) |
| `listmodules` | Loaded modules |
| `getmoduleclispecs` / `runmodulecli` | Module CLI via RPC (**admin**) |

Dynamic module RPC (mesh, miniscript overrides, …) registers at load time. See module pages and [JSON-RPC error reference](../reference/rpc-errors.md#module-not-loaded).

### Control Methods

| Method | Description |
|--------|-------------|
| `stop` | Graceful shutdown (**admin**) |
| `uptime` | Process uptime |
| `getmemoryinfo` | Memory stats |
| `getrpcinfo` | RPC server info |
| `help` / `logging` | Help and log levels |
| `gethealth` / `getmetrics` | **blvm-node** extensions (not Core) |

### Mesh Methods

**Requires `blvm-mesh` loaded.**

| Method | Description |
|--------|-------------|
| `meshsendpacket` | Send mesh payload (hex bincode) |
| `meshpollreceived` | Poll delivered packets |
| `meshquoteroute` | Quote route cost |
| `meshrequesthopinvoice` | Hop invoice for routing |

See [Commons Mesh Module](../modules/mesh.md).

### Address Methods

| Method | Description |
|--------|-------------|
| `validateaddress` | Address validity |
| `getaddressinfo` | Detailed address info |

### Transaction Methods

| Method | Description |
|--------|-------------|
| `gettransactiondetails` | Extended transaction view |

### Payment Methods (BIP70)

> **Build / platform** — `bip70-http` requires full `blvm` features; portable Windows/aarch64 CI builds omit it. `ctv` is a separate compile-time feature. See [Installation](../getting-started/installation.md).

| Method | Description |
|--------|-------------|
| `createpaymentrequest` | BIP70 payment request (`bip70-http`) |
| `verifyonchainpayment` / `verifyonchainpaymentbytx` | On-chain payment verification |
| `verifycovenantproof` | Covenant proof (`ctv` feature) |

**Source of truth:** `blvm-node/src/rpc/methods.rs` (`CORE_RPC_METHODS`).

## Error Codes

BLVM uses standard JSON-RPC 2.0 codes, Bitcoin-style application codes (**-1**, **-5**, **-25**, **-27**), BLVM server codes (**-32001**), and HTTP **401/403/429** for auth, admin RBAC, and rate limits.

**Full catalog:** [JSON-RPC error reference](../reference/rpc-errors.md) — every code, `error.data` fields, admin-only methods, and transport vs JSON-RPC shapes.

### Quick reference

| Code | Meaning |
|------|---------|
| -32700 … -32603 | JSON-RPC protocol errors |
| -1 | Tx already in chain **or** missing inputs (read `message`) |
| -5 | Block, transaction, or UTXO not found |
| -25 | Transaction rejected (policy / consensus / fee) |
| -27 | Transaction already in mempool |
| -32001 | Method requires unloaded module (e.g. miniscript) |
| HTTP 401 / 403 / 429 | Auth failure, non-admin privileged method, or rate limit |

### Example JSON-RPC error

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "param": "blockhash",
      "reason": "Invalid hex string"
    }
  },
  "id": 1
}
```

## Rate Limiting

Rate limiting is enforced per IP, per user, and per method:

- **Authenticated users**: 100 burst, 10 req/sec
- **Unauthenticated**: 50 burst, 5 req/sec
- **Per-method limits**: May override defaults for specific methods


## Request/Response Format

### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "getblockchaininfo",
  "params": [],
  "id": 1
}
```

### Response Format

**Success Response**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "chain": "regtest",
    "blocks": 123456,
    "headers": 123456,
    "bestblockhash": "0000...",
    "difficulty": 4.656542373906925e-10
  },
  "id": 1
}
```

**Error Response**:
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params"
  },
  "id": 1
}
```


## Batch Requests

Multiple requests can be sent in a single batch:

```json
[
  {"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1},
  {"jsonrpc": "2.0", "method": "getblockhash", "params": [100], "id": 2},
  {"jsonrpc": "2.0", "method": "getblock", "params": ["0000..."], "id": 3}
]
```

Responses are returned in the same order as requests.

## Implementation Status

The RPC API implements JSON-RPC 2.0 methods documented in the [Available Methods](#available-methods) section above.

## REST API

### Overview

The REST API is a **separate HTTP server** from JSON-RPC (`blvm-node/src/rpc/rest/`). It requires the **`rest-api`** compile-time feature (included in **`blvm` default features**; omitted from portable Windows/aarch64 release builds).

> **Operator note** — REST is **off by default** (`[rest_api].enabled = false`). When enabled, it binds its **own** address (default loopback **8080** / **18080** from RPC port). Handler coverage matches **`rest/server.rs` routing**, not every function in `rest/*.rs`.

When enabled programmatically, REST binds its **own** address (tests use `127.0.0.1:8080`). It does **not** share the JSON-RPC port (**8332** / **18332** / **18443**). HTTP **`GET /health`** on the RPC port is separate (see [Node Operations](operations.md)).

**Base URL (when running):** `http://<rest-bind>/api/v1/`

### Authentication

Same **`RpcAuthConfig`** / **`RpcAuthManager`** as JSON-RPC when the REST server is built with **`RestServer::with_auth(...)`** (Bearer tokens, HTTP Basic, admin tokens). If auth is **enabled** on that instance, unauthenticated requests receive **401 Unauthorized** before route handlers run — same guard as JSON-RPC. When auth is **disabled**, REST accepts anonymous requests (still subject to per-IP rate limits). Embedders must call **`with_auth`** explicitly; default test servers may run without it.

**Admin RBAC** mirrors JSON-RPC **`admin_rpc_methods()`** via `rest/rbac.rs`: each REST path maps to an equivalent RPC method; privileged routes return **403 Forbidden** for authenticated non-admin tokens. Examples: `GET /api/v1/mining/block-template`, `POST /api/v1/node/stop`, `POST /api/v1/transactions`. Non-admin POST routes include `POST /api/v1/transactions/decode`, `…/test`, `POST /api/v1/chain/verify`, and `POST /api/v1/network/ping`. Unmapped POST/DELETE paths (e.g. payment writes) **fail closed** (admin required).

### Endpoints (wired in `rest/server.rs`)

#### Chain

- `GET /api/v1/chain/tip` — Best block hash
- `GET /api/v1/chain/height` — Block height
- `GET /api/v1/chain/info` — Blockchain state summary
- `GET /api/v1/chain/difficulty` — Current difficulty
- `GET /api/v1/chain/utxo-set` — UTXO set summary
- `GET /api/v1/chain/tips` — Known chain tips
- `GET /api/v1/chain/tx-stats?nblocks={n}` — Transaction statistics
- `GET /api/v1/chain/prune-info` — Pruning status
- `POST /api/v1/chain/verify` — Verify chain (optional JSON: `checklevel`, `numblocks`)
- `POST /api/v1/chain/prune` — Prune to height (JSON: `height`)

#### Indexes

- `GET /api/v1/indexes` — Index status (optional `?index={name}`)

#### Blocks

- `GET /api/v1/blocks/{hash}` — Block by hash
- `GET /api/v1/blocks/{hash}/header` — Block header
- `GET /api/v1/blocks/{hash}/stats` — Block statistics
- `GET /api/v1/blocks/{hash}/filter` — Block filter
- `GET /api/v1/blocks/{hash}/transactions` — Block transactions
- `GET /api/v1/blocks/height/{height}` — Block by height
- `POST /api/v1/blocks/{hash}/invalidate` — Invalidate block (admin)
- `POST /api/v1/blocks/{hash}/reconsider` — Reconsider block (admin)

#### Transactions

- `GET /api/v1/transactions/{txid}` — Transaction details
- `GET /api/v1/transactions/{txid}/confirmations`
- `GET /api/v1/transactions/{txid}/outputs/{n}?include_mempool=true` — Output details
- `POST /api/v1/transactions` — Submit raw hex (body)
- `POST /api/v1/transactions/test` — Test mempool acceptance
- `POST /api/v1/transactions/decode` — Decode raw hex
- `POST /api/v1/transactions/create` — Create raw tx (JSON: `inputs`, `outputs`, optional `locktime`, `replaceable`, `version`)

#### Addresses

- `GET /api/v1/addresses/{address}/balance`
- `GET /api/v1/addresses/{address}/transactions`
- `GET /api/v1/addresses/{address}/utxos`

#### Mempool

- `GET /api/v1/mempool` — List txids (`verbose` via query where supported)
- `GET /api/v1/mempool/transactions/{txid}` — Mempool entry
- `GET /api/v1/mempool/transactions/{txid}/ancestors` — Ancestor txids
- `GET /api/v1/mempool/transactions/{txid}/descendants` — Descendant txids
- `GET /api/v1/mempool/stats` — Mempool info (maps to `getmempoolinfo`)
- `POST /api/v1/mempool/save` — Persist mempool to disk
- `POST /api/v1/mempool/transactions/{txid}/priority` — Adjust effective fee (JSON: `fee_delta`; admin; maps to `prioritisetransaction`)

#### Network

- `GET /api/v1/network/info`
- `GET /api/v1/network/peers`
- `GET /api/v1/network/connections/count`
- `GET /api/v1/network/connections/totals`
- `GET /api/v1/network/nodes` — Known nodes
- `GET /api/v1/network/addresses` — Network addresses
- `GET /api/v1/network/bans` — Ban list
- `POST /api/v1/network/ping` — Ping peers
- `POST /api/v1/network/nodes` — Add/remove node (JSON: `address`, `command`)
- `POST /api/v1/network/active` — Set network active (JSON: `state`)
- `POST /api/v1/network/bans` — Ban subnet (JSON body)
- `DELETE /api/v1/network/nodes/{addr}` — Disconnect node
- `DELETE /api/v1/network/bans/{subnet}` — Remove ban

#### Node

- `GET /api/v1/node/uptime`
- `GET /api/v1/node/memory`
- `GET /api/v1/node/rpc-info`
- `GET /api/v1/node/help?command={name}`
- `GET /api/v1/node/logging`
- `POST /api/v1/node/stop` — Stop node (admin)
- `POST /api/v1/node/logging` — Set logging categories (JSON body)

#### Mining

- `GET /api/v1/mining/info`
- `GET /api/v1/mining/block-template`
- `POST /api/v1/mining/blocks` — Submit block (JSON body)

#### Fees

- `GET /api/v1/fees/estimate?blocks=6` — Smart fee estimate (default 6 blocks)

#### Payment / CTV (`bip70-http`, `ctv`)

When the REST server is running **and** payment state is configured:

- `GET|POST /api/v1/payments` — List / create payment requests
- `GET /api/v1/payments/{id}` — Payment state
- `POST /api/v1/payments/{id}/covenant` — CTV covenant proof (`ctv` feature)
- Vault: `POST /api/v1/vaults`, `GET /api/v1/vaults/{id}`, `POST …/unvault`, `POST …/withdraw`
- Pool: `POST /api/v1/pools`, `GET /api/v1/pools/{id}`, `POST …/join`, `POST …/distribute`
- Batch: `POST /api/v1/batches`, `GET /api/v1/batches/{id}`, `POST …/transactions`, `POST …/broadcast`
- `GET /api/v1/congestion` — Congestion metrics

Legacy BIP70 HTTP also registers under `/api/v1/payment/*` when `bip70-http` is enabled.

### Response format

Success and error envelopes use `ApiResponse` (`status`, `data` / `error`, `request_id`). See `rest/types.rs`.

### Error codes

Standard HTTP status codes: 200, 400, 401, 404, 429, 500, 503 (feature or payment engine unavailable).

## Source

- [auth.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/auth.rs)
- [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/server.rs)
- [types.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/types.rs)
- [rest/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/mod.rs)
- [rest/server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/server.rs)
- [rest/types.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/types.rs)
- [rest/node.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/node.rs)
- [rest/blocks.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/blocks.rs)
- [rest/network.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/network.rs)
- [rest/payment.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/payment.rs)
- [rest/vault.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/vault.rs)
- [rest/pool.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/pool.rs)
- [rest/congestion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/congestion.rs)
## See Also

- [Node Overview](overview.md) - Node implementation details
- [Node Configuration](configuration.md) - RPC configuration options
- [JSON-RPC error reference](../reference/rpc-errors.md) - Error codes and HTTP auth failures
- [Node Operations](operations.md) - Node management
- [Getting Started](../getting-started/quick-start.md) - Quick start guide
- [API Index](../reference/api-index.md) - Cross-reference to all APIs
- [Troubleshooting](../appendices/troubleshooting.md) - Common RPC issues
- [Commons Mesh Module](../modules/mesh.md) - Payment endpoints and mesh networking
- [Module System](../architecture/module-system.md) - Module architecture and IPC
