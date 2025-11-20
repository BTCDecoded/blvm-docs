# Quick Start

Get up and running with BLLVM in minutes.

## Running Your First Node

After [installing](installation.md) the binary, you can start a node:

### Regtest Mode (Recommended for Development)

Regtest mode is safe for development - it creates an isolated network:

```bash
bllvm
```

Or explicitly:

```bash
bllvm --network regtest
```

This starts a node in regtest mode (default), creating an isolated network with instant block generation, perfect for testing and development.

### Testnet Mode

Connect to Bitcoin testnet:

```bash
bllvm --network testnet
```

### Mainnet Mode

⚠️ **Warning**: Only use mainnet if you understand the risks.

```bash
bllvm --network mainnet
```

## Basic Node Operations

### Checking Node Status

Once the node is running, check its status via RPC:

```bash
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1}'
```

### Verifying Installation

```bash
bllvm --version  # Verify installation
bllvm --help     # View available options
```

The node connects to the P2P network, syncs blockchain state, accepts RPC commands on port 8332 (default), and can mine blocks if configured.

## Using the SDK

### Generate a Governance Keypair

```bash
bllvm-keygen --output my-key.key
```

### Sign a Message

```bash
bllvm-sign release \
  --version v1.0.0 \
  --commit abc123 \
  --key my-key.key \
  --output signature.txt
```

### Verify Signatures

```bash
bllvm-verify release \
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

