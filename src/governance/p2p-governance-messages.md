# P2P Governance Messages

## Overview

Bitcoin Commons nodes relay governance messages through the P2P network, enabling decentralized governance communication without requiring direct connection to the governance infrastructure. Nodes forward governance messages to other peers and optionally to the governance application.

## Architecture

### Message Flow

```
Economic Node
    │
    ├─→ P2P Network (Bitcoin Protocol)
    │   │
    │   ├─→ Node A (relays to peers)
    │   ├─→ Node B (relays to peers)
    │   └─→ Node C (relays to peers)
    │
    └─→ Governance Application (bllvm-commons)
        (if governance relay enabled)
```

### Two-Mode Operation

1. **Gossip Mode**: Messages relayed to governance-enabled peers only
2. **Relay Mode**: Messages forwarded to governance application via VPN/API

**Code**: ```731:848:bllvm-node/src/network/mod.rs```

## Governance Message Types

### EconomicNodeRegistration

Economic node registration messages:

- **Purpose**: Register economic nodes on the network
- **Fields**: Node type, entity name, message ID
- **Relay**: Gossiped to peers, optionally forwarded to governance app

**Code**: ```731:803:bllvm-node/src/network/mod.rs```

### EconomicNodeVeto

Economic node veto messages:

- **Purpose**: Signal veto for Tier 3+ proposals
- **Fields**: PR ID, signal type, message ID
- **Relay**: Gossiped to peers, optionally forwarded to governance app

**Code**: ```850:950:bllvm-node/src/network/mod.rs```

### EconomicNodeStatus

Economic node status query messages:

- **Purpose**: Query economic node status
- **Fields**: Request ID, query parameters
- **Relay**: Forwarded to governance app, response sent back to peer

**Code**: ```950:1047:bllvm-node/src/network/mod.rs```

### EconomicNodeForkDecision

Governance fork decision messages:

- **Purpose**: Signal fork decision (ruleset choice)
- **Fields**: Chosen ruleset, message ID
- **Relay**: Gossiped to peers, optionally forwarded to governance app

**Code**: ```1049:1100:bllvm-node/src/network/mod.rs```

## Gossip Protocol

### Peer Selection

Nodes gossip governance messages to:
- Governance-enabled peers only
- Excluding the sender
- Using Bitcoin P2P protocol

**Code**: ```805:848:bllvm-node/src/network/mod.rs```

### Message Serialization

Messages are serialized using JSON for gossip:

```rust
let msg_json = serde_json::to_vec(msg)?;
peer.send_message(msg_json).await?;
```

**Code**: ```829:844:bllvm-node/src/network/mod.rs```

## Governance Relay

### Configuration

```toml
[governance]
enabled = true
commons_url = "https://commons.example.com/api"
vpn_enabled = true
```

**Code**: ```486:559:bllvm-node/src/config/mod.rs```

### Relay Process

1. **Receive Message**: Node receives governance message from peer
2. **Check Configuration**: Verify governance relay enabled
3. **Forward to Commons**: Send message to governance application via API
4. **Gossip to Peers**: Also gossip message to other governance-enabled peers

**Code**: ```731:803:bllvm-node/src/network/mod.rs```

## Message Deduplication

### Duplicate Detection

The governance application deduplicates messages:

- **Message ID**: Unique identifier per message
- **Sender Tracking**: Tracks message origin
- **Timestamp**: Prevents replay attacks

**Code**: ```1:200:bllvm-commons/src/governance/message_dedup.rs```

## P2P Receiver

### Message Processing

The governance application receives messages via P2P receiver:

- **HTTP Endpoint**: Receives forwarded messages
- **Validation**: Validates message structure
- **Storage**: Stores messages in database
- **Processing**: Processes governance actions

**Code**: ```1:28:bllvm-commons/src/governance/p2p_receiver.rs```

## Network Integration

### Protocol Messages

Governance messages are integrated into Bitcoin P2P protocol:

- **Message Types**: New protocol message types for governance
- **Backward Compatible**: Non-governance nodes ignore messages
- **Service Flags**: Nodes advertise governance capability

**Code**: ```1:200:bllvm-node/src/network/protocol.rs```

### Peer Management

Nodes track governance-enabled peers:

- **Service Flags**: Identify governance-capable peers
- **Peer List**: Maintain list of governance peers
- **Connection Management**: Handle peer connections/disconnections

**Code**: ```814:848:bllvm-node/src/network/mod.rs```

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

**Location**: `bllvm-node/src/network/mod.rs`, `bllvm-node/src/network/protocol.rs`, `bllvm-commons/src/governance/p2p_receiver.rs`, `bllvm-commons/src/governance/message_dedup.rs`

