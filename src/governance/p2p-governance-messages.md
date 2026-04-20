# P2P governance-related extensions

## Overview

The node can advertise **governance-related P2P capability** via the `NODE_GOVERNANCE` service bit in `Version.services`. Peers use that flag to identify nodes that participate in **Commons-oriented extensions** (for example **ban list sharing**: `getbanlist` / `banlist`). Relay and forwarding behavior are implemented in `blvm-node` networking code and gated by node configuration.

## Architecture

### Capability and peers

- Nodes set **`NODE_GOVERNANCE`** when configured to advertise this capability (see service flags / node config).
- **`PeerManager`** can track peers that advertised the governance bit for features that need governance-capable peers (e.g. ban-list gossip).

### Concrete protocol surface today

- **Ban list sharing**: `GetBanList` / `BanList` (and the corresponding framed command strings) are part of the shared protocol stack.
- Other P2P commands follow the node’s **allowlisted** command set in `network/protocol.rs` and `blvm-protocol`’s `node_tcp` / wire layers.

### Configuration

Optional `[governance]` settings in the node (e.g. `commons_url`, relay toggles) control whether the node forwards or integrates with **blvm-commons**-side HTTP APIs. Exact fields change over time; see the live [configuration reference](../reference/configuration-reference.md) and `blvm-node` `config` sources.

## Code references

| Area | Location |
|------|----------|
| Service flag | `blvm-protocol` / `blvm-node` `NODE_GOVERNANCE` |
| Framed commands & `ProtocolMessage` | `blvm-node/src/network/protocol.rs`, `blvm-protocol/src/node_tcp.rs` |
| Peer selection for governance bit | `blvm-node/src/network/peer_manager.rs` (`governance` feature) |

## See also

- [Node overview](../node/overview.md) — networking and configuration entry points
- [Module system](../architecture/module-system.md#event-system) — `EventType` / governance-related **events** (proposal lifecycle, webhooks, fork detection)
