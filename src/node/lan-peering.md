# LAN Peering System

## Overview

The LAN peering system automatically discovers and prioritizes local network (LAN) Bitcoin nodes for Initial Block Download (IBD), reducing sync time when a local node is available (lower latency than typical internet peers). Security is maintained through checkpoint validation and peer diversity requirements.

## Benefits

- **Lower latency**: LAN peers typically have much lower latency than internet peers
- **Local throughput**: Local network capacity is often higher than internet links
- **Stable connectivity**: LAN peers are not subject to internet path failures
- **Automatic Discovery**: Scans local network automatically during startup
- **Secure by Default**: Internet checkpoint validation prevents eclipse attacks

## How It Works

### Automatic Discovery

During node startup, the system automatically:

1. **Detects Local Network Interfaces**: Identifies private network interfaces (10.x, 172.16-31.x, 192.168.x)
2. **Scans Local Subnet**: Scans /24 subnets (254 IPs per subnet) for Bitcoin nodes on port 8333
3. **Parallel Scanning**: Uses up to 64 concurrent connection attempts for fast discovery
4. **Verifies Peers**: Performs protocol handshake and chain verification before accepting

**Code**: [lan_discovery.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_discovery.rs)

### LAN Peer Detection

A peer is considered a LAN peer if its IP address is in one of these ranges:

**IPv4 Private Ranges:**
- `10.0.0.0/8` - Class A private network
- `172.16.0.0/12` - Class B private network (172.16-31.x)
- `192.168.0.0/16` - Class C private network (most common for home networks)
- `127.0.0.0/8` - Loopback addresses
- `169.254.0.0/16` - Link-local addresses

**IPv6 Private Ranges:**
- `::1` - Loopback
- `fd00::/8` - Unique Local Addresses (ULA)
- `fe80::/10` - Link-local addresses

**Code**: [peer_scoring.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/peer_scoring.rs)

### Progressive Trust System

LAN peers start with limited trust and earn higher priority over time:

1. **Initial Trust** (1.5x multiplier):
   - Newly discovered LAN peers
   - Whitelisted peers start at maximum trust instead

2. **Level 2 Trust** (2.0x multiplier):
   - After 1000 valid blocks received
   - Indicates reliable peer behavior

3. **Maximum Trust** (3.0x multiplier):
   - After 10000 valid blocks **AND** 1 hour of connection time
   - Maximum priority for block downloads

4. **Demoted** (1.0x multiplier, no bonus):
   - After 3 failures
   - Loses LAN status but remains connected

5. **Banned** (0.0x multiplier, not used):
   - Checkpoint validation failure
   - Permanent ban (1 year duration)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

### Peer Prioritization

LAN peers receive priority for block downloads during IBD:

- **IBD Optimization**: LAN peers get priority chunks (first 50,000 blocks)
- **Header Download**: LAN peers prioritized for header sync
- **Score Multiplier**: Higher trust score for LAN peers in selection
- **Bandwidth Allocation**: LAN peers receive more bandwidth allocation

**Code**: [parallel_ibd/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)

## Security Model

### Hard Limits

The system enforces strict security limits to prevent eclipse attacks:

- **Maximum 25% LAN Peers**: Hard cap on LAN peer percentage
- **Minimum 75% Internet Peers**: Required for security
- **Minimum 3 Internet Peers**: Required for checkpoint validation
- **Maximum 1 Discovered LAN Peer**: Limits automatically discovered peers (whitelisted are separate)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

### Checkpoint Validation

Internet checkpoints are the **primary security mechanism**. Even with discovery enabled, eclipse attacks are prevented through regular checkpoint validation:

- **Block Checkpoints**: Every 1000 blocks, validate block hash against internet peers
- **Header Checkpoints**: Every 10000 blocks, validate header hash against internet peers
- **Consensus Requirement**: Requires agreement from at least 3 internet peers
- **Failure Response**: Checkpoint failure results in permanent ban (1 year)
- **Request Timeout**: 5 seconds per checkpoint request
- **Max Retries**: 3 retry attempts per checkpoint
- **Protocol Verify Timeout**: 5 seconds for protocol handshake verification
- **Headers Verify Timeout**: 10 seconds for headers verification
- **Max Header Divergence**: 6 blocks maximum divergence allowed

