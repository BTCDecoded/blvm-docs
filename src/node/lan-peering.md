# LAN Peering System

## Overview

The LAN peering system automatically discovers and prioritizes local network (LAN) Bitcoin nodes for faster Initial Block Download (IBD) while maintaining security through checkpoint validation and peer diversity requirements. This can speed up IBD by **10-50x** when a local Bitcoin node is available on your network.

## Benefits

- **10-50x IBD Speedup**: LAN peers typically have <10ms latency vs 100-5000ms for internet peers
- **High Throughput**: ~1 Gbps local network vs ~10-100 Mbps internet
- **100% Reliability**: No connection drops compared to internet peers
- **Automatic Discovery**: Scans local network automatically during startup
- **Secure by Default**: Internet checkpoint validation prevents eclipse attacks

## How It Works

### Automatic Discovery

During node startup, the system automatically:

1. **Detects Local Network Interfaces**: Identifies private network interfaces (10.x, 172.16-31.x, 192.168.x)
2. **Scans Local Subnet**: Scans /24 subnets (254 IPs per subnet) for Bitcoin nodes on port 8333
3. **Parallel Scanning**: Uses up to 64 concurrent connection attempts for fast discovery
4. **Verifies Peers**: Performs protocol handshake and chain verification before accepting

**Code**: [lan_discovery.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_discovery.rs#L1-L333)

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

**Code**: [peer_scoring.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/peer_scoring.rs#L26-L50)

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

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L89-L217)

### Peer Prioritization

LAN peers receive priority for block downloads during IBD:

- **IBD Optimization**: LAN peers get priority chunks (first 50,000 blocks)
- **Header Download**: LAN peers prioritized for header sync (10-100x faster)
- **Score Multiplier**: Up to 3x score multiplier for peer selection
- **Bandwidth Allocation**: LAN peers receive more bandwidth allocation

**Code**: [parallel_ibd.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd.rs#L680-L800)

## Security Model

### Hard Limits

The system enforces strict security limits to prevent eclipse attacks:

- **Maximum 25% LAN Peers**: Hard cap on LAN peer percentage
- **Minimum 75% Internet Peers**: Required for security
- **Minimum 3 Internet Peers**: Required for checkpoint validation
- **Maximum 1 Discovered LAN Peer**: Limits automatically discovered peers (whitelisted are separate)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L29-L51)

### Checkpoint Validation

Internet checkpoints are the **primary security mechanism**. Even with discovery enabled, eclipse attacks are prevented through regular checkpoint validation:

- **Block Checkpoints**: Every 1000 blocks, validate block hash against internet peers
- **Header Checkpoints**: Every 10000 blocks, validate header hash against internet peers
- **Consensus Requirement**: Requires agreement from at least 3 internet peers
- **Failure Response**: Checkpoint failure results in permanent ban (1 year)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L460-L690)

### Security Guarantees

1. **No Eclipse Attacks**: 75% internet peer minimum ensures honest network connection
2. **Checkpoint Validation**: Regular validation prevents chain divergence
3. **LAN Address Privacy**: LAN addresses are never advertised to external peers
4. **Progressive Trust**: New LAN peers start with limited trust
5. **Failure Handling**: Multiple failures result in demotion or ban

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L1-L51)

## Configuration

### Whitelisting

You can whitelist trusted LAN peers to start at maximum trust:

```rust
// Whitelisted peers start at maximum trust (3x multiplier)
policy.add_to_whitelist("192.168.1.100:8333".parse().unwrap());
```

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L245-L254)

### Discovery Control

LAN discovery is enabled by default. The system automatically discovers peers during startup, but you can control this behavior through the security policy.

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L232-L243)

## Use Cases

### Home Networks

If you run multiple Bitcoin nodes on your home network (e.g., Start9, Umbrel, RaspiBlitz), the system will automatically discover and prioritize them for faster sync.

**Example**: Node on `192.168.1.50` automatically discovers node on `192.168.1.100` and uses it for fast IBD.

### Docker/VM Environments

The system also checks common Docker/VM bridge networks:
- Docker default bridge: `172.17.0.1`
- Common VM network: `10.0.0.1`

**Code**: [lan_discovery.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_discovery.rs#L42-L60)

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

**Code**: [lan_discovery.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_discovery.rs#L94-L156)

### Checkpoint Failures

**Problem**: LAN peer is being banned due to checkpoint failures.

**Solutions**:
1. Verify LAN peer is on the correct chain (not a testnet/mainnet mismatch)
2. Verify internet peers are available (need at least 3 for validation)
3. Check network connectivity (LAN peer may be on different chain due to network issues)
4. Verify LAN peer is not malicious (check logs for checkpoint failure details)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L656-L688)

### Trust Level Not Increasing

**Problem**: LAN peer trust level is not increasing beyond initial.

**Solutions**:
1. Verify peer is actually sending valid blocks (check block validation logs)
2. Wait for required blocks (1000 for Level 2, 10000 for Maximum)
3. Verify connection time (Maximum trust requires 1 hour of connection)
4. Check for failures (3 failures result in demotion)

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L147-L193)

### Performance Issues

**Problem**: LAN peer is not providing expected speedup.

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

**Code**: [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs#L401-L404)

## See Also

- [IBD Bandwidth Protection](ibd-protection.md) - How LAN peers interact with bandwidth protection
- [Network Operations](operations.md) - General network operations
- [Security Threat Models](../security/threat-models.md#lan-peering-security) - Security model details
- [Node Configuration](configuration.md) - Configuration options
