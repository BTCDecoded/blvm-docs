# Performance Tuning Guide

## Overview

bllvm-node provides extensive configuration options for performance tuning. This guide covers optimization strategies for different use cases and resource constraints.

## Configuration Areas

### Storage Performance

#### Pruning Configuration

**Purpose**: Reduce disk usage by removing old block data while maintaining chain validity.

**Configuration**:
```toml
[storage.pruning]
mode = "normal"  # Options: "disabled", "normal", "aggressive", "custom"
auto_prune = true
auto_prune_interval = 1000  # Prune every 1000 blocks
min_blocks_to_keep = 288  # Keep at least 2 days of blocks (regtest)
prune_on_startup = false
```

**Modes**:
- `disabled`: No pruning, full blockchain storage
- `normal`: Prune old blocks, keep recent blocks (default)
- `aggressive`: Prune aggressively, keep minimal recent blocks
- `custom`: Custom pruning configuration

**When to Use**:
- **Full node (mainnet)**: `disabled` or `normal` with high `min_blocks_to_keep`
- **Resource-constrained**: `aggressive` with low `min_blocks_to_keep`
- **Development/testing**: `aggressive` to save disk space

**Performance Impact**:
- Pruning reduces disk I/O for old blocks
- Increases startup time if `prune_on_startup = true`
- Reduces disk space usage significantly

---

#### Cache Configuration

**Purpose**: Improve read performance by caching frequently accessed data.

**Configuration**:
```toml
[storage]
cache_size_mb = 512  # Default: 256 MB
```

**Tuning Guidelines**:
- **Low memory (< 4GB)**: 128-256 MB
- **Medium memory (4-16GB)**: 512 MB - 1 GB
- **High memory (> 16GB)**: 1-4 GB
- **Dedicated server**: Up to 25% of available RAM

**Performance Impact**:
- Larger cache = faster reads, higher memory usage
- Monitor memory usage and adjust accordingly

---

#### Database Backend

**Current**: Redb (default, production-ready)

**Configuration**: Automatic, no tuning needed

**Performance Characteristics**:
- Fast writes (append-only log)
- Good read performance
- Efficient for blockchain data

---

### Network Performance

#### Peer Connection Settings

**Purpose**: Control peer connections for optimal network performance.

**Configuration**:
```toml
[network]
max_peers = 100  # Default: 100
target_peer_count = 8  # Default: 8

[network_timing]
target_peer_count = 8
peer_connection_delay_seconds = 2
addr_relay_min_interval_seconds = 8640  # 2.4 hours
max_addresses_per_addr_message = 1000
max_addresses_from_dns = 100
```

**Tuning Guidelines**:
- **Low bandwidth**: `max_peers = 8-16`, `target_peer_count = 4-8`
- **Medium bandwidth**: `max_peers = 50-100`, `target_peer_count = 8`
- **High bandwidth**: `max_peers = 100-125`, `target_peer_count = 8-16`

**Performance Impact**:
- More peers = faster block propagation, higher bandwidth
- Fewer peers = lower bandwidth, slower propagation

---

#### Request Timeouts

**Purpose**: Control timeout behavior for network requests.

**Configuration**:
```toml
[request_timeouts]
async_request_timeout_seconds = 300  # 5 minutes (default)
utxo_commitment_request_timeout_seconds = 30  # 30 seconds (default)
request_cleanup_interval_seconds = 60  # 1 minute (default)
pending_request_max_age_seconds = 300  # 5 minutes (default)
```

**Tuning Guidelines**:
- **Slow network**: Increase timeouts (600-900 seconds)
- **Fast network**: Decrease timeouts (60-180 seconds)
- **UTXO commitments**: Keep at 30 seconds (fast failure)

**Performance Impact**:
- Longer timeouts = more memory for pending requests
- Shorter timeouts = faster failure detection, less memory

---

#### Peer Rate Limiting

**Purpose**: Prevent peer spam and DoS attacks.

