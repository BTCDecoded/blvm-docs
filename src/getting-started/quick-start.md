# Quick Start

Get up and running with BLVM in minutes.

## Running Your First Node

After [installing](installation.md) the binary, you can start a node:

### Regtest Mode (Recommended for Development)

Regtest mode is safe for development - it creates an isolated network:

```bash
blvm
```

Or explicitly:

```bash
blvm --network regtest
```

Starts a node in regtest mode (default), creating an isolated network with instant block generation for testing and development.

### Testnet Mode

Connect to Bitcoin testnet:

```bash
blvm --network testnet
```

### Mainnet Mode

⚠️ **Warning**: Only use mainnet if you understand the risks.

```bash
blvm --network mainnet
```

## Basic Node Operations

### Checking Node Status

Once the node is running, check its status via RPC:

```bash
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1}'
```

**Example Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "chain": "regtest",
    "blocks": 100,
    "headers": 100,
    "bestblockhash": "0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206",
    "difficulty": 4.656542373906925e-10,
    "mediantime": 1231006505,
    "verificationprogress": 1.0,
    "chainwork": "0000000000000000000000000000000000000000000000000000000000000064",
    "pruned": false,
    "initialblockdownload": false
  },
  "id": 1
}
```

### Getting Peer Information

```bash
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getpeerinfo", "params": [], "id": 2}'
```

### Getting Mempool Information

```bash
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getmempoolinfo", "params": [], "id": 3}'
```

### Verifying Installation

```bash
blvm --version  # Verify installation
blvm --help     # View available options
```

The node connects to the P2P network, syncs blockchain state, accepts [RPC commands](rpc-api.md) on port 8332 (default), and can [mine blocks](mining.md) if configured.

## Using the SDK

### Generate a Governance Keypair

```bash
blvm-keygen --output my-key.key
```

### Sign a Message

```bash
blvm-sign release \
  --version v1.0.0 \
  --commit abc123 \
  --key my-key.key \
  --output signature.txt
```

### Verify Signatures

```bash
blvm-verify release \
  --version v1.0.0 \
  --commit abc123 \
  --signatures sig1.txt,sig2.txt,sig3.txt \
  --threshold 3-of-5 \
  --pubkeys keys.json
```

## Next Steps

- [First Node Setup](first-node.md) - Detailed configuration guide
- [Node Configuration](../node/configuration.md) - Full configuration options
- [RPC API Reference](../node/rpc-api.md) - Interact with your node

## See Also

- [Installation](installation.md) - Installing BLVM
- [First Node Setup](first-node.md) - Complete setup guide
- [Node Configuration](../node/configuration.md) - Configuration options
- [Node Operations](../node/operations.md) - Managing your node
- [RPC API Reference](../node/rpc-api.md) - Complete RPC API
- [Troubleshooting](../appendices/troubleshooting.md) - Common issues

