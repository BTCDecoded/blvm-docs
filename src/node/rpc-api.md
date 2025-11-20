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

## Implementation Status

{{#include ../../../modules/bllvm-node/docs/status/RPC_IMPLEMENTATION_STATUS.md}}