**Configuration**:
```toml
[peer_rate_limiting]
default_burst = 100  # Default: 100 messages
default_rate = 10    # Default: 10 messages/second
```

**Tuning Guidelines**:
- **High-traffic node**: Increase `default_rate` to 20-50
- **Low-resource node**: Decrease `default_rate` to 5
- **DoS protection**: Keep defaults or lower

**Performance Impact**:
- Higher limits = better throughput, more resource usage
- Lower limits = better DoS protection, potential throttling

---

### RPC Performance

#### Rate Limiting

**Purpose**: Control RPC request rate to prevent overload.

**Configuration**:
```toml
[rpc_auth]
rate_limit_burst = 100  # Default: 100 requests
rate_limit_rate = 10    # Default: 10 requests/second

# Per-method overrides
[rpc_auth.per_method_limits]
getblocktemplate = { burst = 20, rate = 10 }
sendrawtransaction = { burst = 10, rate = 5 }
```

**Tuning Guidelines**:
- **Public RPC**: Lower limits (50 burst, 5 req/sec)
- **Private RPC**: Higher limits (200 burst, 20 req/sec)
- **Mining operations**: Higher limits for `getblocktemplate`

**Performance Impact**:
- Higher limits = better throughput, more resource usage
- Lower limits = better protection, potential throttling

---

#### Request Size Limits

**Purpose**: Prevent large requests from consuming resources.

**Configuration**: Hardcoded to 1MB (not configurable)

**Performance Impact**:
- Prevents memory exhaustion from large requests
- May reject valid large transactions (rare)

---

### Module System Performance

#### Resource Limits

**Purpose**: Control module resource usage.

**Configuration**:
```toml
[module_resource_limits]
default_max_cpu_percent = 50  # Default: 50%
default_max_memory_bytes = 536870912  # Default: 512 MB
default_max_file_descriptors = 256  # Default: 256
default_max_child_processes = 10  # Default: 10
module_startup_wait_millis = 100  # Default: 100ms
module_socket_timeout_seconds = 5  # Default: 5 seconds
```

**Tuning Guidelines**:
- **CPU-intensive modules**: Increase `default_max_cpu_percent` to 75-100
- **Memory-intensive modules**: Increase `default_max_memory_bytes`
- **Many modules**: Decrease per-module limits to allow more modules

**Performance Impact**:
- Higher limits = better module performance, more resource usage
- Lower limits = more modules possible, potential throttling

---

### DoS Protection

#### Connection Limits

**Purpose**: Prevent connection-based DoS attacks.

**Configuration**:
```toml
[dos_protection]
max_connections_per_ip = 3  # Default: 3
connection_rate_limit = 5   # Default: 5 connections/minute
max_active_connections = 125  # Default: 125
```

**Tuning Guidelines**:
- **Public node**: Keep defaults or lower
- **Private node**: Increase `max_connections_per_ip` to 10-20
- **High-traffic**: Increase `max_active_connections` to 200-500

**Performance Impact**:
- Higher limits = better connectivity, more resource usage
- Lower limits = better DoS protection, potential connection rejections

---

## Performance Profiles

### Development/Testing Profile

**Use Case**: Local development, testing, regtest

**Configuration**:
```toml
[storage.pruning]
mode = "aggressive"
auto_prune = true
min_blocks_to_keep = 100

[storage]
cache_size_mb = 128

[network]
max_peers = 8
target_peer_count = 4

[rpc_auth]
rate_limit_burst = 200
rate_limit_rate = 50
```

**Characteristics**:
- Minimal disk usage
- Low memory footprint
- Fast RPC (no rate limiting)
- Fewer peers

---

### Resource-Constrained Profile

**Use Case**: VPS, limited RAM/disk

**Configuration**:
```toml
[storage.pruning]
mode = "aggressive"
auto_prune = true
min_blocks_to_keep = 288  # 2 days

[storage]
cache_size_mb = 256

[network]
max_peers = 16
target_peer_count = 4

[request_timeouts]
async_request_timeout_seconds = 600  # Longer for slow network
```

