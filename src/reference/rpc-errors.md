# JSON-RPC error reference

Complete error catalog for the BLVM node JSON-RPC surface. Method parameters and examples: [RPC API Reference](../node/rpc-api.md).

**Source of truth:** [blvm-node/src/rpc/errors.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/errors.rs) (`RpcError`, `RpcErrorCode`).

## Two response shapes

### Successful JSON-RPC envelope

```json
{
 "jsonrpc": "2.0",
 "result": { ... },
 "id": 1
}
```

### JSON-RPC error envelope (handler / parse errors)

Returned when the request is valid JSON-RPC but the method handler fails (or JSON parse fails inside the RPC processor):

```json
{
 "jsonrpc": "2.0",
 "error": {
 "code": -32602,
 "message": "Invalid params",
 "data": { "parameter": "blockhash", "suggestions": ["..."] }
 },
 "id": 1
}
```

`data` is optional. BLVM helpers often populate `suggestions`, `txid`, `rejection_code`, or field-level `invalid_fields`.

### HTTP transport errors (auth, rate limits, size)

When authentication, RBAC, or rate limiting fails **before** JSON-RPC dispatch, the server returns an HTTP status with a **non-JSON-RPC** body:

```json
{
 "error": {
 "code": 401,
 "message": "Invalid authentication token"
 }
}
```

`error.code` is the **HTTP status number** (401, 403, 429, 413), not a JSON-RPC code. Clients must check HTTP status and this shape separately from JSON-RPC `error.code`.

