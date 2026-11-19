# Transaction relay

Dandelion++ is transaction relay in the default `blvm` build. FIBRE is block relay in the [`blvm-fibre` module](../modules/fibre.md). Package relay is a separate page: [Package relay (BIP331)](package-relay.md).

## Dandelion++

A transaction first walks a short random path (the stem), then floods (the fluff). Each stem draws its own deadline from `stem_timeout_seconds` up to one and a half times that value. The defaults are a 10 second base, a 10% chance to fluff at each hop, and 2 hops. `[relay].enable_dandelion` turns it on. `--enable-dandelion` does the same when the binary includes the feature.

```toml
[relay]
enable_dandelion = true

[dandelion]
stem_timeout_seconds = 10
fluff_probability = 0.1
max_stem_hops = 2
```

## FIBRE block relay (module)

FIBRE (Fast Internet Bitcoin Relay Engine) is **block** transport over UDP with FEC: not transaction propagation.

- **Operator path:** load **`blvm-fibre`** ([FIBRE module](../modules/fibre.md)): outbound on `NewBlock` / `BlockMined`, inbound via `queue_received_block_bytes`.
- **Node support:** advertises **`NODE_FIBRE`** on P2P and publishes **`CompanionUdpPeerRegistered`** / **`CompanionUdpPeerUnregistered`** when peers advertise FIBRE (companion UDP = peer TCP port + 1) so the module can register dynamic peers.


There is **no** in-node `network/fibre.rs` or `[network.fibre]` configuration table.

## Integration

### Relay Manager

The `RelayManager` coordinates relay protocols:

- Standard block/transaction relay
- Dandelion++ integration (optional `dandelion` feature + `[relay].enable_dandelion`)
- Package relay (optional; see [Package Relay (BIP331)](package-relay.md))

FIBRE block relay runs in the **`blvm-fibre`** module process, not inside `RelayManager`.


### Protocol Selection

Relay protocols are selected based on:

- Compile-time features (`dandelion`, etc.)
- Peer capabilities
- Configuration settings
- Runtime preferences


## Components

- Dandelion++ stem/fluff phase management
- Relay manager coordination
- P2P `NODE_FIBRE` service bit and companion-UDP events for modules

## Source

- [network_manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_manager.rs) (companion UDP events), [blvm-fibre](https://github.com/BTCDecoded/blvm-fibre) (UDP/FEC relay)
- [relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/relay.rs)
- [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs)

