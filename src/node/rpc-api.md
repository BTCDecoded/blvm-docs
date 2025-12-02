# RPC API Reference

BLLVM node provides a JSON-RPC 2.0 interface for interacting with the node.

## Connection

Default RPC endpoint: `http://localhost:8332`

## Authentication

For production use, configure RPC authentication:

```toml
[rpc]
enabled = true
username = "rpcuser"
password = "rpcpassword"
```

## Example Requests

### Get Blockchain Info

```bash
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
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "getnetworkinfo",
    "params": [],
    "id": 1
  }'
```

## Available Methods

**Total Methods Implemented: 28**

### Blockchain Methods (8 methods)
- `getblockchaininfo` - Get blockchain information
- `getblock` - Get block by hash
- `getblockhash` - Get block hash by height
- `getblockheader` - Get block header by hash
- `getbestblockhash` - Get best block hash
- `getblockcount` - Get current block height
- `getdifficulty` - Get current difficulty
- `gettxoutsetinfo` - Get UTXO set statistics
- `verifychain` - Verify blockchain database

### Raw Transaction Methods (7 methods)
- `getrawtransaction` - Get transaction by txid
- `sendrawtransaction` - Submit transaction to mempool
- `testmempoolaccept` - Test if transaction would be accepted
- `decoderawtransaction` - Decode raw transaction hex
- `gettxout` - Get UTXO information
- `gettxoutproof` - Get merkle proof for transaction
- `verifytxoutproof` - Verify merkle proof

### Mempool Methods (3 methods)
- `getmempoolinfo` - Get mempool statistics
- `getrawmempool` - List transactions in mempool
- `savemempool` - Persist mempool to disk

### Network Methods (9 methods)
- `getnetworkinfo` - Get network information
- `getpeerinfo` - Get connected peers
- `getconnectioncount` - Get number of connections
- `ping` - Ping connected peers
- `addnode` - Add/remove node from peer list
- `disconnectnode` - Disconnect specific node
- `getnettotals` - Get network statistics
- `clearbanned` - Clear banned nodes
- `setban` - Ban/unban a subnet
- `listbanned` - List banned nodes

### Mining Methods (4 methods)
- `getmininginfo` - Get mining information
- `getblocktemplate` - Get block template for mining
- `submitblock` - Submit a mined block
- `estimatesmartfee` - Estimate smart fee rate

## Error Codes

The RPC API uses Bitcoin Core-compatible JSON-RPC 2.0 error codes:

### Standard JSON-RPC Errors

| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse error | Invalid JSON was received |
| -32600 | Invalid Request | The JSON sent is not a valid Request object |
| -32601 | Method not found | The method does not exist |
| -32602 | Invalid params | Invalid method parameter(s) |
| -32603 | Internal error | Internal JSON-RPC error |

### Bitcoin-Specific Errors

| Code | Name | Description |
|------|------|-------------|
| -1 | Transaction already in chain | Transaction is already in blockchain |
| -1 | Transaction missing inputs | Transaction references non-existent inputs |
| -5 | Block not found | Block hash not found |
| -5 | Transaction not found | Transaction hash not found |
| -5 | UTXO not found | UTXO does not exist |
| -25 | Transaction rejected | Transaction rejected by consensus rules |
| -27 | Transaction already in mempool | Transaction already in mempool |

**Code**: ```9:78:bllvm-node/src/rpc/errors.rs```

### Error Response Format

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

**Code**: ```432:450:bllvm-node/src/rpc/errors.rs```

## Authentication

RPC authentication is optional but recommended for production:

### Token-Based Authentication

```bash
curl -X POST http://localhost:8332 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1}'
```

### Certificate-Based Authentication

TLS client certificates can be used for authentication when QUIC transport is enabled.

**Code**: ```1:100:bllvm-node/src/rpc/auth.rs```

## Rate Limiting

Rate limiting is enforced per IP, per user, and per method:

- **Authenticated users**: 100 burst, 10 req/sec
- **Unauthenticated**: 50 burst, 5 req/sec
- **Per-method limits**: May override defaults for specific methods

**Code**: ```1:100:bllvm-node/src/rpc/server.rs```

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

**Code**: ```16:45:bllvm-node/src/rpc/types.rs```

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

{{#include ../../../modules/bllvm-node/docs/status/RPC_IMPLEMENTATION_STATUS.md}}

