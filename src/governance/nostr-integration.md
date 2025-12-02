# Nostr Integration

## Overview

Bitcoin Commons uses Nostr (Notes and Other Stuff Transmitted by Relays) for real-time transparency and decentralized governance communication. The system includes a multi-bot architecture for different types of announcements and status updates.

## Purpose

Nostr integration serves as a transparency mechanism by:
- Publishing real-time governance status updates
- Providing public verification of server operations
- Enabling decentralized monitoring of governance events
- Creating an immutable public record of governance actions

## Multi-Bot System

### Bot Types

The system uses multiple bot identities for different purposes:

- **gov**: Governance announcements and status updates
- **dev**: Development updates and technical information
- **research**: Educational content (optional)
- **network**: Network metrics and statistics (optional)

**Code**: ```1:60:bllvm-commons/src/nostr/bot_manager.rs```

### Bot Configuration

```toml
[nostr.bots.gov]
nsec_path = "env:GOV_BOT_NSEC"  # or file path
npub = "npub1..."
lightning_address = "gov@bitcoincommons.org"

[nostr.bots.gov.profile]
name = "@BTCCommons_Gov"
about = "Bitcoin Commons Governance Bot"
picture = "https://bitcoincommons.org/logo.png"
```

**Code**: ```38:51:bllvm-commons/src/config.rs```

## Nostr Client

### Client Implementation

The `NostrClient` manages connections to multiple Nostr relays:

- **Multi-Relay Support**: Connects to multiple relays for redundancy
- **Event Publishing**: Publishes events to all connected relays
- **Error Handling**: Handles relay failures gracefully
- **Retry Logic**: Automatic retry for failed publishes

**Code**: ```1:200:bllvm-commons/src/nostr/client.rs```

### Relay Management

```rust
let client = NostrClient::new(nsec, relay_urls).await?;
client.publish_event(event).await?;
```

**Code**: ```24:52:bllvm-commons/src/nostr/client.rs```

## Event Types

### Governance Status Events (Kind 30078)

Published hourly by each authorized server:
- Server health status
- Binary and config hashes
- Audit log status
- Tagged with `d:governance-status`

**Code**: ```1:200:bllvm-commons/src/nostr/events.rs```

### Server Health Events (Kind 30079)

Published when server status changes:
- Uptime metrics
- Last merge information
- Operational status
- Tagged with `d:server-health`

**Code**: ```1:200:bllvm-commons/src/nostr/events.rs```

### Audit Log Head Events (Kind 30080)

Published when audit log head changes:
- Current audit log head hash
- Entry count
- Tagged with `d:audit-head`

**Code**: ```1:200:bllvm-commons/src/nostr/events.rs```

### Governance Action Events

Published for governance actions:
- PR merges
- Review period notifications
- Keyholder announcements
- Economic node registrations

**Code**: ```1:200:bllvm-commons/src/nostr/governance_publisher.rs```

## Governance Publisher

### Status Publishing

The `StatusPublisher` publishes governance status:

- **Hourly Updates**: Regular status updates
- **Event Signing**: Events signed with server key
- **Multi-Relay**: Published to multiple relays
- **Error Recovery**: Handles relay failures

**Code**: ```1:200:bllvm-commons/src/nostr/publisher.rs```

### Action Publishing

The `GovernanceActionPublisher` publishes governance actions:

- **PR Events**: Merge and review events
- **Keyholder Events**: Signature announcements
- **Economic Node Events**: Registration and veto events
- **Fork Events**: Governance fork decisions

**Code**: ```1:200:bllvm-commons/src/nostr/governance_publisher.rs```

## Zap Tracking

### Zap Contributions

Zaps are tracked for contribution-based voting:

- **Zap Tracker**: Monitors Nostr zaps
- **Contribution Recording**: Records zap contributions
- **Vote Conversion**: Converts zaps to votes
- **Real-Time Processing**: Processes zaps as received

**Code**: ```1:281:bllvm-commons/src/nostr/zap_tracker.rs```

### Zap-to-Vote

Zaps to governance events become votes:

- **Proposal Zaps**: Zaps to governance event IDs
- **Vote Weight**: Calculated using quadratic formula
- **Vote Type**: Extracted from zap message
- **Database Storage**: Stored in proposal_zap_votes table

**Code**: ```1:293:bllvm-commons/src/nostr/zap_voting.rs```

## Configuration

```toml
[nostr]
enabled = true
relays = [
    "wss://relay.bitcoincommons.org",
    "wss://nostr.bitcoincommons.org"
]
publish_interval_secs = 3600  # 1 hour
governance_config = "commons_mainnet"

[nostr.bots.gov]
nsec_path = "env:GOV_BOT_NSEC"
npub = "npub1..."
lightning_address = "gov@bitcoincommons.org"
```

**Code**: ```25:51:bllvm-commons/src/config.rs```

## Real-Time Transparency

### Public Monitoring

Anyone can monitor governance via Nostr:

- **Event Filtering**: Filter by event kind and tags
- **Relay Queries**: Query any Nostr relay
- **Real-Time Updates**: Receive updates as they happen
- **Verification**: Verify event signatures

### Event Verification

All events are signed:

- **Server Keys**: Each server has Nostr keypair
- **Event Signing**: Events signed with server key
- **Public Verification**: Anyone can verify signatures
- **Tamper-Evident**: Cannot modify events without breaking signature

## Benefits

1. **Decentralization**: No single point of failure
2. **Censorship Resistance**: Multiple relays, no central authority
3. **Real-Time**: Immediate status updates
4. **Public Verification**: Anyone can verify events
5. **Transparency**: Complete public record of governance actions

## Components

The Nostr integration includes:
- Multi-bot manager
- Nostr client with multi-relay support
- Event types (status, health, audit, actions)
- Governance publisher
- Status publisher
- Zap tracker and voting processor

**Location**: `bllvm-commons/src/nostr/`

