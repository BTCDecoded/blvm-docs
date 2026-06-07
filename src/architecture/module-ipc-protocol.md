# Module IPC Protocol

## Overview

The Module IPC (Inter-Process Communication) protocol enables secure communication between process-isolated modules and the base node. Modules run in separate processes and communicate via Unix domain sockets using a length-delimited binary message protocol.

## Architecture

```
┌─────────────────────────────────────┐
│         blvm-node Process          │
│  ┌───────────────────────────────┐ │
│  │    Module IPC Server          │ │
│  │    (Unix Domain Socket)       │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
              │ IPC Protocol
              │ (Unix Domain Socket)
              │
┌─────────────┴─────────────────────┐
│      Module Process (Isolated)     │
│  ┌───────────────────────────────┐ │
│  │    Module IPC Client          │ │
│  │    (Unix Domain Socket)       │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Protocol Format

### Message Encoding

Messages use length-delimited binary encoding:

```
[4-byte length][message payload]
```

- **Length**: 4-byte little-endian integer (message size)
- **Payload**: Binary-encoded message (bincode serialization)

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/mod.rs)

### Message Types

The protocol uses length-delimited **`ModuleMessage`** variants:

1. **Request** — module → node (NodeAPI calls, handshake, `RegisterModuleApi`, …)
2. **Response** — node → module
3. **Event** — node → module (subscribed notifications)
4. **Log** — module → node (forwarded to node logging)
5. **Invocation** — node → module (CLI, RPC, or **`ModuleApi`** dispatch)
6. **InvocationResult** — module → node (correlated reply)

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs) (`ModuleMessage`)

## Message Structure

### Request Message

```rust
pub struct RequestMessage {
    pub correlation_id: CorrelationId,
    pub request_type: MessageType,
    pub payload: RequestPayload,
}
```

**Request types (representative)**:

Reads and subscriptions include `GetBlock`, `GetBlockHeader`, `GetTransaction`, `GetChainTip`, `GetBlockHeight`, `GetUTXO`, `SubscribeEvents`, `GetMempoolTransactions`, `GetNetworkStats`, `GetNetworkPeers`, `GetChainInfo`, and many others (mining, storage, RPC, timers, …).

**P2P serve policy & sync (module → node):**

| `MessageType` | Role |
|-----------------|------|
| `MergeBlockServeDenylist` | Add block hashes that must not receive full `block` on `getdata` (`notfound` instead). |
| `GetBlockServeDenylistSnapshot` | Bounded snapshot of the block denylist. |
| `ClearBlockServeDenylist` / `ReplaceBlockServeDenylist` | Clear or replace the full set. |
| `MergeTxServeDenylist` | Same pattern for full `tx` on `getdata`. |
| `GetTxServeDenylistSnapshot` | Bounded snapshot of the tx denylist. |
| `ClearTxServeDenylist` / `ReplaceTxServeDenylist` | Clear or replace the tx set. |
| `GetSyncStatus` | Sync coordinator status (`SyncStatus`). |
| `BanPeer` | Ban peer by address; optional duration. |
| `SetBlockServeMaintenanceMode` | Refuse all full-block `getdata` answers when enabled. |

These affect **relay/serving only**, not consensus validation. See [`NodeAPI`](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs) for the Rust surface.

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs)

### Response Message

```rust
pub struct ResponseMessage {
    pub correlation_id: CorrelationId,
    pub payload: ResponsePayload,
}
```

**Response payload** variants carry typed data (blocks, templates, snapshots, booleans, errors, etc.); denylist merges return dedicated merged/snapshot payloads where applicable.

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs)

### Event Message

```rust
pub struct EventMessage {
    pub event_type: EventType,
    pub payload: EventPayload,
}
```

**Event types:** The node defines many **`EventType`** values (chain, mempool, network, payments, mining, mesh, sync, modules, governance, maintenance, …). Modules subscribe to a subset via **`SubscribeEvents`**. See the **`EventType`** enum in [traits.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs) for the authoritative list — do not assume a fixed count in docs.

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs), [traits.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs)

### Log Message

```rust
pub struct LogMessage {
    pub level: LogLevel,
    pub message: String,
    pub module_id: String,
}
```

**Log Levels**: `Error`, `Warn`, `Info`, `Debug`, `Trace`

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs)

## Communication Flow

### Request-Response Pattern

1. **Module sends Request**: Module sends request message with correlation ID
2. **Node processes Request**: Node processes request and generates response
3. **Node sends Response**: Node sends response with matching correlation ID
4. **Module receives Response**: Module matches response to request using correlation ID

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs)

### Invocation pattern (CLI, RPC, ModuleAPI)

The node sends **`Invocation`** messages to a connected module subprocess:

| `InvocationType` | Use |
|------------------|-----|
| `Cli` | `runmodulecli` / module CLI dispatch |
| `Rpc` | Module-registered RPC methods |
| `ModuleApi` | Inter-module **`call_module`** forwarded to the subprocess handler |

The module replies with **`InvocationResult`** (same **`correlation_id`**). For **`ModuleApi`**, the payload is opaque bytes (`InvocationResultPayload::ModuleApi`).

### Subprocess ModuleAPI registration

Spawned modules cannot pass `Arc<dyn ModuleAPI>` into the node process. Instead:

1. Module sends **`RegisterModuleApi`** with method names and API version.
2. Node installs **`IpcForwardingModuleAPI`** in the module registry.
3. Other callers use **`call_module`** (or node RPC such as **`meshsendpacket`**) → node sends **`InvocationType::ModuleApi`** to the subprocess.
4. On disconnect, the node unregisters the proxy.

Cross-task invocations use **`ModuleIpcHandle`** so callers do not lock the server accept loop.

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs), [ipc_proxy.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/inter_module/ipc_proxy.rs), [runner.rs](https://github.com/BTCDecoded/blvm-sdk/blob/main/src/module/runner.rs)

### Event Subscription Pattern

1. **Module subscribes**: Module sends `SubscribeEvents` request with event types
2. **Node confirms**: Node sends subscription confirmation
3. **Node publishes Events**: Node sends event messages as they occur
4. **Module receives Events**: Module processes events asynchronously

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs)

## Connection Management

### Handshake

On connection, the module sends a **handshake** as the first **`Request`**:

```rust
RequestPayload::Handshake {
    module_id,
    module_name,
    version,
}
```

The node replies with **`HandshakeAck`** (node version). Modules without a handshake receive a fallback connection id (legacy path).

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs)

### Connection Lifecycle

1. **Connect**: Module connects to Unix domain socket
2. **Handshake**: Module sends handshake, node validates
3. **Active**: Connection active, ready for requests/events
4. **Disconnect**: Connection closed (graceful or error)

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs)

## Security

### Process Isolation

- Modules run in separate processes with isolated memory
- No shared memory between node and modules
- Module crashes don't affect the base node

**Code**: [spawner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/process/spawner.rs)

### Permission System

Modules request capabilities that are validated before API access:

- `ReadBlockchain` - Read-only blockchain access
- `ReadUTXO` - Query UTXO set (read-only)
- `ReadChainState` - Query chain state (height, tip)
- `SubscribeEvents` - Subscribe to node events
- `SendTransactions` - Submit transactions to mempool

**Code**: [permissions.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/security/permissions.rs)

### Sandboxing

Modules run in sandboxed environments with:

- Resource limits (CPU, memory, file descriptors)
- Filesystem restrictions (module data dir)
- **Network**: modules do not open arbitrary sockets; P2P and mesh sends go through **NodeAPI** with the **`network_access`** capability
- Permission-based API access

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/sandbox/mod.rs), [permissions.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/security/permissions.rs)

## Error Handling

### Error Types

```rust
pub enum ModuleError {
    ConnectionError(String),
    ProtocolError(String),
    PermissionDenied(String),
    ResourceExhausted(String),
    Timeout(String),
}
```

**Code**: [traits.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs)

### Error Recovery

- **Connection Errors**: Automatic reconnection with exponential backoff
- **Protocol Errors**: Clear error messages, connection termination
- **Permission Errors**: Detailed error messages, request rejection
- **Timeout Errors**: Request timeout, connection remains active

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/client.rs)

## Performance

### Message Serialization

- **Format**: bincode (binary encoding)
- **Size**: Compact binary representation
- **Speed**: Fast serialization/deserialization

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs)

### Connection Pooling

- **Persistent Connections**: Connections remain open for multiple requests
- **Concurrent Requests**: Multiple requests can be in-flight simultaneously
- **Correlation IDs**: Match responses to requests asynchronously

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/client.rs)

## Implementation Details

### IPC Server

The node-side IPC server:

- Listens on Unix domain socket
- Accepts module connections
- Routes requests to NodeAPI implementation
- Publishes events to subscribed modules

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs)

### IPC Client

The module-side IPC client:

- Connects to Unix domain socket
- Sends requests and receives responses
- Subscribes to events
- Handles connection errors

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/client.rs)

## See Also

- [Module System](module-system.md) - Module system architecture
- [Module Development](../sdk/module-development.md) - Building modules
- [Modules Overview](../modules/overview.md) - Available modules


