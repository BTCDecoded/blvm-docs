# Troubleshooting Guide

## Common Issues and Solutions

### bllvm-node Issues

#### Node Won't Start

**Symptoms**:
- Node fails to start
- Error: "Database already open" or "Cannot acquire lock"
- Port already in use errors

**Solutions**:
1. **Check for running instances**:
   ```bash
   ps aux | grep bllvm-node
   killall bllvm-node  # If found
   ```

2. **Check database lock**:
   ```bash
   # Remove lock file if corrupted
   rm -f data/redb.db.lock
   ```

3. **Check port availability**:
   ```bash
   # Check if port is in use
   lsof -i :18332  # RPC port
   lsof -i :18444  # P2P port (regtest)
   ```

4. **Use different data directory**:
   ```bash
   bllvm-node --data-dir ./data2
   ```

---

#### Database Errors

**Symptoms**:
- "Database corruption" errors
- "Unknown table name" errors
- Database lock errors

**Solutions**:
1. **Check database file permissions**:
   ```bash
   ls -la data/redb.db
   chmod 644 data/redb.db  # If needed
   ```

2. **Verify database integrity**:
   ```bash
   # Redb doesn't have built-in integrity check
   # If corrupted, restore from backup or resync
   ```

3. **Recreate database** (data loss):
   ```bash
   rm -f data/redb.db*
   # Node will recreate on next start
   ```

4. **Check disk space**:
   ```bash
   df -h data/
   # Ensure sufficient space for database growth
   ```

---

#### Network Connection Issues

**Symptoms**:
- No peers connected
- "Connection refused" errors
- Network timeouts

**Solutions**:
1. **Check firewall settings**:
   ```bash
   # Allow P2P port (default: 18444 for regtest, 8333 for mainnet)
   sudo ufw allow 18444/tcp
   ```

2. **Check network configuration**:
   ```bash
   # Verify network interface
   ip addr show
   
   # Test connectivity
   ping 8.8.8.8
   ```

3. **Check DNS resolution**:
   ```bash
   # For DNS seed nodes
   nslookup seed.btcdecoded.org
   ```

4. **Use persistent peers**:
   ```toml
   [network]
   persistent_peers = ["1.2.3.4:8333", "5.6.7.8:8333"]
   ```

5. **Check ban list**:
   ```bash
   # Via RPC
   curl -X POST http://localhost:18332 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"listbanned","params":[],"id":1}'
   ```

---

#### RPC Connection Issues

**Symptoms**:
- "Connection refused" when calling RPC
- "401 Unauthorized" errors
- "429 Too Many Requests" errors

**Solutions**:
1. **Check RPC server is running**:
   ```bash
   curl http://localhost:18332/health
   ```

2. **Check authentication**:
   ```bash
   # If auth is enabled, provide token
   curl -X POST http://localhost:18332 \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
   ```

3. **Check rate limiting**:
   - Reduce request frequency
   - Use authenticated requests (higher limits)
   - Check rate limit configuration

4. **Check RPC bind address**:
   ```toml
   [rpc]
   bind_address = "127.0.0.1:18332"  # Localhost only
   # or
   bind_address = "0.0.0.0:18332"    # All interfaces
   ```

---

#### Performance Issues

**Symptoms**:
- Slow block processing
- High CPU usage
- High memory usage
- Disk I/O bottlenecks

**Solutions**:
1. **Check system resources**:
   ```bash
   # CPU usage
   top -p $(pgrep bllvm-node)
   
   # Memory usage
   free -h
   
   # Disk I/O
   iostat -x 1
   ```

2. **Enable pruning**:
   ```toml
   [storage]
   pruning_mode = "normal"
   pruning_threshold_gb = 100
   pruning_target_gb = 80
   ```

3. **Adjust cache sizes**:
   ```toml
   [storage]
   cache_size_mb = 512  # Increase if RAM available
   ```

4. **Check for disk space**:
   ```bash
   df -h
   # Ensure sufficient space for blockchain data
   ```

5. **Profile with perf**:
   ```bash
   perf record -g ./target/release/bllvm-node
   perf report
   ```

---

#### Block Validation Errors

**Symptoms**:
- "Invalid block" errors
- "Consensus validation failed"
- Blocks rejected

**Solutions**:
1. **Check block data**:
   ```bash
   # Get block details via RPC
   curl -X POST http://localhost:18332 \
     -d '{"jsonrpc":"2.0","method":"getblock","params":["blockhash"],"id":1}'
   ```

2. **Verify chain state**:
   ```bash
   # Check chain tips
   curl -X POST http://localhost:18332 \
     -d '{"jsonrpc":"2.0","method":"getchaintips","params":[],"id":1}'
   ```

3. **Check for chain reorganization**:
   - Monitor logs for reorganization events
   - Verify UTXO set consistency

4. **Revalidate chain**:
   ```bash
   # Via RPC (may take time)
   curl -X POST http://localhost:18332 \
     -d '{"jsonrpc":"2.0","method":"verifychain","params":[3,6],"id":1}'
   ```

---

