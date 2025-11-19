# Quick Start Guide

## System Overview

Bitcoin Commons is a 6-tier Bitcoin implementation with cryptographic governance. This guide provides a minimal setup to run the system.

## Prerequisites

- Rust 1.70+ (for building from source)
- SQLite 3.35+ (for development) or PostgreSQL 13+ (for production)
- Git 2.30+

## Repository Setup

Clone all repositories:

```bash
# Create workspace directory
mkdir bitcoin-commons && cd bitcoin-commons

# Clone repositories
git clone https://github.com/BTCDecoded/bllvm-consensus.git
git clone https://github.com/BTCDecoded/bllvm-protocol.git
git clone https://github.com/BTCDecoded/bllvm-node.git
git clone https://github.com/BTCDecoded/bllvm-sdk.git
git clone https://github.com/BTCDecoded/bllvm-commons.git
```

## Build Order

Build components in dependency order:

```bash
# 1. Foundation: bllvm-consensus
cd bllvm-consensus
cargo build --release
cd ..

# 2. Protocol layer: bllvm-protocol
cd bllvm-protocol
cargo build --release
cd ..

# 3. Node: bllvm-node
cd bllvm-node
cargo build --release
cd ..

# 4. SDK: bllvm-sdk (parallel with consensus)
cd bllvm-sdk
cargo build --release
cd ..

# 5. Governance: bllvm-commons
cd bllvm-commons/bllvm-commons
cargo build --release
cd ../..
```

## Quick Start: bllvm-node

Run a regtest node:

```bash
cd bllvm-node
cargo run --release -- --network regtest --data-dir ./data
```

Node starts on:
- P2P: `0.0.0.0:18444` (regtest default)
- RPC: `127.0.0.1:18332` (regtest default)

## Quick Start: bllvm-commons

Run governance service:

```bash
cd bllvm-commons/bllvm-commons

# Set environment variables
export DATABASE_URL="sqlite:governance.db"
export GITHUB_APP_ID="your-app-id"
export GITHUB_PRIVATE_KEY_PATH="./keys/github-app.pem"
export GITHUB_WEBHOOK_SECRET="your-webhook-secret"

# Run
cargo run --release
```

Service starts on `http://0.0.0.0:3000`

## Integration Setup

### Connect bllvm-node to bllvm-commons

**In bllvm-node config** (`config.toml`):
```toml
[governance]
webhook_url = "http://localhost:3000/webhooks/block"
node_id = "test-node-001"
enabled = true
```

**Register node in bllvm-commons**:
```bash
curl -X POST http://localhost:3000/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "test-node-001",
    "node_name": "Test Node",
    "node_type": "node",
    "bitcoin_addresses": ["bc1q..."],
    "metadata": {}
  }'
```

## Verification

### Verify bllvm-node

```bash
cd bllvm-node
cargo test --release
```

### Verify bllvm-commons

```bash
cd bllvm-commons/bllvm-commons
cargo test --release
```

### Verify integration

1. Start `bllvm-node` (regtest)
2. Start `bllvm-commons`
3. Register node in `bllvm-commons`
4. Mine a block in `bllvm-node`
5. Check `bllvm-commons` logs for webhook receipt

## Next Steps

- [Architecture](ARCHITECTURE.md) - Understand system architecture
- [Integration](INTEGRATION.md) - Learn integration patterns
- [Deployment](DEPLOYMENT.md) - Production deployment
- [Configuration](CONFIGURATION.md) - Configuration reference

## Component-Specific Quick Starts

- **bllvm-consensus**: See `bllvm-consensus/README.md`
- **bllvm-protocol**: See `bllvm-protocol/README.md`
- **bllvm-node**: See `bllvm-node/README.md`
- **bllvm-sdk**: See `bllvm-sdk/README.md`
- **bllvm-commons**: See `bllvm-commons/README.md`