| HTTP status | Typical cause |
|-------------|----------------|
| **401** | Missing/invalid Bearer or Basic credentials; auth failure tracker block |
| **403** | Authenticated but non-admin caller invoked an [admin-only method](#admin-only-methods) |
| **429** | User, IP, or per-method rate limit exceeded |
| **413** | Request body larger than configured max |

## Standard JSON-RPC 2.0 errors

| Code | Name | When |
|------|------|------|
| **-32700** | Parse error | Request body is not valid JSON |
| **-32600** | Invalid Request | JSON is not a valid JSON-RPC 2.0 request object |
| **-32601** | Method not found | Unknown method (core or module RPC not registered) |
| **-32602** | Invalid params | Bad parameter type, missing required param, invalid hex/address |
| **-32603** | Internal error | Unhandled server error; storage not initialized; unexpected handler failure |

### Common `-32602` helpers

| Helper | Typical message pattern | `data` hints |
|--------|-------------------------|--------------|
| `invalid_params` | Free-form message |: |
| `missing_parameter` | `Missing required parameter: {name}` | `parameter`, `expected_type`, `suggestions` |
| `invalid_hash_format` | `Invalid hash format: …` | `hash`, `expected_length`, `suggestions` |
| `invalid_address_format` | `Invalid address format: …` | `address`, `expected_format`, `suggestions` |
| `invalid_params_with_fields` | Custom message | `invalid_fields[]` with `field` + `reason` |

## Bitcoin-style application errors

Same numeric codes as common Bitcoin node RPC docs. **Disambiguate by `message`** when codes collide.

| Code | Enum / theme | Default message | Typical methods |
|------|----------------|-----------------|-----------------|
| **-1** | `TxAlreadyInChain` | Transaction already in block chain | `sendrawtransaction`, `testmempoolaccept` |
| **-1** | `TxMissingInputs` | Missing inputs | `sendrawtransaction` (unknown prevouts) |
| **-5** | `BlockNotFound` | Block not found | `getblock`, `getblockheader`, `invalidateblock`, … |
| **-5** | `TxNotFound` | Transaction not found | `getrawtransaction`, `getmempoolentry` |
| **-5** | `UtxoNotFound` | No such UTXO | `gettxout` |
| **-25** | `TxRejected` | Transaction rejected | `sendrawtransaction`, consensus/policy rejection |
| **-27** | `TxAlreadyInMempool` | Transaction already in mempool | `sendrawtransaction` |

### `-25` transaction rejected details

`tx_rejected`, `tx_rejected_with_context`, and `tx_rejected_insufficient_fee` may include:

| `data` field | Meaning |
|--------------|---------|
| `txid` | Transaction hash |
| `rejection_code` | Short machine-oriented code |
| `details` | Structured rejection context |
| `reason` | e.g. `insufficient_fee` |
| `required_fee_rate` / `provided_fee_rate` | sat/vB comparison |
| `required_fee_satoshis` / `provided_fee_satoshis` | Absolute fee comparison |
| `suggestions` | Human-readable remediation hints |

Consensus failures from `blvm_protocol::ConsensusError` map to **-25** with message prefix `Consensus error:`.

## BLVM server errors (-32000 to -32099)

Reserved JSON-RPC server error range.

| Code | When |
|------|------|
| **-32001** | Method needs a module that is not loaded (e.g. `getdescriptorinfo`, `analyzepsbt` → load `blvm-miniscript`) |

Message pattern: `Method '{method}' requires the blvm-miniscript module to be loaded. Load it with: loadmodule "blvm-miniscript"`

Other `ServerError(n)` codes may appear as the implementation grows; treat unknown negatives in this band as server/configuration errors.

## Internal errors operators see often

| Message | Cause | Fix |
|---------|-------|-----|
| `Storage not available. This operation requires storage to be initialized.` | Handler called before storage is ready | Wait for node startup / sync; check datadir permissions |
| `Tip block not found` | Chain tip missing in store | Corrupt or empty datadir; re-sync |
| `Height parameter required` / `Block hash parameter required` | Missing RPC param | Pass required argument |
| `Payment RPC not available` | Payment feature not built or wired | Build with required features or use supported verify methods |

## Admin-only methods

Authenticated callers without **admin** credentials receive **HTTP 403** (not JSON-RPC -32603):

`stop`, `loadmodule`, `unloadmodule`, `reloadmodule`, `runmodulecli`, `logging`, `invalidateblock`, `reconsiderblock`, `pruneblockchain`, `addnode`, `disconnectnode`, `setban`, `clearbanned`, `setnetworkactive`, `getblocktemplate`, `submitblock`, `generatetoaddress`, `sendrawtransaction`, `createrawtransaction`, `savemempool`, `prioritisetransaction`.

REST **`/api/v1/*`** privileged routes use the same admin set via path→method mapping (`rest/rbac.rs`). See [RPC API: REST authentication](../node/rpc-api.md#authentication).

Admin tokens: `[rpc_auth].admin_tokens`, tokens also listed in `admin_tokens`, or HTTP Basic password registered as admin. See [RPC transport × authentication](../security/rpc-transport-auth-matrix.md).

## Rate limiting defaults

When `[rpc_auth]` is enabled:

| Caller | Default bucket |
|--------|----------------|
| Authenticated user | 100 burst, 10 req/sec |
| Unauthenticated (per IP) | 50 burst, 5 req/sec |

Per-method and per-user overrides are configurable. Violations return **HTTP 429** with messages such as `User rate limit exceeded`, `IP rate limit exceeded`, or `Method '{name}' rate limit exceeded`.

## Errors by operation (quick lookup)

| Operation | Common errors |
|-----------|----------------|
| `sendrawtransaction` | **-27** already in mempool; **-1** in chain or missing inputs; **-25** policy/consensus/fee; **403** without admin token |
| `getrawtransaction` | **-5** not found; **-32602** bad txid hex |
| `getblock` / `getblockheader` | **-5** block not found; **-32602** bad hash or height |
| `gettxout` | **-5** no such UTXO |
| `getblocktemplate` / `submitblock` / `generatetoaddress` | **403** without admin; **-32603** if protocol engine unavailable |
| Unknown method | **-32601** |
| Module RPC (mesh, miniscript, …) | **-32601** if module not loaded; **-32001** for miniscript descriptor methods |

### Module RPC not loaded {#module-not-loaded}

Dynamic module methods (mesh, miniscript overrides, …) return **-32601** *Method not found* when the module is not loaded. Load the module with `loadmodule` before calling module RPCs.

## See Also

- [RPC API Reference](../node/rpc-api.md): methods, auth, examples
- [RPC transport × authentication](../security/rpc-transport-auth-matrix.md): Bearer, Basic, admin tokens
- [Deployment posture](../security/deployment-posture.md): production RPC exposure
- [Troubleshooting](../appendices/troubleshooting.md): operator fixes