### bllvm-commons Issues

#### Database Connection Failed

**Symptoms**:
- Application fails to start
- Error: "Database connection failed"
- Logs show connection timeout

**Solutions**:
1. **Check database URL**:
   ```bash
   echo $DATABASE_URL
   # Should be: sqlite:governance.db or postgresql://...
   ```

2. **Verify SQLite installation**:
   ```bash
   sqlite3 --version
   ```

3. **Check file permissions**:
   ```bash
   ls -la governance.db
   chmod 644 governance.db  # If needed
   ```

4. **Test database connection**:
   ```bash
   sqlite3 governance.db "SELECT 1;"
   ```

---

#### GitHub API Errors

**Symptoms**:
- Error: "GitHub authentication failed"
- API calls return 401 Unauthorized
- Webhook validation fails

**Solutions**:
1. **Verify App ID and private key**:
   ```bash
   echo $GITHUB_APP_ID
   ls -la private_key.pem
   ```

2. **Check private key format**:
   ```bash
   head -1 private_key.pem
   # Should start with: -----BEGIN RSA PRIVATE KEY-----
   ```

3. **Verify app installation**:
   - Check GitHub App is installed on repositories
   - Verify installation has correct permissions

4. **Check webhook secret**:
   ```bash
   echo $GITHUB_WEBHOOK_SECRET
   # Must match GitHub webhook configuration
   ```

---

#### Webhook Not Received

**Symptoms**:
- GitHub webhooks not processed
- No webhook events in logs
- Webhook delivery failures

**Solutions**:
1. **Check webhook URL**:
   - Verify webhook URL in GitHub settings
   - Must be publicly accessible (use ngrok for local dev)

2. **Check webhook secret**:
   ```bash
   # Must match in both places
   echo $GITHUB_WEBHOOK_SECRET
   ```

3. **Test webhook locally**:
   ```bash
   # Use ngrok to expose local server
   ngrok http 3000
   # Update GitHub webhook URL to ngrok URL
   ```

4. **Check webhook event types**:
   - Ensure "Pull requests" and "Pull request reviews" are enabled
   - Check webhook delivery logs in GitHub

---

### Integration Issues

#### Governance Webhook Not Working

**Symptoms**:
- Blocks processed but no contributions tracked
- Webhook errors in logs
- Node registry lookup fails

**Solutions**:
1. **Check webhook URL configuration**:
   ```toml
   # In bllvm-node config
   [governance]
   webhook_url = "http://localhost:3000/webhooks/block"
   node_id = "your-node-id"
   enabled = true
   ```

2. **Verify node registration**:
   ```bash
   curl http://localhost:3000/nodes/your-node-id
   ```

3. **Check network connectivity**:
   ```bash
   # From bllvm-node host
   curl http://bllvm-commons-host:3000/health
   ```

4. **Check logs**:
   ```bash
   # bllvm-node logs
   tail -f logs/bllvm-node.log | grep webhook
   
   # bllvm-commons logs
   tail -f logs/bllvm-commons.log | grep webhook
   ```

---

#### Signature Verification Fails

**Symptoms**:
- PR signatures not recognized
- "Invalid signature" errors
- Multisig threshold not met

**Solutions**:
1. **Verify key format**:
   ```bash
   # Check public key format
   bllvm-verify --key pubkey.pem --message message.txt --signature sig.txt
   ```

2. **Check signature format**:
   - Signatures must be in correct format
   - Verify signature encoding (hex/base64)

3. **Verify maintainer keys**:
   ```bash
   # List registered maintainers
   curl http://localhost:3000/maintainers
   ```

4. **Check multisig threshold**:
   - Verify threshold configuration matches governance tier
   - Ensure sufficient signatures collected

---

## Debugging Tips

### Enable Debug Logging

**bllvm-node**:
```bash
RUST_LOG=debug bllvm-node
# or
RUST_LOG=trace bllvm-node  # Very verbose
```

**bllvm-commons**:
```bash
RUST_LOG=debug cargo run
```

### Check Health Endpoints

**bllvm-node**:
```bash
curl http://localhost:18332/health
curl http://localhost:18332/health/detailed
```

**bllvm-commons**:
```bash
curl http://localhost:3000/health
```

### Monitor Metrics

**bllvm-node Prometheus metrics**:
```bash
curl http://localhost:18332/metrics
```

### Check System Resources

```bash
# CPU and memory
htop

# Disk I/O
iostat -x 1

# Network
iftop
```

---

## Getting Help

1. **Check logs**: Review application logs for error messages
2. **Check documentation**: See component-specific docs
3. **Search issues**: Check GitHub issues for similar problems
4. **Ask community**: Use GitHub Discussions
5. **Report bugs**: Create GitHub issue with details

---

## Related Documentation

- [Performance Tuning](PERFORMANCE_TUNING.md) - Performance optimization
- [Best Practices](BEST_PRACTICES.md) - Configuration recommendations
- [High Availability](../bllvm-node/docs/HIGH_AVAILABILITY.md) - HA features
- Component-specific troubleshooting in each repository
