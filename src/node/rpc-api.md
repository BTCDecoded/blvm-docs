# RPC API Reference

BLVM node provides both a JSON-RPC 2.0 interface (Bitcoin Core compatible) and a modern REST API for interacting with the node.

## API Overview

- **JSON-RPC 2.0**: Bitcoin Core-compatible interface
  - Mainnet: `http://localhost:8332` (default)
  - Testnet/Regtest: `http://localhost:18332` (default)
- **REST API**: Modern RESTful interface at `http://localhost:8080/api/v1/`

Both APIs provide access to the same functionality, with the REST API offering better type safety, clearer error messages, and improved developer experience.

## Connection

Default RPC endpoints:
- Mainnet: `http://localhost:8332`
- Testnet/Regtest: `http://localhost:18332`

RPC ports are configurable. See [Node Configuration](configuration.md) for details.

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
# Mainnet uses port 8332, testnet/regtest use 18332
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
# Mainnet uses port 8332, testnet/regtest use 18332
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
# Mainnet uses port 8332, testnet/regtest use 18332
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

**Methods Implemented**: Multiple RPC methods

### Blockchain Methods
- `getblockchaininfo` - Get blockchain information
- `getblock` - Get block by hash
- `getblockhash` - Get block hash by height
- `getblockheader` - Get block header by hash
- `getbestblockhash` - Get best block hash
- `getblockcount` - Get current block height
- `getdifficulty` - Get current difficulty
- `gettxoutsetinfo` - Get UTXO set statistics
- `verifychain` - Verify blockchain database
- `getblockfilter` - Get block filter (BIP158)
- `getindexinfo` - Get index information
- `getblockchainstate` - Get blockchain state
- `invalidateblock` - Invalidate a block
- `reconsiderblock` - Reconsider a previously invalidated block
- `waitfornewblock` - Wait for a new block
- `waitforblock` - Wait for a specific block
- `waitforblockheight` - Wait for a specific block height

### Raw Transaction Methods
- `getrawtransaction` - Get transaction by txid
- `sendrawtransaction` - Submit transaction to mempool
- `testmempoolaccept` - Test if transaction would be accepted
- `decoderawtransaction` - Decode raw transaction hex
- `createrawtransaction` - Create a raw transaction
- `gettxout` - Get UTXO information
- `gettxoutproof` - Get merkle proof for transaction
- `verifytxoutproof` - Verify merkle proof

### Mempool Methods
- `getmempoolinfo` - Get mempool statistics
- `getrawmempool` - List transactions in mempool
- `savemempool` - Persist mempool to disk
- `getmempoolancestors` - Get mempool ancestors of a transaction
- `getmempooldescendants` - Get mempool descendants of a transaction
- `getmempoolentry` - Get mempool entry for a transaction

### Network Methods
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
- `getaddednodeinfo` - Get information about manually added nodes
- `getnodeaddresses` - Get known node addresses
- `setnetworkactive` - Enable or disable network activity

### Mining Methods
- `getmininginfo` - Get mining information
- `getblocktemplate` - Get block template for mining
- `submitblock` - Submit a mined block
- `estimatesmartfee` - Estimate smart fee rate
- `prioritisetransaction` - Prioritize a transaction in mempool

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

