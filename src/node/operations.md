# Node Operations

Operational guide for running and maintaining a BLLVM node.

## Starting the Node

### Basic Startup

```bash
# Regtest mode (default, safe for development)
bllvm

# Testnet mode
bllvm --network testnet

# Mainnet mode (use with caution)
bllvm --network mainnet
```

### With Configuration

```bash
bllvm --config bllvm.toml
```

## Node Lifecycle

### Initial Sync

When starting for the first time, the node will:

1. Connect to the P2P network
2. Discover peers
3. Download and validate blockchain history
4. Build UTXO set
5. Sync to current block height

### Running State

Once synced, the node maintains peer connections, validates and relays blocks/transactions, updates chain state, and serves RPC requests.

## Monitoring

### Health Checks

```bash
# Check if node is running
curl http://localhost:8332/health

# Get blockchain info via RPC
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getblockchaininfo", "params": [], "id": 1}'
```

### Logging

The node uses structured logging. Set log level via environment variable:

```bash
# Set log level
RUST_LOG=info bllvm

# Debug mode
RUST_LOG=debug bllvm

# Trace all operations
RUST_LOG=trace bllvm
```

## Maintenance

### Database Maintenance

The node automatically maintains block storage, UTXO set, chain indexes, and transaction indexes.

### Backup

Regular backups recommended:

```bash
# Backup data directory
tar -czf bllvm-backup-$(date +%Y%m%d).tar.gz /var/lib/bllvm
```

### Updates

When updating the node:

1. Stop the node gracefully
2. Backup data directory
3. Download new binary from [GitHub Releases](https://github.com/BTCDecoded/bllvm-node/releases)
4. Replace old binary with new one
5. Restart node

## Troubleshooting

See [Troubleshooting](../appendices/troubleshooting.md) for detailed solutions to common issues.