**Characteristics**:
- Aggressive pruning
- Small cache
- Few peers
- Longer timeouts

---

### Production Mainnet Profile

**Use Case**: Full node, mainnet, high availability

**Configuration**:
```toml
[storage.pruning]
mode = "normal"
auto_prune = false  # Manual pruning
min_blocks_to_keep = 2016  # Keep difficulty adjustment period

[storage]
cache_size_mb = 2048  # 2 GB cache

[network]
max_peers = 100
target_peer_count = 8

[rpc_auth]
rate_limit_burst = 100
rate_limit_rate = 10

[dos_protection]
max_active_connections = 125
```

**Characteristics**:
- Full blockchain (or normal pruning)
- Large cache
- Many peers
- Standard rate limits

---

### High-Performance Profile

**Use Case**: Mining pool, exchange, high-traffic node

**Configuration**:
```toml
[storage.pruning]
mode = "disabled"  # Full blockchain

[storage]
cache_size_mb = 4096  # 4 GB cache

[network]
max_peers = 125
target_peer_count = 16

[rpc_auth]
rate_limit_burst = 500
rate_limit_rate = 100

[rpc_auth.per_method_limits]
getblocktemplate = { burst = 100, rate = 50 }
sendrawtransaction = { burst = 200, rate = 100 }

[dos_protection]
max_active_connections = 500
```

**Characteristics**:
- Full blockchain
- Very large cache
- Maximum peers
- High rate limits
- Optimized for mining/exchange use

---

## Benchmarking

### Measuring Performance

**Block Processing**:
```bash
# Monitor block processing time
RUST_LOG=info bllvm-node 2>&1 | grep "Block validated and stored"
```

**RPC Latency**:
```bash
# Measure RPC response time
time curl -X POST http://localhost:18332 \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
```

**Memory Usage**:
```bash
# Monitor memory usage
watch -n 1 'ps aux | grep bllvm-node | awk "{print \$6/1024 \" MB\"}"'
```

**Disk I/O**:
```bash
# Monitor disk I/O
iostat -x 1
```

---

## Optimization Tips

### 1. Storage Optimization

- **Use pruning** if full blockchain not needed
- **Increase cache** if RAM available
- **Use SSD** for database directory
- **Monitor disk space** and prune proactively

### 2. Network Optimization

- **Adjust peer count** based on bandwidth
- **Use persistent peers** for stable connections
- **Enable ban list sharing** for DoS protection
- **Tune timeouts** based on network quality

### 3. RPC Optimization

- **Use authentication** for higher rate limits
- **Tune per-method limits** for specific use cases
- **Monitor RPC usage** and adjust limits
- **Use connection pooling** in clients

### 4. Module Optimization

- **Limit resource usage** per module
- **Disable unused modules** to save resources
- **Monitor module performance** and adjust limits
- **Use module-specific configs** for fine-tuning

---

## Monitoring

### Key Metrics

**Storage**:
- Disk usage (bytes)
- Cache hit rate (if available)
- Pruning statistics

**Network**:
- Peer count
- Bytes sent/received
- Connection failures

**RPC**:
- Requests per second
- Average response time
- Rate limit hits

**System**:
- CPU usage
- Memory usage
- Disk I/O

### Prometheus Metrics

Access metrics endpoint:
```bash
curl http://localhost:18332/metrics
```

Key metrics:
- `bllvm_storage_block_count`: Total blocks stored
- `bllvm_network_peers_total`: Connected peers
- `bllvm_rpc_requests_total`: Total RPC requests
- `bllvm_rpc_errors_total`: RPC errors

---

## Related Documentation

- [Best Practices](BEST_PRACTICES.md) - When to use specific configurations
- [Troubleshooting](TROUBLESHOOTING.md) - Performance issue resolution
- [High Availability](../bllvm-node/docs/HIGH_AVAILABILITY.md) - HA configuration
- [Configuration Reference](CONFIGURATION.md) - Complete configuration options
