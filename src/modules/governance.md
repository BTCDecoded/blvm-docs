# Governance Module

## Overview

The Governance module (`blvm-governance`) integrates governance functionality for blvm-node: webhook notifications to [blvm-commons](../governance/overview.md), [economic node tracking](../governance/economic-nodes.md), [veto system integration](../governance/economic-nodes.md#veto-mechanism), and governance proposal monitoring. For information on developing custom modules, see [Module Development](../sdk/module-development.md).

## Features

- **Webhook Notifications**: Sends governance events to blvm-commons via webhooks
- **Economic Node Tracking**: Tracks economic node status and contributions
- **Veto System Integration**: Monitors and reports veto threshold status
- **Governance Proposal Monitoring**: Tracks governance proposals from creation to merge

## Installation

### Via Cargo

```bash
cargo install blvm-governance
```

### Via Module Installer

```bash
cargo install cargo-blvm-module
cargo blvm-module install blvm-governance
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-governance.git
   cd blvm-governance
   ```

2. Build the module:
   ```bash
   cargo build --release
   ```

3. Install to node modules directory:
   ```bash
   mkdir -p /path/to/node/modules/blvm-governance/target/release
   cp target/release/blvm-governance /path/to/node/modules/blvm-governance/target/release/
   ```

## Configuration

Create a `config.toml` file in the module directory:

```toml
[governance]
# Webhook URL for blvm-commons integration
webhook_url = "https://governance.example.com/webhook"

# Node identifier for governance tracking
node_id = "your_node_id"

# Enable/disable module
enabled = true
```

### Configuration Options

- `webhook_url` (required): URL for sending webhook notifications to blvm-commons
- `node_id` (required): Unique identifier for this node in the governance system
- `enabled` (default: `true`): Enable or disable the module

## Module Manifest

The module includes a `module.toml` manifest (see [Module Development](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-governance"
version = "0.1.0"
description = "Governance webhook and economic node tracking module"
author = "Bitcoin Commons Team"
entry_point = "blvm-governance"

capabilities = [
    "read_blockchain",
    "subscribe_events",
]
```

## Events

### Subscribed Events

The module subscribes to the following node events:

- `GovernanceProposalCreated` - New governance proposal created
- `GovernanceProposalVoted` - Vote cast on governance proposal
- `GovernanceProposalMerged` - Governance proposal merged
- `EconomicNodeRegistered` - Economic node registered in governance system
- `EconomicNodeVeto` - Economic node veto signal received
- `ChainTipUpdated` - Chain tip updated (for tracking block height)

### Published Events

The module publishes the following events:

- `WebhookSent` - Webhook notification successfully sent to blvm-commons
- `WebhookFailed` - Webhook delivery failed (with error details)
- `VetoThresholdReached` - Economic node veto threshold reached
- `GovernanceForkDetected` - Governance fork detected

## Webhook Integration

The module sends webhook notifications to blvm-commons for:

- Governance proposal lifecycle events
- Economic node registration and status changes
- Veto threshold status
- Governance fork detection

Webhook payloads include:
- Event type and timestamp
- Node identifier
- Event-specific data (proposal details, node status, etc.)
- Cryptographic signatures for verification

## Economic Node Tracking

The module tracks economic node status including:

- Node registration status
- Contribution tracking (merge mining, fee forwarding, zaps, marketplace)
- Veto eligibility and status
- Governance participation metrics

## Veto System Integration

The module monitors veto signals from economic nodes and:

- Tracks veto threshold status
- Publishes events when veto threshold is reached
- Sends webhook notifications for veto events

## Usage

Once installed and configured, the module automatically:

1. Subscribes to governance-related events from the node
2. Tracks economic node status and contributions
3. Monitors governance proposals and votes
4. Sends webhook notifications to blvm-commons
5. Publishes governance events for other modules

## API Integration

The module integrates with the node via the Node API IPC protocol:

- **Read-only blockchain access**: Queries blockchain data for governance tracking
- **Event subscription**: Receives real-time governance events from the node
- **Event publication**: Publishes governance-specific events

## Troubleshooting

### Module Not Loading

- Verify the module binary exists at the correct path
- Check `module.toml` manifest is present and valid
- Verify module has required capabilities
- Check node logs for module loading errors

### Webhook Delivery Failing

- Verify webhook URL is correct and accessible
- Check network connectivity to blvm-commons
- Verify node_id is correctly configured
- Check node logs for webhook delivery errors

### Economic Node Tracking Not Working

- Verify node has `read_blockchain` capability
- Check that governance events are being published by the node
- Verify node_id matches governance system records
- Check node logs for tracking errors

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [Governance Overview](../governance/overview.md) - Governance system documentation
- [Economic Nodes](../governance/economic-nodes.md) - Economic node system documentation
- [PR Process](../development/pr-process.md) - Governance tiers and PR review process


