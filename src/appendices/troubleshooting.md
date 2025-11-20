# Troubleshooting

Common issues and solutions when running BLLVM nodes.

## Node Won't Start

### Port Already in Use

**Error**: `Address already in use` or `Port 8332 already in use`

**Solution**:
```bash
# Use a different port
bllvm --rpc-port 8333

# Or find and stop the process using the port
lsof -i :8332
kill <PID>
```

### Permission Denied

**Error**: `Permission denied` when accessing data directory

**Solution**:
```bash
# Fix directory permissions
sudo chown -R $USER:$USER /var/lib/bllvm

# Or use a user-writable directory
bllvm --data-dir ~/.bllvm
```

## Storage Issues

### Database Backend Fails

**Error**: `Failed to initialize database backend`

**Solution**:
- The system automatically falls back to alternative backends
- Check data directory permissions
- Ensure sufficient disk space
- Try specifying backend explicitly: `--storage-backend sled`

### Corrupted Database

**Error**: Database corruption or inconsistent state

**Solution**:
```bash
# Stop the node
# Remove corrupted database files (backup first!)
rm -rf data/blocks data/chainstate

# Restart and resync
bllvm
```

## Network Issues

### No Peer Connections

**Symptoms**: Node starts but shows 0 connections

**Solutions**:
- Check firewall settings (port 8333 for mainnet, 18333 for testnet)
- Verify network connectivity
- Try adding manual peers: `bllvm --addnode <peer-ip>:8333`
- Check DNS seed resolution

### Connection Drops

**Symptoms**: Connections established but immediately drop

**Solutions**:
- Check network stability
- Verify protocol version compatibility
- Review node logs for specific error messages
- Try different transport: `--transport tcp_only`

## RPC Issues

### RPC Connection Refused

**Error**: `Connection refused` when calling RPC

**Solutions**:
- Verify RPC is enabled: `--rpc-enabled true`
- Check RPC port: `--rpc-port 8332`
- Verify bind address: `--rpc-host 127.0.0.1` (default)
- Check firewall for RPC port

### RPC Authentication Errors

**Error**: `Unauthorized` or authentication failures

**Solutions**:
- Configure RPC credentials in config file
- Use correct username/password in requests
- For development, RPC can run without auth (not recommended for production)

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
- Use pruning: `--pruning enabled --pruning-keep-blocks 288`
- Increase cache sizes in config
- Use faster storage backend (redb recommended)
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

