# Troubleshooting

Common issues and solutions when running BLVM nodes. See [Node Operations](../node/operations.md) for operational details.

## Mainnet IBD

See [Mainnet initial sync](../getting-started/mainnet-sync.md).

| Symptom | Fix |
|---------|-----|
| Quiet 15–60s after start | Wait for peer discovery → `IBD:` lines |
| P2P **8333** in use | Stop Core or change `listen_addr` |
| `blvm sync` won't connect | `blvm --network mainnet --config … sync` |
| Slow / stalled sync | Auto-LAN when Core on LAN; else `BLVM_IBD_PEERS=<ip>:8333` |
| Slow near ~900k+ | Normal after assume-valid |
| Lost progress | Same `--data-dir`; don't delete `rocksdb/` |

## Node Won't Start

### Port Already in Use

**Error**: `Address already in use` or `Port 8332 already in use`

**Solution**:
```bash
# Use a different JSON-RPC bind (full host:port)
blvm --rpc-addr 127.0.0.1:8334

# Or pick a different P2P listen address
blvm --listen-addr 0.0.0.0:8334

# Or find and stop the process using the port
lsof -i :8332
kill <PID>
```

### Permission Denied

**Error**: `Permission denied` when accessing data directory

**Solution**:
```bash
# Fix directory permissions
sudo chown -R $USER:$USER /var/lib/blvm

# Or use a user-writable directory
blvm --data-dir ~/.blvm
```

## Storage Issues

### Bitcoin Core drop-in migration

| Symptom | Fix |
|---------|-----|
| Migration refused / lock error | Stop **`bitcoind`**; remove stale **`chainstate/LOCK`** or **`bitcoind.pid`** only when Core is not running |
| Wrong chain after migrate | Set **`--network`** to match the Core datadir (mainnet / testnet / regtest) |
| Re-import on every start | Check **`blvm_meta/migration.json`** under the BLVM store; use **`--no-auto-migrate`** after a successful migrate |
| Pruned Core datadir | Use a full node copy, or enable **`storage.reuse_core_block_files`** only if remaining block files cover the chain |
| Interrupted migrate | Resume with **`blvm migrate core`** or restart with auto-migrate; checkpoint at **`blvm_meta/migration_checkpoint.json`** |

See [Starting from a Bitcoin Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir).

### Database Backend Fails

**Error**: `Failed to initialize database backend`

**Solution**:
- The system automatically falls back to alternative backends when the chosen one fails
- Check data directory permissions and sufficient disk space
- Set backend explicitly in config if needed: `[storage] database_backend = "rocksdb"` / `"redb"` / `"sled"` / `"tidesdb"`, or keep **`"auto"`** (default builds usually pick **RocksDB** first). See [Configuration Reference](../reference/configuration-reference.md).

### Corrupted Database

**Error**: Database corruption or inconsistent state

**Solution**:
```bash
# Stop the node
# Remove corrupted database files (backup first!)
rm -rf data/blocks data/chainstate

# Restart and resync
blvm
```

## Network Issues

### No Peer Connections

**Symptoms**: Node starts but shows 0 connections

**Solutions**:
- Check firewall settings (port 8333 for mainnet, 18333 for testnet)
- Verify network connectivity
- Try adding manual peers: `persistent_peers` in `blvm.toml`, or the **`addnode`** RPC method after the node is up
- Check DNS seed resolution

### Connection Drops

**Symptoms**: Connections established but immediately drop

**Solutions**:
- Check network stability
- Verify protocol version compatibility
- Review node logs for specific error messages
- Adjust transport in **`blvm.toml`** (`transport_preference = "tcponly"`, etc.) or set **`BLVM_NODE_TRANSPORT`** (e.g. `tcp_only`) — there is no `--transport` flag on **`blvm`**

## RPC Issues

### RPC Connection Refused

**Error**: `Connection refused` when calling RPC

**Solutions**:
- Verify the process is listening on **`--rpc-addr`** (mainnet default `127.0.0.1:8332`; testnet/regtest `127.0.0.1:18332` when using `blvm` without overrides)
- Check bind address: use `0.0.0.0:8332` when exposing RPC in a container
- Check firewall for the RPC port you configured

### RPC Authentication Errors

**Error**: `Unauthorized` or authentication failures

**Solutions**:
- Configure **`[rpc_auth]`** tokens (or `RPC_AUTH_TOKENS` / `token_file`) when `required = true`
- Send `Authorization: Bearer <token>` on HTTP JSON-RPC requests
- For local development only, leave **`[rpc_auth].required = false`** (not for production)

## Module System Issues

### Module Not Loading

**Error**: Module fails to load or start

**Solutions**:
- Verify `module.toml` exists and is valid
- Check module binary exists at expected path
- Review module logs in `data/modules/logs/`
- Verify module has required permissions in manifest
- Check IPC socket directory permissions

### IPC Connection Failures

**Error**: Module cannot connect to node IPC

**Solutions**:
- Ensure socket directory exists: `data/modules/sockets/`
- Check file permissions on socket directory
- Verify module process has access to socket
- Restart node to recreate sockets

## Performance Issues

### Slow Initial Sync

**Symptoms**: Node takes very long to sync

**Solutions**:
- Tune **`[storage.pruning]`** in `blvm.toml` (see [Storage backends](../node/storage-backends.md)); pruning is not toggled via ad-hoc `blvm --pruning …` flags
- Increase cache sizes in config
- Use a storage backend suited to your workload (see [Storage Backends](../node/storage-backends.md))
- Check network bandwidth and latency

### High Memory Usage

**Symptoms**: Node uses excessive memory

**Solutions**:
- Reduce cache sizes in config
- Enable pruning to reduce data size
- Check for memory leaks in logs
- Consider using lighter storage backend

## Getting Help

- Check node logs: `data/logs/` or console output
- Review [Configuration](../node/configuration.md) for options
- See [RPC API](../node/rpc-api.md) for available methods
- Check GitHub issues for known problems

## See Also

- [Node Operations](../node/operations.md) - Node management and operations
- [Node Configuration](../node/configuration.md) - Configuration options
- [Getting Started](../getting-started/first-node.md) - First node setup
- [FAQ](faq.md) - Frequently asked questions
- [Migration Guides](migration-guides.md) - Migration from other implementations