**Code**: [errors.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/errors.rs#L9-L78)

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

**Code**: [errors.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/errors.rs#L432-L450)

## Authentication

RPC authentication is optional but recommended for production:

### Token-Based Authentication

```bash
# Mainnet uses port 8332, testnet/regtest use 18332
curl -X POST http://localhost:8332 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1}'
```

### Certificate-Based Authentication

TLS client certificates can be used for authentication when QUIC transport is enabled.

**Code**: [auth.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/auth.rs#L1-L100)

## Rate Limiting

Rate limiting is enforced per IP, per user, and per method:

- **Authenticated users**: 100 burst, 10 req/sec
- **Unauthenticated**: 50 burst, 5 req/sec
- **Per-method limits**: May override defaults for specific methods

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/server.rs#L1-L100)

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

**Code**: [types.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/types.rs#L16-L45)

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

The RPC API implements Bitcoin Core-compatible JSON-RPC 2.0 methods. See the [Available Methods](#available-methods) section above for a complete list of implemented methods.

## REST API

### Overview

The REST API provides a modern, developer-friendly interface alongside the JSON-RPC API. It uses standard HTTP methods and status codes, with JSON request/response bodies.

**Base URL**: `http://localhost:8080/api/v1/`

**Code**: [rest/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/mod.rs#L1-L37)

### Authentication

REST API authentication works the same as JSON-RPC:

```bash
# Token-based authentication
curl -H "Authorization: Bearer <token>" http://localhost:8080/api/v1/node/uptime

# Basic authentication (if configured)
curl -u username:password http://localhost:8080/api/v1/node/uptime
```

### Rate Limiting

Rate limiting is enforced per IP, per user, and per endpoint:

- **Authenticated users**: 100 burst, 10 req/sec
- **Unauthenticated**: 50 burst, 5 req/sec
- **Per-endpoint limits**: Stricter limits for write operations

**Code**: [rest/server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/server.rs#L207-L256)

### Response Format

All REST API responses follow a consistent format:

**Success Response**:
```json
{
  "status": "success",
  "data": {
    "chain": "regtest",
    "blocks": 123456
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error Response**:
```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "Block not found",
    "details": "Block hash 0000... does not exist"
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Code**: [rest/types.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/types.rs)

### Endpoints

#### Node Endpoints

**Code**: [rest/node.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/node.rs#L1-L81)

- `GET /api/v1/node/uptime` - Get node uptime
- `GET /api/v1/node/memory` - Get memory information
- `GET /api/v1/node/memory?mode=detailed` - Get detailed memory info
- `GET /api/v1/node/rpc-info` - Get RPC server information
- `GET /api/v1/node/help` - Get help for all commands
- `GET /api/v1/node/help?command=getblock` - Get help for specific command
- `GET /api/v1/node/logging` - Get logging configuration
- `POST /api/v1/node/logging` - Update logging configuration
- `POST /api/v1/node/stop` - Stop the node

**Example**:
```bash
curl http://localhost:8080/api/v1/node/uptime
```

#### Chain Endpoints

- `GET /api/v1/chain/info` - Get blockchain information
- `GET /api/v1/chain/blockhash/{height}` - Get block hash by height
- `GET /api/v1/chain/blockcount` - Get current block height
- `GET /api/v1/chain/difficulty` - Get current difficulty
- `GET /api/v1/chain/txoutsetinfo` - Get UTXO set statistics
- `POST /api/v1/chain/verify` - Verify blockchain database

**Example**:
```bash
curl http://localhost:8080/api/v1/chain/info
```

#### Block Endpoints

**Code**: [rest/blocks.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/blocks.rs#L1-L91)

- `GET /api/v1/blocks/{hash}` - Get block by hash
- `GET /api/v1/blocks/{hash}/transactions` - Get block transactions
- `GET /api/v1/blocks/{hash}/header` - Get block header
- `GET /api/v1/blocks/{hash}/header?verbose=true` - Get verbose block header
- `GET /api/v1/blocks/{hash}/stats` - Get block statistics
- `GET /api/v1/blocks/{hash}/filter` - Get BIP158 block filter
- `GET /api/v1/blocks/{hash}/filter?filtertype=basic` - Get specific filter type
- `GET /api/v1/blocks/height/{height}` - Get block by height
- `POST /api/v1/blocks/{hash}/invalidate` - Invalidate block
- `POST /api/v1/blocks/{hash}/reconsider` - Reconsider invalidated block

**Example**:
```bash
curl http://localhost:8080/api/v1/blocks/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
```

#### Transaction Endpoints

- `GET /api/v1/transactions/{txid}` - Get transaction by txid
- `GET /api/v1/transactions/{txid}?verbose=true` - Get verbose transaction
- `POST /api/v1/transactions` - Submit raw transaction
- `POST /api/v1/transactions/test` - Test if transaction would be accepted
- `GET /api/v1/transactions/{txid}/out/{n}` - Get UTXO information

**Example**:
```bash
curl -X POST http://localhost:8080/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{"hex": "0100000001..."}'
```

#### Address Endpoints

- `GET /api/v1/addresses/{address}/balance` - Get address balance
- `GET /api/v1/addresses/{address}/transactions` - Get address transaction history
- `GET /api/v1/addresses/{address}/utxos` - Get address UTXOs

**Example**:
```bash
curl http://localhost:8080/api/v1/addresses/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa/balance
```

#### Mempool Endpoints

- `GET /api/v1/mempool/info` - Get mempool information
- `GET /api/v1/mempool/transactions` - List transactions in mempool
- `GET /api/v1/mempool/transactions?verbose=true` - List verbose transactions
- `POST /api/v1/mempool/save` - Persist mempool to disk

**Example**:
```bash
curl http://localhost:8080/api/v1/mempool/info
```

#### Network Endpoints

**Code**: [rest/network.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/network.rs#L1-L133)

- `GET /api/v1/network/info` - Get network information
- `GET /api/v1/network/peers` - Get connected peers
- `GET /api/v1/network/connections/count` - Get connection count
- `GET /api/v1/network/totals` - Get network statistics
- `GET /api/v1/network/nodes` - Get added node information
- `GET /api/v1/network/nodes?dns=true` - Get added nodes with DNS lookup
- `GET /api/v1/network/nodes/addresses` - Get node addresses
- `GET /api/v1/network/nodes/addresses?count=10` - Get N node addresses
- `GET /api/v1/network/bans` - List banned nodes
- `POST /api/v1/network/ping` - Ping connected peers
- `POST /api/v1/network/nodes` - Add node to peer list
- `POST /api/v1/network/active` - Activate node connection
- `POST /api/v1/network/bans` - Ban/unban a subnet
- `DELETE /api/v1/network/nodes/{address}` - Remove node from peer list
- `DELETE /api/v1/network/bans` - Clear all banned nodes

**Example**:
```bash
curl http://localhost:8080/api/v1/network/info
```

#### Fee Estimation Endpoints

- `GET /api/v1/fees/estimate` - Estimate fee rate
- `GET /api/v1/fees/estimate?blocks=6` - Estimate fee for N blocks
- `GET /api/v1/fees/smart` - Get smart fee estimate

**Example**:
```bash
curl http://localhost:8080/api/v1/fees/estimate?blocks=6
```

#### Payment Endpoints (BIP70 HTTP)

**Requires**: `--features bip70-http`

**Code**: [rest/payment.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/payment.rs)

- `GET /api/v1/payments/{payment_id}` - Get payment status
- `POST /api/v1/payments` - Create payment request
- `POST /api/v1/payments/{payment_id}/pay` - Submit payment
- `POST /api/v1/payments/{payment_id}/cancel` - Cancel payment

#### Vault Endpoints (CTV)

**Requires**: `--features ctv`

**Code**: [rest/vault.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/vault.rs)

- `GET /api/v1/vaults` - List vaults
- `GET /api/v1/vaults/{vault_id}` - Get vault information
- `POST /api/v1/vaults` - Create vault
- `POST /api/v1/vaults/{vault_id}/deposit` - Deposit to vault
- `POST /api/v1/vaults/{vault_id}/withdraw` - Withdraw from vault

#### Pool Endpoints (CTV)

**Requires**: `--features ctv`

**Code**: [rest/pool.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/pool.rs)

- `GET /api/v1/pools` - List pools
- `GET /api/v1/pools/{pool_id}` - Get pool information
- `POST /api/v1/pools` - Create pool
- `POST /api/v1/pools/{pool_id}/join` - Join pool
- `POST /api/v1/pools/{pool_id}/leave` - Leave pool

#### Congestion Control Endpoints (CTV)

**Requires**: `--features ctv`

**Code**: [rest/congestion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/congestion.rs)

- `GET /api/v1/congestion/status` - Get congestion status
- `GET /api/v1/batches` - List pending batches
- `POST /api/v1/batches` - Create batch
- `POST /api/v1/batches/{batch_id}/submit` - Submit batch

### Security Headers

The REST API includes security headers by default:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000` (when TLS enabled)

**Code**: [rest/server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/rest/server.rs#L111-L115)

### Error Codes

REST API uses standard HTTP status codes:

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 401 | Unauthorized (authentication required) |
| 404 | Not Found (resource doesn't exist) |
| 429 | Too Many Requests (rate limit exceeded) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (feature not enabled) |

## See Also

- [Node Overview](overview.md) - Node implementation details
- [Node Configuration](configuration.md) - RPC configuration options
- [Node Operations](operations.md) - Node management
- [Getting Started](../getting-started/quick-start.md) - Quick start guide
- [API Index](../reference/api-index.md) - Cross-reference to all APIs
- [Troubleshooting](../appendices/troubleshooting.md) - Common RPC issues
- [Commons Mesh Module](../modules/mesh.md) - Payment endpoints and mesh networking
- [Module System](../architecture/module-system.md) - Module architecture and IPC
