# P2P Governance Messages

## Overview

Bitcoin Commons nodes relay governance messages through the P2P network, enabling decentralized governance communication without requiring direct connection to the governance infrastructure. Nodes forward governance messages to other peers and optionally to the governance application.

## Architecture

### Message Flow

```
Node
    │
    ├─→ P2P Network (Bitcoin Protocol)
    │   │
    │   ├─→ Node A (relays to peers)
    │   ├─→ Node B (relays to peers)
    │   └─→ Node C (relays to peers)
    │
    └─→ Governance Application (blvm-commons)
        (if governance relay enabled)
```

### Two-Mode Operation

1. **Gossip Mode**: Messages relayed to governance-enabled peers only
2. **Relay Mode**: Messages forwarded to governance application via VPN/API

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs#L731-L848)

## Governance Message Types


**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs#L1049-L1100)

## Gossip Protocol

### Peer Selection

Nodes gossip governance messages to:
- Governance-enabled peers only
- Excluding the sender
- Using Bitcoin P2P protocol

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs#L805-L848)

### Message Serialization

Messages are serialized using JSON for gossip:

```rust
let msg_json = serde_json::to_vec(msg)?;
peer.send_message(msg_json).await?;
```

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs#L829-L844)

## Governance Relay

### Configuration

```toml
[governance]
enabled = true
commons_url = "https://commons.example.com/api"
vpn_enabled = true
```

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs#L486-L559)

### Relay Process

1. **Receive Message**: Node receives governance message from peer
2. **Check Configuration**: Verify governance relay enabled
3. **Forward to Commons**: Send message to governance application via API
4. **Gossip to Peers**: Also gossip message to other governance-enabled peers

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs#L731-L803)

## Message Deduplication

### Duplicate Detection

The governance application deduplicates messages:

- **Message ID**: Unique identifier per message
- **Sender Tracking**: Tracks message origin
- **Timestamp**: Prevents replay attacks

**Code**: [message_dedup.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/governance/message_dedup.rs#L1-L200)

## P2P Receiver

### Message Processing

The governance application receives messages via P2P receiver:

- **HTTP Endpoint**: Receives forwarded messages
- **Validation**: Validates message structure
- **Storage**: Stores messages in database
- **Processing**: Processes governance actions

**Code**: [p2p_receiver.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/governance/p2p_receiver.rs#L1-L28)

## Network Integration

### Protocol Messages

Governance messages are integrated into Bitcoin P2P protocol:

- **Message Types**: New protocol message types for governance
- **Backward Compatible**: Non-governance nodes ignore messages
- **Service Flags**: Nodes advertise governance capability

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/protocol.rs#L1-L200)

### Peer Management

Nodes track governance-enabled peers:

- **Service Flags**: Identify governance-capable peers
- **Peer List**: Maintain list of governance peers
- **Connection Management**: Handle peer connections/disconnections

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs#L814-L848)

## Benefits

1. **Decentralization**: Governance messages flow through P2P network
2. **Resilience**: No single point of failure
3. **Privacy**: Messages relayed without revealing origin
4. **Scalability**: Gossip protocol scales to many nodes
5. **Backward Compatibility**: Non-governance nodes unaffected

## Components

The P2P governance message system includes:
- Governance message types (registration, veto, status, fork decision)
- Gossip protocol for peer-to-peer relay
- Governance relay to application
- Message deduplication
- P2P receiver in governance application
- Network protocol integration

**Location**: `blvm-node/src/network/mod.rs`, `blvm-node/src/network/protocol.rs`, `blvm-commons/src/governance/p2p_receiver.rs`, `blvm-commons/src/governance/message_dedup.rs`

