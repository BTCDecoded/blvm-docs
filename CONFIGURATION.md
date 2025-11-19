# Configuration Guide

Complete configuration reference for all BLLVM components.

## Overview

BLLVM components use configuration files and environment variables for customization. This guide covers all configuration options with their defaults, types, and usage.

## Configuration Defaults

All configuration defaults are automatically extracted from source code. See [Configuration Defaults](CONFIGURATION_DEFAULTS.md) for the complete list.

### Quick Reference

**bllvm-node**:
- Storage: Cache sizes, pruning modes, data paths
- Network: Peer settings, timeouts, connection limits
- RPC: Rate limiting, authentication
- Modules: Resource limits, directories
- DoS Protection: Ban thresholds, window sizes

**bllvm-commons**:
- Network: Bitcoin network (mainnet/testnet/regtest)
- Governance: Weight update intervals, contribution tracking

## bllvm-node Configuration

### Storage Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `storage.path` | `"data"` | Directory for blockchain data |
| `block.cache.mb` | `100` | Block cache size in MB |
| `header.cache.mb` | `10` | Header cache size in MB |
| `utxo.cache.mb` | `50` | UTXO cache size in MB |
| `pruning.mode` | `true` | Enable block pruning |

See [Configuration Defaults](CONFIGURATION_DEFAULTS.md#bllvm-node-defaults) for complete list.

### Network Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `target.peer.count` | `8` | Target number of connected peers |
| `peer.connection.delay` | `2` | Delay between peer connections (seconds) |
| `async.request.timeout` | `300` | Async request timeout (5 minutes) |
| `utxo.commitment.timeout` | `30` | UTXO commitment timeout (seconds) |

See [Configuration Defaults](CONFIGURATION_DEFAULTS.md#network-configuration) for complete list.

### RPC Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `rate.limit.rate` | `10` | RPC rate limit (requests per window) |
| `rate.limit.burst` | `100` | RPC burst limit |

See [Configuration Defaults](CONFIGURATION_DEFAULTS.md#rpc-configuration) for complete list.

### Module Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `modules.dir` | `"modules"` | Directory containing module binaries |
| `modules.data.dir` | `"data/modules"` | Directory for module data |
| `module.max.memory.bytes` | `536870912` | Maximum memory per module (512 MB) |
| `module.max.cpu.percent` | `50` | Maximum CPU usage per module (%) |

See [Configuration Defaults](CONFIGURATION_DEFAULTS.md#modules-configuration) for complete list.

### DoS Protection Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `dos.auto.ban.threshold` | `3` | Violations before auto-ban |
| `dos.ban.duration` | `3600` | Ban duration (1 hour) |
| `dos.window.seconds` | `60` | Rate limit window (seconds) |

See [Configuration Defaults](CONFIGURATION_DEFAULTS.md#dos-protection-configuration) for complete list.

## bllvm-commons Configuration

### Governance Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `network` | `"mainnet"` | Bitcoin network (mainnet/testnet/regtest) |
| `weight.update.interval` | `86400` | Weight update interval (daily) |

See [Configuration Defaults](CONFIGURATION_DEFAULTS.md#bllvm-commons-defaults) for complete list.

## Configuration Files

### bllvm-node

Configuration file: `config.toml` (or via environment variables)

Example:
```toml
[storage]
path = "data"
block_cache_mb = 200
pruning_mode = true

[network]
target_peer_count = 16
peer_connection_delay = 1

[rpc]
rate_limit_rate = 20
rate_limit_burst = 200

[modules]
max_memory_bytes = 1073741824  # 1 GB
max_cpu_percent = 75
```

### bllvm-commons

Configuration file: `config.toml` (or via environment variables)

Example:
```toml
[governance]
network = "mainnet"
weight_update_interval_secs = 86400
contribution_tracking_enabled = true
```

## Environment Variables

All configuration options can be overridden via environment variables:

- Format: `BLLVM_<SECTION>_<KEY>` (uppercase, underscores)
- Example: `BLLVM_STORAGE_PATH=/custom/path`
- Example: `BLLVM_NETWORK_TARGET_PEER_COUNT=16`

## Best Practices

See [Best Practices](BEST_PRACTICES.md) for configuration recommendations based on use case.

## Performance Tuning

See [Performance Tuning](PERFORMANCE_TUNING.md) for performance-related configuration options.

## Troubleshooting

See [Troubleshooting](TROUBLESHOOTING.md) for common configuration issues.

## Related Documentation

- [Configuration Defaults](CONFIGURATION_DEFAULTS.md) - Auto-generated from source code
- [Best Practices](BEST_PRACTICES.md) - Configuration recommendations
- [Performance Tuning](PERFORMANCE_TUNING.md) - Performance optimization
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues

