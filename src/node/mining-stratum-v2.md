# Stratum V2 Mining Protocol

## Overview

The Stratum V2 mining stack is implemented primarily in the **`blvm-stratum-v2`** module repository (pool/server/protocol). The reference node integrates a **TCP listener** that accepts Stratum V2 TLV frames and forwards them into the node’s network layer; optional `stratum-v2` feature hooks exist on the mining coordinator for a future client path.

**Merge mining** is a separate optional plugin (`blvm-merge-mining`) that depends on the Stratum V2 module.

## Where the code lives

| Piece | Repository / path |
|-------|-------------------|
| Protocol, messages, pool, server, module API | **[blvm-stratum-v2](https://github.com/BTCDecoded/blvm-stratum-v2)** (`src/protocol.rs`, `messages.rs`, `pool.rs`, `server.rs`, `module.rs`, `config.rs`) |
| Node: TCP listener → network queue | **[stratum_v2_listener.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2_listener.rs)** |
| Node: `StratumV2Config`, `[stratum_v2]` in config | **[config/rpc.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/rpc.rs)** (type), **[config/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs)** (top-level config) |

## Stratum V2 Protocol

### Protocol features

- **Binary protocol**: TLV framing (see module `messages` / `protocol`)
- **Server and pool**: Implemented in **`blvm-stratum-v2`** ([server.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/server.rs), [pool.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/pool.rs))
- **Message encoding**: [protocol.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/protocol.rs), [messages.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/messages.rs)

### Listener (reference node)

The node does **not** ship a full `blvm_node::network::stratum_v2::*` tree on `main` by default. Incoming miner connections are handled by the listener, which reads TLV frames and emits `NetworkMessage::StratumV2MessageReceived` for the rest of the stack.

**Code**: [stratum_v2_listener.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2_listener.rs), [network/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs) (message variants)

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
listen_addr = "0.0.0.0:3333"  # Server / listener mode
```

**Code**: [StratumV2Config](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/rpc.rs)

## Usage

Integrate via the **`blvm-stratum-v2`** crate as a **node module** ([`StratumV2Module`](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/module.rs), [lib.rs](https://github.com/BTCDecoded/blvm-stratum-v2/blob/main/src/lib.rs)). The snippets in older revisions that imported `blvm_node::network::stratum_v2::StratumV2Server` do not match the current on-disk layout; follow the module’s examples and the node’s `stratum_v2` config + listener wiring above.

## Benefits

1. **Bandwidth**: Stratum V2 binary framing vs Stratum V1 text
2. **Modularity**: Full server/pool logic in **`blvm-stratum-v2`**, node provides listener and config
3. **Optional merge mining**: Separate commercial module

## See also

- [Mining integration](mining.md)
- [Modules overview](../modules/overview.md)
- [Stratum V2 module](../modules/stratum-v2.md)
