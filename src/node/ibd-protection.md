# IBD Bandwidth Protection

## Overview

The node implements comprehensive protection against Initial Block Download (IBD) bandwidth exhaustion attacks. This prevents malicious peers from forcing a node to upload the entire blockchain multiple times, which could cause ISP data cap overages and economic denial-of-service.

## Protection Mechanisms

### Per-Peer Bandwidth Limits

Tracks bandwidth usage per peer with configurable daily and hourly limits:

- **Daily Limit**: Maximum bytes a peer can request per day
- **Hourly Limit**: Maximum bytes a peer can request per hour
- **Automatic Throttling**: Blocks requests when limits are exceeded
- **Legitimate Node Protection**: First request always allowed, reasonable limits for legitimate sync

**Code**: [ibd_protection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/ibd_protection.rs#L265-L350)

### Per-IP Bandwidth Limits

Tracks bandwidth usage per IP address to prevent single-IP attacks:

- **IP-Based Tracking**: Monitors all peers from the same IP
- **Aggregate Limits**: Combined daily/hourly limits for all peers from an IP
- **Attack Detection**: Identifies coordinated attacks from single IP

**Code**: [ibd_protection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/ibd_protection.rs#L350-L450)

### Per-Subnet Bandwidth Limits

Tracks bandwidth usage per subnet to prevent distributed attacks:

- **IPv4 Subnets**: Tracks /24 subnets (256 addresses)
- **IPv6 Subnets**: Tracks /64 subnets
- **Subnet Aggregation**: Combines bandwidth from all IPs in subnet
- **Distributed Attack Mitigation**: Prevents coordinated attacks from subnet

**Code**: [ibd_protection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/ibd_protection.rs#L450-L550)

### Concurrent IBD Serving Limits

Limits how many peers can simultaneously request IBD:

- **Concurrent Limit**: Maximum number of peers serving IBD at once
- **Queue Management**: Queues additional requests when limit reached
- **Fair Serving**: Rotates serving to queued peers

**Code**: [ibd_protection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/ibd_protection.rs#L550-L600)

### Peer Reputation Scoring

Tracks peer behavior to identify malicious patterns:

- **Reputation System**: Scores peers based on behavior
- **Suspicious Pattern Detection**: Identifies rapid reconnection with new peer IDs
- **Cooldown Periods**: Enforces cooldown after suspicious activity
- **Legitimate Node Protection**: First-time sync always allowed

**Code**: [ibd_protection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/ibd_protection.rs#L600-L650)

## Configuration

### Default Limits

```toml
[network.ibd_protection]
max_bandwidth_per_peer_per_day_gb = 10.0
max_bandwidth_per_peer_per_hour_gb = 2.0
max_bandwidth_per_ip_per_day_gb = 50.0
max_bandwidth_per_ip_per_hour_gb = 10.0
max_bandwidth_per_subnet_per_day_gb = 200.0
max_bandwidth_per_subnet_per_hour_gb = 50.0
max_concurrent_ibd_serving = 3
ibd_request_cooldown_seconds = 3600
```

### Configuration Options

- **max_bandwidth_per_peer_per_day_gb**: Daily limit per peer (default: 10 GB)
- **max_bandwidth_per_peer_per_hour_gb**: Hourly limit per peer (default: 2 GB)
- **max_bandwidth_per_ip_per_day_gb**: Daily limit per IP (default: 50 GB)
- **max_bandwidth_per_ip_per_hour_gb**: Hourly limit per IP (default: 10 GB)
- **max_bandwidth_per_subnet_per_day_gb**: Daily limit per subnet (default: 200 GB)
- **max_bandwidth_per_subnet_per_hour_gb**: Hourly limit per subnet (default: 50 GB)
- **max_concurrent_ibd_serving**: Maximum concurrent IBD serving (default: 3)
- **ibd_request_cooldown_seconds**: Cooldown period after suspicious activity (default: 3600 seconds)

**Code**: [ibd_protection.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/ibd_protection.rs#L209-L264)

## Attack Mitigation

### Single IP Attack

**Attack**: Attacker runs multiple fake nodes from same IP
**Protection**: Per-IP bandwidth limits aggregate all peers from IP
**Result**: Blocked after IP limit reached

### Subnet Attack

**Attack**: Attacker distributes fake nodes across subnet
**Protection**: Per-subnet bandwidth limits aggregate all IPs in subnet
**Result**: Blocked after subnet limit reached

### Rapid Reconnection Attack

**Attack**: Attacker disconnects and reconnects with new peer ID
**Protection**: Reputation scoring detects pattern, enforces cooldown
**Result**: Blocked during cooldown period

### Distributed Attack

**Attack**: Coordinated attack from multiple IPs/subnets
**Protection**: Concurrent serving limits prevent serving too many peers simultaneously
**Result**: Additional requests queued, serving rotated fairly

### Legitimate New Node

**Scenario**: Legitimate new node requests full sync
**Protection**: First request always allowed, reasonable limits accommodate legitimate sync
**Result**: Allowed to sync within limits

## Integration

The IBD protection is automatically integrated into the network manager:

- **Automatic Tracking**: Tracks bandwidth when serving Headers/Block messages
- **Request Protection**: Protects GetHeaders and GetData requests
- **Cleanup**: Automatically cleans up tracking on peer disconnect

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs#L604-L650)

## LAN Peer Prioritization

LAN peers are automatically discovered and prioritized for IBD, but still respect bandwidth protection limits:

- **Priority Assignment**: LAN peers get priority within bandwidth limits
- **Score Multiplier**: LAN peers receive up to 3x score multiplier (progressive trust system)
- **Bandwidth Limits**: LAN peers still respect per-peer, per-IP, and per-subnet limits
- **Reputation Scoring**: LAN peer behavior affects reputation scoring

**Code**: [parallel_ibd.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L680-L800)

For details on LAN peering discovery, security, and configuration, see [LAN Peering System](lan-peering.md).

## See Also

- [LAN Peering System](lan-peering.md) - Automatic local network discovery and prioritization
- [Network Operations](operations.md) - General network operations
- [Node Configuration](configuration.md) - IBD protection configuration
- [Security Controls](../security/security-controls.md) - Security system overview