**Security Constants**:
- `BLOCK_CHECKPOINT_INTERVAL`: 1000 blocks
- `HEADER_CHECKPOINT_INTERVAL`: 10000 blocks
- `MIN_CHECKPOINT_PEERS`: 3 internet peers required
- `CHECKPOINT_FAILURE_BAN_DURATION`: 1 year (31,536,000 seconds)
- `CHECKPOINT_REQUEST_TIMEOUT`: 5 seconds
- `CHECKPOINT_MAX_RETRIES`: 3 retries
- `PROTOCOL_VERIFY_TIMEOUT`: 5 seconds
- `HEADERS_VERIFY_TIMEOUT`: 10 seconds
- `MAX_HEADER_DIVERGENCE`: 6 blocks

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs) (progressive trust and auto-trust thresholds)

### Security Guarantees

1. **No Eclipse Attacks**: 75% internet peer minimum ensures honest network connection
2. **Checkpoint Validation**: Regular validation prevents chain divergence
3. **LAN Address Privacy**: LAN addresses are never advertised to external peers
4. **Progressive Trust**: New LAN peers start with limited trust
5. **Failure Handling**: Multiple failures result in demotion or ban

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

## Configuration

### Whitelisting

You can whitelist trusted LAN peers to start at maximum trust:

```rust
// Whitelisted peers start at maximum trust
policy.add_to_whitelist("192.168.1.100:8333".parse().unwrap());
```

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

### Discovery Control

LAN discovery is enabled by default. The system automatically discovers peers during startup, but you can control this behavior through the security policy.

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

## Use Cases

### Home Networks

If you run multiple Bitcoin nodes on your home network (e.g., Start9, Umbrel, RaspiBlitz), the system can discover and prioritize them for IBD.

**Example**: Node on `192.168.1.50` automatically discovers node on `192.168.1.100` and uses it for fast IBD.

### Docker/VM Environments

The system also checks common Docker/VM bridge networks:
- Docker default bridge: `172.17.0.1`
- Common VM network: `10.0.0.1`

**Code**: [lan_discovery.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_discovery.rs)

### Local Development

For local development and testing, LAN peering speeds up blockchain sync when running multiple nodes locally.

## Troubleshooting

### LAN Peers Not Discovered

**Problem**: LAN peers are not being discovered automatically.

**Solutions**:
1. Verify both nodes are on the same network (check IP ranges)
2. Verify Bitcoin P2P port (default 8333) is open and accessible
3. Check firewall rules (local network traffic may be blocked)
4. Verify network interface detection (check logs for "Detected local interface")

**Code**: [lan_discovery.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_discovery.rs)

### Checkpoint Failures

**Problem**: LAN peer is being banned due to checkpoint failures.

**Solutions**:
1. Verify LAN peer is on the correct chain (not a testnet/mainnet mismatch)
2. Verify internet peers are available (need at least 3 for validation)
3. Check network connectivity (LAN peer may be on different chain due to network issues)
4. Verify LAN peer is not malicious (check logs for checkpoint failure details)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

### Trust Level Not Increasing

**Problem**: LAN peer trust level is not increasing beyond initial.

**Solutions**:
1. Verify peer is actually sending valid blocks (check block validation logs)
2. Wait for required blocks (1000 for Level 2, 10000 for Maximum)
3. Verify connection time (Maximum trust requires 1 hour of connection)
4. Check for failures (3 failures result in demotion)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

### Performance Issues

**Problem**: LAN peer is not being used or sync is slow.

**Solutions**:
1. Verify network speed (check actual bandwidth between nodes)
2. Check peer trust level (higher trust = more priority)
3. Verify peer is not demoted (check trust level in logs)
4. Check for network congestion (other traffic may affect performance)

## Integration with IBD Protection

LAN peers are integrated with the IBD bandwidth protection system:

- **Bandwidth Limits**: LAN peers still respect per-peer bandwidth limits
- **Priority Assignment**: LAN peers get priority within bandwidth limits
- **Reputation Scoring**: LAN peer behavior affects reputation scoring

See [IBD Bandwidth Protection](ibd-protection.md#lan-peer-prioritization) for details.

## Security Considerations

### Eclipse Attack Prevention

The 25% LAN peer cap and 75% internet peer minimum ensure that even if all LAN peers are malicious, the node maintains connection to the honest network through internet peers.

### Checkpoint Validation

Regular checkpoint validation ensures that LAN peers cannot diverge from the honest chain. Checkpoint failures result in immediate ban.

### LAN Address Privacy

LAN addresses are never advertised to external peers, preventing information leakage about your local network topology.

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)

## See Also

- [IBD Bandwidth Protection](ibd-protection.md) - How LAN peers interact with bandwidth protection
- [Network Operations](operations.md) - General network operations
- [Security Threat Models](../security/threat-models.md#lan-peering-security) - Security model details
- [Node Configuration](configuration.md) - Configuration options
