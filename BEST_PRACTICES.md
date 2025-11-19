# Best Practices Guide

## Overview

This guide provides recommendations for when to use specific configuration options, modules, and features based on use case and requirements.

## Configuration Decisions

### When to Use Pruning

**Use Pruning When**:
- Disk space is limited (< 500GB available)
- Running on VPS or cloud instance
- Development or testing environment
- Not serving historical blockchain data
- Running a lightweight node

**Don't Use Pruning When**:
- Serving historical blockchain queries
- Running archival node
- Need full blockchain for analysis
- Disk space is abundant (> 1TB)

**Pruning Mode Selection**:
- **Normal**: General use, keeps recent blocks
- **Aggressive**: Maximum disk savings, minimal history
- **Custom**: Specific requirements (e.g., keep last N blocks)

---

### When to Use Rate Limiting

**Use Strict Rate Limiting When**:
- Public RPC endpoint
- Exposed to internet
- Resource-constrained environment
- Preventing abuse is priority

**Use Relaxed Rate Limiting When**:
- Private/internal RPC
- Authenticated users only
- High-performance requirements
- Mining pool or exchange use

**Rate Limit Guidelines**:
- **Public**: 50 burst, 5 req/sec
- **Private**: 200 burst, 20 req/sec
- **Mining**: 500 burst, 100 req/sec (with per-method overrides)

---

### When to Use Module System

**Use Modules When**:
- Need optional features (Lightning, merge mining, etc.)
- Want process isolation for experimental features
- Developing custom functionality
- Need modular architecture

**Don't Use Modules When**:
- Running minimal node
- Resource-constrained (modules add overhead)
- Don't need optional features
- Want maximum performance (modules add IPC overhead)

**Module Selection**:
- **Lightning module**: Payment channels, LN integration
- **Merge mining module**: Auxiliary proof-of-work
- **Privacy module**: Enhanced transaction privacy
- **Custom modules**: Application-specific functionality

---

### When to Use Governance Integration

**Use Governance Integration When**:
- Running a mining node (fee forwarding attribution)
- Participating in governance (economic node)
- Want contribution tracking
- Running production node with governance participation

**Don't Use Governance Integration When**:
- Development/testing only
- Not participating in governance
- Don't need contribution tracking
- Running lightweight node

**Configuration**:
```toml
[governance]
webhook_url = "http://bllvm-commons:3000/webhooks/block"
node_id = "your-node-id"
enabled = true
```

---

### When to Use DoS Protection

**Use Strict DoS Protection When**:
- Public node exposed to internet
- High attack risk
- Resource-constrained
- Want maximum security

**Use Relaxed DoS Protection When**:
- Private/internal network
- Trusted peers only
- High-performance requirements
- Low attack risk

**DoS Protection Settings**:
- **Public**: `max_connections_per_ip = 3`, `connection_rate_limit = 5`
- **Private**: `max_connections_per_ip = 20`, `connection_rate_limit = 50`

---

### When to Use Ban List Sharing

**Use Ban List Sharing When**:
- Network of nodes (share attack information)
- Want collaborative DoS protection
- Running multiple nodes
- Community protection is priority

**Don't Use Ban List Sharing When**:
- Single isolated node
- Privacy concerns (sharing peer information)
- Don't want external dependencies
- Testing/development

**Sharing Modes**:
- **Immediate**: Share bans immediately (best protection)
- **Periodic**: Share bans periodically (balanced)
- **Disabled**: No sharing (privacy-focused)

---

### When to Use RPC Authentication

**Use RPC Authentication When**:
- RPC exposed to network
- Multiple users accessing RPC
- Need per-user rate limiting
- Security is priority

**Don't Use RPC Authentication When**:
- Local-only RPC (localhost)
- Single user
- Development/testing
- Performance is priority (auth adds overhead)

**Authentication Methods**:
- **Token-based**: Simple, good for scripts
- **Certificate-based**: Strong security, good for production

---

### When to Use Persistent Peers

**Use Persistent Peers When**:
- Have trusted peers
- Want stable connections
- Network has known good peers
- Want faster initial connection

**Don't Use Persistent Peers When**:
- No trusted peers available
- Want maximum network diversity
- Testing network discovery
- Privacy concerns (revealing peer relationships)

**Configuration**:
```toml
persistent_peers = [
    "1.2.3.4:8333",
    "5.6.7.8:8333"
]
```

---

### When to Use Transport Options

**TCP (Default)**:
- Bitcoin Core compatibility
- Maximum compatibility
- Standard P2P protocol
- **Use**: General use, compatibility priority

**QUIC (Quinn)**:
- Lower latency
- Better connection handling
- Modern protocol
- **Use**: Performance priority, modern peers

**Iroh**:
- NAT traversal
- Better connectivity
- QUIC-based
- **Use**: Behind NAT, connectivity issues

**Hybrid (TCP + Iroh)**:
- Best of both worlds
- Maximum compatibility
- **Use**: Production, maximum connectivity

---

## Module-Specific Best Practices

### Lightning Module

**When to Use**:
- Running Lightning Network node
- Payment channel operations
- LN integration required

**Configuration**:
```toml
[modules]
enabled_modules = ["lightning"]

[module_resource_limits]
# Lightning needs more resources
default_max_memory_bytes = 1073741824  # 1 GB
default_max_cpu_percent = 75
```

