# Node Operations

Operational guide for running and maintaining a BLVM node.

## Operations runbook

| Task | Section |
|------|---------|
| Start regtest / testnet / mainnet | [Starting the Node](#starting-the-node) |
| Import Bitcoin Core datadir | [Starting from a Bitcoin Core datadir](#starting-from-a-bitcoin-core-datadir) |
| Graceful shutdown | [Maintenance — Updates](#updates) (stop before upgrade; RPC `stop` or SIGTERM) |
| Backup datadir | [Maintenance — Backup](#backup) |
| Mainnet first sync | [Mainnet initial sync](../getting-started/mainnet-sync.md) |
| RPC hardening before exposure | [Deployment posture](../security/deployment-posture.md) |
| IBD stuck / slow | [Troubleshooting — Mainnet IBD](../appendices/troubleshooting.md#mainnet-ibd) |

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

## Starting from a Bitcoin Core datadir

Use when Core is **fully synced** and you want the same tip without full IBD.

<div class="admonition danger">

<div class="admonition-title">Danger</div>

Stop **`bitcoind`** before migrate or start against a Core datadir. Running both nodes against the same chainstate can corrupt data.

</div>

```bash
# Recommended: auto-migrate on start → ~/.bitcoin/blvm/
blvm start --network mainnet --datadir ~/.bitcoin
```

On first start BLVM detects the Core layout, migrates once into **`<datadir>/blvm/`**, then opens the BLVM store. **Block files are not copied by default** — BLVM keeps reading bodies from Core **`blocks/`** (~700 GB stays in one place). Only the UTXO set and indexes are converted into BLVM format (~15–30 GB under **`blvm/`**).

```bash
# Optional: explicit migrate with verify, then start the BLVM store
blvm migrate core --source ~/.bitcoin --destination ~/.bitcoin/blvm \
  --network mainnet --verify
blvm start --network mainnet --datadir ~/.bitcoin/blvm
```

### What gets migrated

| Core path | Migrated? | Notes |
|-----------|-----------|--------|
| `chainstate/` (UTXO) | **Yes** → `blvm/` | One-time convert; ~12 GB on mainnet |
| `blocks/blk*.dat` | **No** (default) | BLVM reads in place; **do not delete** `blocks/` |
| `blocks/index/` | Partial | Height/header metadata copied when readable |

<div class="admonition warning">

<div class="admonition-title">Warning</div>

Keep Core **`blocks/`** on disk unless you explicitly copied block bodies into the BLVM store. Deleting `blocks/` while BLVM reads them in place will break the node.

</div>

After a successful migrate you may delete Core **`chainstate/`** (~12 GB) if you will not run **`bitcoind`** on that datadir again.

### Flags and settings

| Flag / setting | Effect |
|----------------|--------|
| `--no-auto-migrate` | Skip Core import on start |
| `--migrate-destination PATH` | BLVM store path (default `<datadir>/blvm`) |
| `--migrate-core-only` | Migrate and exit |
| `storage.auto_migrate_core = false` | Same as `--no-auto-migrate` |
| `storage.reuse_core_block_files = false` | Copy block bodies into BLVM store (large disk use) |
| `BLVM_REUSE_CORE_BLOCK_FILES=0` | Same as `reuse_core_block_files = false` |
| `BLVM_CORE_MIGRATE_BLOCK_WORKERS` / `BLVM_CORE_MIGRATE_BLOCK_BATCH` | Parallel block read tuning |

Requires the **`rocksdb`** Cargo feature (included in default `blvm` release builds). Config and ENV details: [Bitcoin Core drop-in](configuration.md#bitcoin-core-drop-in), [Storage Backends](storage-backends.md#bitcoin-core-drop-in-migrate-on-start).

**Verify:** `--verify` on `blvm migrate core`; regtest test `core_drop_in` (fixture: `blvm-node/scripts/gen-core-regtest-fixture.sh`); mainnet smoke: `blvm-node/scripts/core-drop-in-mainnet-smoke.sh`.

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


### State Transitions

State transitions are managed by the `SyncStateMachine`:

- **Initial → Headers**: When sync begins
- **Headers → Blocks**: When headers are complete (30% progress)
- **Blocks → Synced**: When blocks are complete (60% progress)
- **Any → Error**: On error conditions


### Initial Sync

When starting for the first time, the node will:

1. **Initialize Components**: [Storage](storage-backends.md), [network](transport-abstraction.md), [RPC](rpc-api.md), [modules](../modules/overview.md)
2. **Connect to P2P Network**: Discover peers via DNS seeds or persistent peers
3. **Download Headers**: Request and validate block headers
4. **Download Blocks**: Request and validate blocks
5. **Build UTXO Set**: Construct UTXO set from validated blocks
6. **Sync to Current Height**: Continue until caught up with network


### Running State

Once synced, the node maintains:

- **Peer Connections**: Active P2P connections
- **Block Validation**: Validates and relays new blocks (via [blvm-consensus](../consensus/overview.md))
- **Transaction Processing**: Validates and relays transactions
- **Chain State Updates**: Updates chain tip and height
- **RPC Requests**: Serves [JSON-RPC API](rpc-api.md) requests
- **Health Monitoring**: Periodic health checks


### Health States

The node tracks health status for each component:

- **Healthy**: Component operating normally
- **Degraded**: Component functional but with issues
- **Unhealthy**: Component not functioning correctly
- **Down**: Component not responding


### Error Recovery

The node implements graceful error recovery:

- **Network Errors**: Automatic reconnection with exponential backoff
- **Storage Errors**: Timeout protection, graceful degradation
- **Validation Errors**: Logged and reported, node continues operation
- **Disk Space**: Periodic checks with warnings


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

## Source

- [sync.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/sync.rs)
- [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/mod.rs)
- [health.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/health.rs)
## See Also

- [Node Configuration](configuration.md) - Configuration options
- [Node Overview](overview.md) - Node architecture and features
- [RPC API Reference](rpc-api.md) - Complete RPC API documentation
- [Troubleshooting](../appendices/troubleshooting.md) - Common issues and solutions
- [Performance Optimizations](performance.md) - Performance tuning
