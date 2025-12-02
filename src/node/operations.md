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

The node follows a well-defined lifecycle with multiple states and transitions.

### Lifecycle States

The node operates in the following states:

```
Initial → Headers → Blocks → Synced
   ↓         ↓         ↓         ↓
 Error    Error    Error    Error
```

**State Descriptions**:

1. **Initial**: Node starting up, initializing components
2. **Headers**: Downloading and validating block headers
3. **Blocks**: Downloading and validating full blocks
4. **Synced**: Fully synchronized, normal operation
5. **Error**: Error state (can transition from any state)

**Code**: ```124:132:bllvm-node/src/node/sync.rs```

### State Transitions

State transitions are managed by the `SyncStateMachine`:

- **Initial → Headers**: When sync begins
- **Headers → Blocks**: When headers are complete (30% progress)
- **Blocks → Synced**: When blocks are complete (60% progress)
- **Any → Error**: On error conditions

**Code**: ```63:121:bllvm-node/src/node/sync.rs```

### Initial Sync

When starting for the first time, the node will:

1. **Initialize Components**: Storage, network, RPC, modules
2. **Connect to P2P Network**: Discover peers via DNS seeds or persistent peers
3. **Download Headers**: Request and validate block headers
4. **Download Blocks**: Request and validate full blocks
5. **Build UTXO Set**: Construct UTXO set from validated blocks
6. **Sync to Current Height**: Continue until caught up with network

**Code**: ```161:171:bllvm-node/src/node/sync.rs```

### Running State

Once synced, the node maintains:

- **Peer Connections**: Active P2P connections
- **Block Validation**: Validates and relays new blocks
- **Transaction Processing**: Validates and relays transactions
- **Chain State Updates**: Updates chain tip and height
- **RPC Requests**: Serves JSON-RPC API requests
- **Health Monitoring**: Periodic health checks

**Code**: ```1000:1102:bllvm-node/src/node/mod.rs```

### Health States

The node tracks health status for each component:

- **Healthy**: Component operating normally
- **Degraded**: Component functional but with issues
- **Unhealthy**: Component not functioning correctly
- **Down**: Component not responding

**Code**: ```8:19:bllvm-node/src/node/health.rs```

### Error Recovery

The node implements graceful error recovery:

- **Network Errors**: Automatic reconnection with exponential backoff
- **Storage Errors**: Timeout protection, graceful degradation
- **Validation Errors**: Logged and reported, node continues operation
- **Disk Space**: Periodic checks with warnings

**Code**: ```1114:1140:bllvm-node/src/node/mod.rs```

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

