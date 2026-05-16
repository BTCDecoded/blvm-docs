# Stratum V2 Mining Protocol

## Overview

The Stratum V2 mining stack is implemented primarily in the **`blvm-stratum-v2`** module repository (pool/server/protocol). The reference node integrates **P2P-side** handling: TLV-shaped bytes on the Bitcoin transport can be demuxed into `NetworkMessage::StratumV2MessageReceived` for the Stratum module. **Dedicated miner TCP** is bound only by **`blvm-stratum-v2`**, not by the node process.

**Merge mining** is a separate optional plugin (`blvm-merge-mining`) that depends on the Stratum V2 module.

## Where the code lives

| Piece | Repository / path |
|-------|-------------------|
| Protocol, messages, pool, server, module API | **[blvm-stratum-v2](https://github.com/BTCDecoded/blvm-stratum-v2)** (`src/protocol.rs`, `messages.rs`, `pool.rs`, `server.rs`, `module.rs`, `config.rs`) |
| Node: P2P TLV demux → `StratumV2MessageReceived` | **[network_manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_manager.rs)** (`stratum-v2` feature) |
| Node: `StratumV2Config`, `[stratum_v2]` in config | **[config/rpc.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/rpc.rs)** (type), **[config/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs)** (top-level config) |

## Stratum V2 Protocol

### Protocol features

- **Binary protocol**: TLV framing (see module `messages` / `protocol`)
- **Server and pool**: Implemented in **`blvm-stratum-v2`** ([server.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/server.rs), [pool.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/pool.rs))
- **Message encoding**: [protocol.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/protocol.rs), [messages.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/messages.rs)

### Dedicated miner TCP (module)

Miners connect to **`blvm-stratum-v2`**’s configured `listen_addr`. The node does **not** run `stratum_v2_listener`; parity framing is documented in the umbrella **`docs/STRATUM_V2_DECOUPLING_PLAN.md`**.

### P2P ingress

When the `stratum-v2` feature is enabled, the network layer may detect Stratum V2 TLV on P2P bytes and emit **`NetworkMessage::StratumV2MessageReceived`** for dispatch to modules.

**Code**: [network_manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_manager.rs), [network_message_dispatch.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_message_dispatch.rs), [network/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs) (message variants)

### Transport

Mining traffic uses the same transport stack as P2P; see [Transport abstraction](transport-abstraction.md).

**Code**: [transport.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/transport.rs)

## Merge mining (optional plugin)

**Merge mining is not part of the core node.** It is provided by **`blvm-merge-mining`**, which builds on **`blvm-stratum-v2`**.

- **Requires** the Stratum V2 module
- **Activation fee / revenue model**: see module and marketplace docs

### Documentation

- [Module system](../modules/overview.md)
- Merge-mining module repository (if present in your workspace): `blvm-merge-mining`

## Configuration

```toml
[stratum_v2]
enabled = true
pool_url = "tcp://pool.example.com:3333"  # or "iroh://<nodeid>"
# Dedicated miner TCP: set on the module; same key in node config is merge-mining / informational
listen_addr = "0.0.0.0:3333"
```

**Code**: [StratumV2Config](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/rpc.rs)

## Usage

Integrate via the **`blvm-stratum-v2`** crate as a **node module** ([`StratumV2Module`](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/module.rs), [lib.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/lib.rs)). Older snippets that imported `blvm_node::network::stratum_v2::StratumV2Server` are obsolete; use the module’s examples and the shared `[stratum_v2]` keys above (**miner TCP is bound by the module**, not by `blvm-node`).

## Benefits

1. **Bandwidth**: Stratum V2 binary framing vs Stratum V1 text
2. **Modularity**: Server/pool logic and **miner `listen_addr`** live in **`blvm-stratum-v2`**; the node provides chain APIs, optional P2P Stratum TLV demux, and **`NodeAPI`** (including **`send_peer_transport_payload`** for peer-oriented bytes)
3. **Optional merge mining**: Separate commercial module

## See also

- [Mining integration](mining.md)
- [Modules overview](../modules/overview.md)
- [Stratum V2 module](../modules/stratum-v2.md)
