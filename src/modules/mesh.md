# Commons Mesh Module

Payment-gated mesh overlay for **blvm-node**: route discovery, replay prevention, optional payment proofs, and subprocess ModuleAPI. Wire format and smoke tests live in the [blvm-mesh](https://github.com/BTCDecoded/blvm-mesh) repo (`docs/TRANSPORT.md`, `API.md`).

## Install

Build and place the binary under the node modules directory:

```bash
git clone https://github.com/BTCDecoded/blvm-mesh.git && cd blvm-mesh
cargo build --release
mkdir -p /path/to/data/modules/blvm-mesh/target/release
cp target/release/blvm-mesh /path/to/data/modules/blvm-mesh/target/release/
```

Copy **`module.toml`** from the repo into the same module directory.

## Configure

Module config: `<modules.data_dir>/blvm-mesh/config.toml`. Node override: `[modules.blvm-mesh]` or `[modules.mesh]` in `blvm.toml`.

```toml
[mesh]
enabled = true
mode = "payment_gated"   # open | payment_gated | bitcoin_only
max_peers = 50
rate_limit_per_minute = 120   # 0 = off
# peers = [{ address = "127.0.0.1:8333", node_id_hex = "..." }]
```

Enable in node config:

```toml
[modules]
enabled_modules = ["blvm-mesh"]
```

**`module.toml` capabilities:** `read_blockchain`, `subscribe_events`, `register_module_api`, `network_access`, `publish_events`, `read_payment`.

## Behaviour

| `mesh.mode` | Effect |
|-------------|--------|
| `open` | Free mesh routing |
| `payment_gated` | `PacketType::Paid` requires valid `PaymentProof` |
| `bitcoin_only` | Reject mesh app traffic |

Routing policy uses **`packet_type`** on mesh packets, not payload sniffing. Fee quotes use a 60% / 30% / 10% split (destination / intermediate hops / source) in `RoutingTable::calculate_routing_fee`.

**Events (subscribed):** `MeshPacketReceived`, `PeerConnected`, `PeerDisconnected`, `MessageReceived`, `MessageSent`, payment and chain/mempool events as registered in the module. **Published:** `RouteDiscovered`, `RouteFailed`.

## Node integration

Spawned modules register a ModuleAPI descriptor over IPC; the node installs **`IpcForwardingModuleAPI`** and forwards **`call_module`**. See [Module IPC Protocol — Subprocess ModuleAPI](../architecture/module-ipc-protocol.md#subprocess-moduleapi-registration).

| RPC | Purpose |
|-----|---------|
| `meshsendpacket` | Hex bincode `SendPacketRequest` → `send_packet` |
| `meshpollreceived` | Poll `poll_local_deliveries` by `protocol_id` |

Details: [RPC API — Mesh Methods](../node/rpc-api.md#mesh-methods).

## ModuleAPI

| Method | Purpose |
|--------|---------|
| `send_packet` | Route outbound mesh packet |
| `discover_route` | Find path to destination |
| `poll_local_deliveries` | Dequeue app payloads delivered locally |
| `get_routing_stats` / `get_node_id` | Stats and local node id |
| `register_protocol_handler` | Legacy; prefer `metadata.protocol` + poll |

Full request/response types: [API.md](https://github.com/BTCDecoded/blvm-mesh/blob/main/API.md).

### Call from another module

```rust
use blvm_mesh::MeshClient;

let mesh = MeshClient::new(node_api.clone(), "blvm-mesh".into());
let resp = mesh
    .send_packet("caller-id", destination, payload, payment_proof, Some("my-proto".into()))
    .await?;
```

Or `node_api.call_module(Some("blvm-mesh"), "send_packet", bincode::serialize(&req)?)`.

**Edge radios (Meshtastic, Reticulum):** use a separate adapter; do not duplicate mesh policy in the adapter. See **`docs/TRANSPORT.md`** in the mesh repo.

## Troubleshooting

| Issue | Check |
|-------|--------|
| Module not loading | Binary path, `module.toml`, required capabilities |
| No routes / no delivery | P2P peers up, `mesh add-peer` / hello, mode `open` for smoke tests |
| Payment rejected | Valid `PaymentProof`, `payment_gated` mode, replay/sequence limits |
| RPC bridge fails | Module loaded, ModuleAPI registered, `mesh_module_id` correct |

## See Also

- [Modules Overview](overview.md)
- [Module Development](../sdk/module-development.md)
- [Module IPC Protocol](../architecture/module-ipc-protocol.md)