**Best Practices**:
- Allocate sufficient memory (1GB+)
- Monitor channel state
- Use persistent storage for channels
- Enable module auto-restart

---

### Merge Mining Module

**When to Use**:
- Participating in merge mining
- Auxiliary proof-of-work
- Mining pool operations

**Configuration**:
```toml
[modules]
enabled_modules = ["merge-mining"]

[module_resource_limits]
# Merge mining is CPU-intensive
default_max_cpu_percent = 100
default_max_memory_bytes = 536870912  # 512 MB
```

**Best Practices**:
- Allocate maximum CPU
- Monitor mining performance
- Use Stratum V2 if available
- Coordinate with mining pool

---

### Privacy Module

**When to Use**:
- Enhanced transaction privacy
- Dandelion++ relay
- Privacy-focused operations

**Configuration**:
```toml
[dandelion]
stem_timeout_seconds = 10
fluff_probability = 0.1  # 10% chance to fluff
max_stem_hops = 2
```

**Best Practices**:
- Enable Dandelion++ for privacy
- Tune fluff probability based on needs
- Monitor relay performance
- Use with privacy-focused modules

---

## Use Case Recommendations

### Development/Testing

**Configuration**:
```toml
[storage.pruning]
mode = "aggressive"
auto_prune = true

[network]
max_peers = 4

[rpc_auth]
required = false  # No auth for dev
rate_limit_burst = 1000
rate_limit_rate = 100

[modules]
enabled = false  # Disable modules for simplicity
```

**Rationale**: Minimal resources, fast iteration, no security concerns

---

### Production Mainnet Node

**Configuration**:
```toml
[storage.pruning]
mode = "normal"
auto_prune = false

[network]
max_peers = 100

[rpc_auth]
required = true
rate_limit_burst = 100
rate_limit_rate = 10

[dos_protection]
max_connections_per_ip = 3
connection_rate_limit = 5

[governance]
enabled = true  # If participating
```

**Rationale**: Security, stability, full functionality

---

### Mining Pool Node

**Configuration**:
```toml
[storage.pruning]
mode = "disabled"  # Full blockchain

[storage]
cache_size_mb = 4096  # Large cache

[network]
max_peers = 125

[rpc_auth]
required = true
rate_limit_burst = 500
rate_limit_rate = 100

[rpc_auth.per_method_limits]
getblocktemplate = { burst = 100, rate = 50 }

[modules]
enabled_modules = ["merge-mining"]
```

**Rationale**: Maximum performance, mining-optimized, full blockchain

---

### Exchange Node

**Configuration**:
```toml
[storage.pruning]
mode = "disabled"  # Full blockchain for queries

[storage]
cache_size_mb = 8192  # Very large cache

[network]
max_peers = 100

[rpc_auth]
required = true
rate_limit_burst = 1000
rate_limit_rate = 200

[rpc_auth.per_method_limits]
getrawtransaction = { burst = 500, rate = 100 }
gettxout = { burst = 500, rate = 100 }
```

**Rationale**: High throughput, full blockchain, transaction queries

---

### Lightweight Node (VPS)

**Configuration**:
```toml
[storage.pruning]
mode = "aggressive"
auto_prune = true
min_blocks_to_keep = 288

[storage]
cache_size_mb = 256

[network]
max_peers = 8

[rpc_auth]
required = true
rate_limit_burst = 50
rate_limit_rate = 5

[modules]
enabled = false  # Disable to save resources
```

**Rationale**: Minimal resources, basic functionality, cost-effective

---

## Security Best Practices

### RPC Security

1. **Always use authentication** for network-exposed RPC
2. **Use certificate-based auth** for production
3. **Set appropriate rate limits** to prevent abuse
4. **Bind to localhost** if RPC not needed externally
5. **Use TLS** if RPC exposed to network (future feature)

### Network Security

1. **Enable DoS protection** for public nodes
2. **Use ban list sharing** for collaborative protection
3. **Limit connections per IP** to prevent attacks
4. **Monitor connection patterns** for anomalies
5. **Use persistent peers** from trusted sources

### Module Security

1. **Limit module resources** to prevent abuse
2. **Review module code** before enabling
3. **Use process isolation** (enabled by default)
4. **Monitor module behavior** for anomalies
5. **Disable unused modules** to reduce attack surface

---

## Performance Best Practices

### Storage

1. **Use pruning** if full blockchain not needed
2. **Increase cache** if RAM available
3. **Use SSD** for database directory
4. **Monitor disk space** proactively
5. **Prune on schedule** rather than on-demand

### Network

1. **Tune peer count** based on bandwidth
2. **Use persistent peers** for stability
3. **Adjust timeouts** based on network quality
4. **Enable ban list sharing** for DoS protection
5. **Monitor network metrics** regularly

### RPC

1. **Use authentication** for higher rate limits
2. **Tune per-method limits** for specific use cases
3. **Monitor RPC usage** and adjust
4. **Use connection pooling** in clients
5. **Cache frequently accessed data**

---

## Related Documentation

- [Performance Tuning](PERFORMANCE_TUNING.md) - Detailed performance optimization
- [Troubleshooting](TROUBLESHOOTING.md) - Issue resolution
- [Configuration Reference](CONFIGURATION.md) - Complete configuration options
- [Module System](../bllvm-node/docs/MODULE_SYSTEM.md) - Module development
