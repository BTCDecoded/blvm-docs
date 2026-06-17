# FIBRE module (`blvm-fibre`)

UDP/FEC **block** relay as a **loadable Commons module**. Distinct from Dandelion++ transaction relay in [Privacy relay](../node/privacy-relay.md).

## Overview

**blvm-fibre** implements FIBRE-style block transport:

- **Outbound:** on `NewBlock` / `BlockMined`, fetches the block via `NodeAPI::get_block`, FEC-encodes, and sends UDP chunks to registered FIBRE peers.
- **Inbound:** assembles chunks and enqueues raw block bytes via `NodeAPI::queue_received_block_bytes` (same validation path as P2P `BlockReceived`).

The node core advertises **`NODE_FIBRE`** on P2P and emits companion-UDP events when peers advertise FIBRE (UDP port = peer TCP port + 1) for dynamic peer registration.

Wire types and `FibreConfig` live in **`blvm-protocol`** (`fibre` feature). The module crate owns UDP, Reed–Solomon, and relay logic.

**Repository:** [BTCDecoded/blvm-fibre](https://github.com/BTCDecoded/blvm-fibre)

## Requirements

- `blvm-node` with modules enabled.
- Module listed in **`registry/modules.json`** (bootstrap via `enabled_modules` version pin) or built locally.
- Do **not** bind the same UDP port twice on one host (only one FIBRE listener per deployment unless ports are explicitly separated).

## Loading

Pin in `blvm.toml` (example):

```toml
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"

[enabled_modules]
blvm-fibre = "0.1.*"
```

Or place a release binary + `module.toml` on the module search path. See [Module catalog — Installing modules](overview.md#installing-modules).

## Configuration

Module `config.toml` (or `[modules.blvm-fibre]` overrides):

| Key | Purpose |
|-----|---------|
| `fibre.enabled` | Enable relay when `true` (nested `fibre` table / `FibreConfig`) |
| `udp_bind` | UDP listen `host:port` when not using TCP+1 follow mode (default `0.0.0.0:8334`) |
| `udp_follow_node_tcp_plus_one` | Listen on node P2P TCP port **+ 1** (node injects `MODULE_CONFIG_NODE_P2P_LISTEN_*` on spawn) |
| `register_peers_from_p2p` | Register peers that advertise `NODE_FIBRE` on P2P (UDP = peer TCP port + 1) |
| `[[fibre_peers]]` | Static outbound targets: `peer_id`, `udp_addr` |

FEC and timeout options are under the nested **`fibre`** table (`FibreConfig` in protocol), including **`fibre.enabled`**.

Example — follow node P2P port (mainnet P2P 8333 → FIBRE UDP 8334):

```toml
udp_follow_node_tcp_plus_one = true
register_peers_from_p2p = true
```

Example — static peer:

```toml
[[fibre_peers]]
peer_id = "relay-east"
udp_addr = "203.0.113.10:8334"
```

## Events

| Event | Module action |
|-------|----------------|
| `NewBlock` | `get_block` → encode → send to registered FIBRE peers |
| `BlockMined` | Same outbound path for locally mined blocks |
| `CompanionUdpPeerRegistered` | Optional dynamic peer registration from P2P |
| `CompanionUdpPeerUnregistered` | Remove dynamic peer |

## Capabilities (`module.toml`)

- `read_blockchain`
- `subscribe_events`
- `queue_inbound_block`

## Node vs module

| | Node core (`blvm-node`) | **`blvm-fibre` module** |
|--|--|--|
| FIBRE UDP/FEC | Not implemented in-process | Subprocess + IPC |
| P2P | Advertises `NODE_FIBRE`; companion UDP events | Registers peers; sends/receives UDP |
| Config | Module pins / `[modules.blvm-fibre]` | Module `config.toml` |
| Operator docs | [Privacy relay](../node/privacy-relay.md) | This page |

## Troubleshooting

| Symptom | Check |
|---------|--------|
| No outbound FIBRE sends | Peers registered? `NewBlock` firing? `get_block` returns block? |
| UDP bind fails | Port clash with P2P+1 or another FIBRE listener; firewall |
| Blocks not accepted from FIBRE | `queue_received_block_bytes` path; check module logs |
| Dynamic peers missing | `register_peers_from_p2p = true`; remote advertises `NODE_FIBRE` |

## See also

- [Privacy relay](../node/privacy-relay.md) — Dandelion++ and `NODE_FIBRE` peer registration
- [Module IPC Protocol](../architecture/module-ipc-protocol.md)
- [Building modules](../sdk/module-development.md)
