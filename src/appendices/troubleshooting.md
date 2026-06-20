# Troubleshooting

Common issues and solutions when running BLVM nodes. See [Node Operations](../node/operations.md) for operational details.

## Symptom guide

Start from what you observe — each row links to a section on this page.

| If you see… | Go to |
|-------------|--------|
| Quiet after start, no `IBD:` lines | [Mainnet IBD](#mainnet-ibd) |
| `Address already in use` | [Port already in use](#port-already-in-use) |
| `Connection refused` on RPC | [RPC connection refused](#rpc-connection-refused) |
| `Unauthorized` / 403 on mining RPC | [RPC authentication](#rpc-authentication-errors) |
| Core migrate fails / lock error | [Core drop-in migration](#bitcoin-core-drop-in-migration) |
| `Failed to initialize database` | [Database backend fails](#database-backend-fails) |
| Corruption / inconsistent chain | [Corrupted database](#corrupted-database) |
| 0 peers | [No peer connections](#no-peer-connections) |
| Module won't load | [Module not loading](#module-not-loading) |

## Mainnet IBD

First-time sync setup: [First Node Setup — Mainnet initial sync](../getting-started/first-node.md#mainnet-initial-sync).

| Symptom | Fix |
|---------|-----|
| Quiet 15–60s after start | Wait for peer discovery → `IBD:` lines |
| P2P **8333** in use | Stop Core or change `listen_addr` |
| `blvm sync` won't connect | `blvm --network mainnet --config … sync` |
| Slow / stalled sync | Auto-LAN when Core on LAN; else `BLVM_IBD_PEERS=<ip>:8333` |
| Slow near ~900k+ | Normal after assume-valid |
| Lost progress | Same `--data-dir`; do not delete the active backend directory (`heed3/`, `rocksdb/`, etc.) mid-IBD |

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
| Pruned Core datadir | Use a full node copy; default **`reuse_core_block_files`** requires readable block files at the tip |
| Disk filling during migrate | Default should **not** copy blocks; if copying, set **`reuse_core_block_files = false`** explicitly — otherwise check you are not re-migrating into a fresh store with reuse disabled |
| Interrupted migrate | Resume with **`blvm migrate core`** or restart with auto-migrate; checkpoint at **`blvm_meta/migration_checkpoint.json`** |

See [Starting from a Bitcoin Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir).

### Database Backend Fails

**Error**: `Failed to initialize database backend`

**Solution**:
- The system automatically falls back to alternative backends when the chosen one fails
- Check data directory permissions and sufficient disk space
- Set backend explicitly in config if needed: `[storage] database_backend = "rocksdb"` / `"heed3"` / `"redb"` / `"sled"` / `"tidesdb"`, or keep **`"auto"`** (default builds usually pick **heed3** first). See [Configuration Reference](../reference/configuration-reference.md).

### Corrupted Database {#corrupted-database}

**Error**: Database corruption or inconsistent state

**Solution**:

1. **Stop the node** before deleting anything.
2. Identify the active backend under `{data_dir}` — e.g. `heed3/`, `rocksdb/`, `redb/`, `sled/`, `tidesdb/` (see [Storage backends](../node/storage-backends.md)).
3. Back up the datadir, then remove only the corrupted backend subtree (not generic `data/blocks` / `data/chainstate` Core paths unless you intentionally reset a Core-import layout).
4. Restart; expect resync or migration depending on what you removed.

For Core chainstate import errors (LevelDB `.ldb` vs RocksDB layout, mixed `.ldb` + `.sst` index), see [Storage backends — Core LevelDB interop](../node/storage-backends.md#core-leveldb-interop) and use `blvm config convert-core` / migration tooling rather than blind `rm -rf`.

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
- Verify the process is listening on **`--rpc-addr`** (mainnet default `127.0.0.1:8332`; testnet `127.0.0.1:18332`; regtest `127.0.0.1:18443` when using `blvm` without overrides)
- Check bind address: use `0.0.0.0:8332` when exposing RPC in a container
- Check firewall for the RPC port you configured

### RPC Authentication Errors

**Error**: `Unauthorized` or authentication failures

**Solutions**:
- Configure **`[rpc_auth]`** tokens (or `RPC_AUTH_TOKENS` / `token_file`) when `required = true`
- Send `Authorization: Bearer <token>` on HTTP JSON-RPC requests
- For **admin-only** methods (`generatetoaddress`, `getblocktemplate`, `submitblock`, `loadmodule`, …), use a token listed in **`admin_tokens`** or HTTP Basic **`password`** — otherwise HTTP **403** (not JSON-RPC -32603). See [JSON-RPC error reference](../reference/rpc-errors.md#admin-only-methods)
- For local development only, leave **`[rpc_auth].required = false`** (not for production)

### `savemempool` / mempool.dat errors

**Error**: `savemempool` fails with I/O or “no such file or directory” for the data directory

**Cause**: Earlier builds wrote `mempool.dat` only when the data directory already existed.

**Solutions**:
- Use a current build: `savemempool` creates the data directory (parent of `mempool.dat`) before writing
- Ensure **`--data-dir`** / `DATA_DIR` points to the intended location
- Check disk space and permissions on the data directory path

## Module System Issues

### Module Not Loading

**Error**: Module fails to load or start

**Solutions**:
- Verify `module.toml` exists and is valid (manifest **`name`** matches `[modules]` pin and `[modules.<name>]` table keys)
- Check module binary exists at the path expected by `module.toml` `entry_point` under **`[modules].modules_dir`**
- Review **node stdout** / **`RUST_LOG`** (module subprocess output is forwarded over IPC; there is no fixed `data/modules/logs/` tree in core)
- Inspect module state under **`{modules.data_dir}/<manifest-name>/`** (default `{modules.data_dir}` is `data/modules` relative to the process unless configured)
- Verify module capabilities in `module.toml` match what the module requests at runtime
- Ensure **`[modules].socket_dir`** exists and is writable (default `data/modules/sockets`)

### IPC Connection Failures

**Error**: Module cannot connect to node IPC

**Solutions**:
- Ensure **`[modules].socket_dir`** exists (default `data/modules/sockets` under the node working directory unless overridden in `blvm.toml`)
- Check file permissions on the socket directory
- Verify the module process can access Unix domain sockets on the host
- Restart the node to recreate IPC sockets after crashes

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

- Check node logs: **console output** from `blvm --verbose`, or **`RUST_LOG`** / `[logging]` filter in config
- Review [Configuration](../node/configuration.md) for options
- See [RPC API](../node/rpc-api.md) for available methods
- Check GitHub issues for known problems

## See Also

- [Node Operations](../node/operations.md) - Node management and operations
- [Node Configuration](../node/configuration.md) - Configuration options
- [Getting Started](../getting-started/first-node.md) - First node setup
- [FAQ](faq.md) - Frequently asked questions
- [Starting from a Bitcoin Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir) - Import a synced Core datadir
- [Upgrading an existing deployment](../development/release-process.md#upgrading-an-existing-deployment) - Version upgrades
