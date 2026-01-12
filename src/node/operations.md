# Node Operations

Operational guide for running and maintaining a BLVM node.

## Starting the Node

### Basic Startup

```bash
# Regtest mode (default, safe for development)
blvm

# Testnet mode
blvm --network testnet

# Mainnet mode (use with caution)
blvm --network mainnet
```

### With Configuration

```bash
blvm --config blvm.toml
```

## Node Lifecycle

The node follows a lifecycle with multiple states and transitions.

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

**Code**: ```124:132:blvm-node/src/node/sync.rs```

### State Transitions

State transitions are managed by the `SyncStateMachine`:

- **Initial → Headers**: When sync begins
- **Headers → Blocks**: When headers are complete (30% progress)
- **Blocks → Synced**: When blocks are complete (60% progress)
- **Any → Error**: On error conditions

**Code**: ```63:121:blvm-node/src/node/sync.rs```

### Initial Sync

When starting for the first time, the node will:

1. **Initialize Components**: [Storage](storage-backends.md), [network](transport-abstraction.md), [RPC](rpc-api.md), [modules](../modules/overview.md)
2. **Connect to P2P Network**: Discover peers via DNS seeds or persistent peers
3. **Download Headers**: Request and validate block headers
4. **Download Blocks**: Request and validate blocks
5. **Build UTXO Set**: Construct UTXO set from validated blocks
6. **Sync to Current Height**: Continue until caught up with network

**Code**: ```161:171:blvm-node/src/node/sync.rs```

### Running State

Once synced, the node maintains:

- **Peer Connections**: Active P2P connections
- **Block Validation**: Validates and relays new blocks (via [blvm-consensus](../consensus/overview.md))
- **Transaction Processing**: Validates and relays transactions
- **Chain State Updates**: Updates chain tip and height
- **RPC Requests**: Serves [JSON-RPC API](rpc-api.md) requests
- **Health Monitoring**: Periodic health checks

**Code**: ```1000:1102:blvm-node/src/node/mod.rs```

### Health States

The node tracks health status for each component:

- **Healthy**: Component operating normally
- **Degraded**: Component functional but with issues
- **Unhealthy**: Component not functioning correctly
- **Down**: Component not responding

**Code**: ```8:19:blvm-node/src/node/health.rs```

### Error Recovery

The node implements graceful error recovery:

- **Network Errors**: Automatic reconnection with exponential backoff
- **Storage Errors**: Timeout protection, graceful degradation
- **Validation Errors**: Logged and reported, node continues operation
- **Disk Space**: Periodic checks with warnings

**Code**: ```1114:1140:blvm-node/src/node/mod.rs```

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
RUST_LOG=info blvm

# Debug mode
RUST_LOG=debug blvm

# Trace all operations
RUST_LOG=trace blvm
```

## Maintenance

### Database Maintenance

The node automatically maintains [block storage](storage-backends.md), UTXO set, chain indexes, and transaction indexes.

### Backup

Regular backups recommended:

```bash
# Backup data directory
tar -czf blvm-backup-$(date +%Y%m%d).tar.gz /var/lib/blvm
```

### Updates

When updating the node:

1. Stop the node gracefully
2. Backup data directory
3. Download new binary from [GitHub Releases](https://github.com/BTCDecoded/blvm/releases)
4. Replace old binary with new one
5. Restart node

## Troubleshooting

See [Troubleshooting](../appendices/troubleshooting.md) for detailed solutions to common issues.

## See Also

- [Node Configuration](configuration.md) - Configuration options
- [Node Overview](overview.md) - Node architecture and features
- [RPC API Reference](rpc-api.md) - Complete RPC API documentation
- [Troubleshooting](../appendices/troubleshooting.md) - Common issues and solutions
- [Performance Optimizations](performance.md) - Performance tuning

