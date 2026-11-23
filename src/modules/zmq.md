# ZMQ module (`blvm-zmq`)

Bitcoin-compatible **ZeroMQ PUB** notifications for blocks and mempool events. Replaces the former in-process **`[zmq]`** section on `blvm-node`: configure endpoints on this module instead.

## Overview

**blvm-zmq** binds one ZMQ **PUB** socket per distinct address and publishes when the node emits matching events. Topics that share an address share that socket:

| Topic | Payload | When |
|-------|---------|------|
| `hashblock` | 32-byte block hash | New block connected (`NewBlock`) |
| `hashtx` | 32-byte tx hash | Mempool add (`MempoolTransactionAdded`) |
| `rawblock` | Block wire bytes | New block (when block body is available via `get_block`) |
| `rawtx` | Transaction wire bytes | Mempool add (when tx is available via `get_mempool_transaction`) |
| `sequence` | 33 bytes (type + txid) | Mempool add (`0x01`) or remove (`0x02`). Not Core's `C`/`D`/`R`/`A` frame. The socket is not authenticated. |

If the module cannot fetch a full block or transaction from the node API, it still publishes **hash** / **sequence** topics where configured (see [Behaviour](#behaviour)).

**Repository:** [BTCDecoded/blvm-zmq](https://github.com/BTCDecoded/blvm-zmq)

## Requirements

- `blvm-node` with the module system enabled.
- Module pinned in **`registry/modules.json`** or installed on the module search path.
- `[config_defaults]` in `module.toml` publishes every topic on `endpoint`. The node copies that table at load and does not name the keys. A topic key publishes that topic on its own address. An empty topic value turns that topic off.

## Loading

Pin in `blvm.toml` (example):

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-zmq = "0.1.*"
```

One bind for every topic:

```toml
[modules.blvm-zmq]
endpoint = "tcp://127.0.0.1:28332"
```

Or place a release binary + `module.toml` under the modules directory. See [Module catalog: Installing modules](overview.md#installing-modules).

Module data-dir config: `<modules.data_dir>/blvm-zmq/config.toml` (same keys as `[modules.blvm-zmq]`).

## Configuration

| Key | Effect | Default |
|-----|--------|---------|
| `endpoint` | One PUB socket for every topic | `tcp://127.0.0.1:28332` |
| `hashblock`, `hashtx`, `rawblock`, `rawtx`, `sequence` | Bind that topic on its own address | unset |

**Endpoint format:** `transport://address`: `tcp://`, `ipc://`, or `inproc://` (same as Bitcoin Core ZMQ).

**Capabilities (`module.toml`):** `read_blockchain`, `read_mempool`, `subscribe_events`

## Wire format

- **Topics:** three frames: the topic, the payload, and a 32-bit little-endian counter for that socket.
- **`rawblock` / `rawtx` payloads:** Bitcoin **P2P wire serialization** from `blvm-protocol` (`serialize_block_witnesses` / `serialize_tx`): the same encoding as P2P `block` / `tx` message bodies, **not** bincode. Subscribers must decode wire format.

## Behaviour

### `NewBlock`

1. `get_block(block_hash)` when possible → `hashblock` + `rawblock`.
2. If the block is not in storage → `hashblock` only.

### `MempoolTransactionAdded`

1. `get_mempool_transaction(tx_hash)` when possible → `hashtx` + `rawtx` + `sequence` (entry=`0x01`).
2. If the tx is no longer in mempool → `hashtx` + `sequence` (entry).

### `MempoolTransactionRemoved`

- `sequence` only (removal=`0x02`): no `hashtx` / `rawtx` on removal.

## Subscribing (example)

```python
import zmq

ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)
sub.connect("tcp://127.0.0.1:28332")
sub.setsockopt(zmq.SUBSCRIBE, b"hashblock")

while True:
 topic = sub.recv_string()
 block_hash = sub.recv()
 print(topic, block_hash.hex())
```

More examples and topic details: [ZMQ notifications](https://github.com/BTCDecoded/blvm-node/blob/main/docs/ZMQ_NOTIFICATIONS.md) (operator reference; configuration lives in **`blvm-zmq`**, not `[zmq]` on the node).

## Troubleshooting

| Symptom | Check |
|---------|--------|
| No ZMQ traffic | Endpoints configured? Module loaded? Check module logs for bind errors |
| `hashblock` only, no `rawblock` | `get_block` returned none: block not available to module yet |
| Subscriber cannot decode `rawtx` | Use P2P wire decoder, not bincode |
| Port already in use | Another process or duplicate bind on same `tcp://` endpoint |
| Firewall | ZMQ binds on configured host; expose only on loopback unless intended |

## See also

- [Module catalog](overview.md)
- [Node configuration: module pins](../node/configuration.md)
- [Module IPC Protocol](../architecture/module-ipc-protocol.md)
