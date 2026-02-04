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

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/mod.rs#L1-L56)

### Message Types

The protocol supports four message types:

1. **Request**: Module → Node (API calls)
2. **Response**: Node → Module (API responses)
3. **Event**: Node → Module (event notifications)
4. **Log**: Module → Node (logging)

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs#L16-L49)

## Message Structure

### Request Message

```rust
pub struct RequestMessage {
    pub correlation_id: CorrelationId,
    pub request_type: MessageType,
    pub payload: RequestPayload,
}
```

**Request Types**:
- `GetBlock` - Get block by hash
- `GetBlockHeader` - Get block header by hash
- `GetTransaction` - Get transaction by hash
- `GetChainTip` - Get current chain tip
- `GetBlockHeight` - Get current block height
- `GetUTXO` - Get UTXO by outpoint
- `SubscribeEvents` - Subscribe to node events
- `GetMempoolTransactions` - Get mempool transaction hashes
- `GetNetworkStats` - Get network statistics
- `GetNetworkPeers` - Get connected peers
- `GetChainInfo` - Get chain information

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs#L51-L150)

### Response Message

```rust
pub struct ResponseMessage {
    pub correlation_id: CorrelationId,
    pub payload: ResponsePayload,
}
```

**Response Types**:
- `Success` - Request succeeded with data
- `Error` - Request failed with error details
- `NotFound` - Resource not found

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs#L152-L207)

### Event Message

```rust
pub struct EventMessage {
    pub event_type: EventType,
    pub payload: EventPayload,
}
```

**Event Types** (46+ event types):
- Network events: `PeerConnected`, `MessageReceived`, `PeerDisconnected`
- Payment events: `PaymentRequestCreated`, `PaymentVerified`, `PaymentSettled`
- Chain events: `NewBlock`, `ChainTipUpdated`, `BlockDisconnected`
- Mempool events: `MempoolTransactionAdded`, `FeeRateChanged`, `MempoolTransactionRemoved`

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs#L209-L234)

### Log Message

```rust
pub struct LogMessage {
    pub level: LogLevel,
    pub message: String,
    pub module_id: String,
}
```

**Log Levels**: `Error`, `Warn`, `Info`, `Debug`, `Trace`

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs#L236-L250)

## Communication Flow

### Request-Response Pattern

1. **Module sends Request**: Module sends request message with correlation ID
2. **Node processes Request**: Node processes request and generates response
3. **Node sends Response**: Node sends response with matching correlation ID
4. **Module receives Response**: Module matches response to request using correlation ID

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs#L138-L200)

### Event Subscription Pattern

1. **Module subscribes**: Module sends `SubscribeEvents` request with event types
2. **Node confirms**: Node sends subscription confirmation
3. **Node publishes Events**: Node sends event messages as they occur
4. **Module receives Events**: Module processes events asynchronously

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs#L200-L300)

## Connection Management

### Handshake

On connection, modules send a handshake message:

```rust
pub struct HandshakeMessage {
    pub module_id: String,
    pub capabilities: Vec<String>,
    pub version: String,
}
```

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs#L148-L200)

### Connection Lifecycle

1. **Connect**: Module connects to Unix domain socket
2. **Handshake**: Module sends handshake, node validates
3. **Active**: Connection active, ready for requests/events
4. **Disconnect**: Connection closed (graceful or error)

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs#L139-L200)

## Security

### Process Isolation

- Modules run in separate processes with isolated memory
- No shared memory between node and modules
- Module crashes don't affect the base node

**Code**: [spawner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/process/spawner.rs#L1-L132)

### Permission System

Modules request capabilities that are validated before API access:

- `ReadBlockchain` - Read-only blockchain access
- `ReadUTXO` - Query UTXO set (read-only)
- `ReadChainState` - Query chain state (height, tip)
- `SubscribeEvents` - Subscribe to node events
- `SendTransactions` - Submit transactions to mempool

**Code**: [permissions.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/security/permissions.rs#L1-L100)

### Sandboxing

Modules run in sandboxed environments with:

- Resource limits (CPU, memory, file descriptors)
- Filesystem restrictions
- Network restrictions (modules cannot open network connections)
- Permission-based API access

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/sandbox/mod.rs#L1-L200)

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

**Code**: [traits.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/traits.rs#L1-L100)

### Error Recovery

- **Connection Errors**: Automatic reconnection with exponential backoff
- **Protocol Errors**: Clear error messages, connection termination
- **Permission Errors**: Detailed error messages, request rejection
- **Timeout Errors**: Request timeout, connection remains active

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/client.rs#L1-L200)

## Performance

### Message Serialization

- **Format**: bincode (binary encoding)
- **Size**: Compact binary representation
- **Speed**: Fast serialization/deserialization

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/protocol.rs#L1-L56)

### Connection Pooling

- **Persistent Connections**: Connections remain open for multiple requests
- **Concurrent Requests**: Multiple requests can be in-flight simultaneously
- **Correlation IDs**: Match responses to requests asynchronously

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/client.rs#L1-L200)

## Implementation Details

### IPC Server

The node-side IPC server:

- Listens on Unix domain socket
- Accepts module connections
- Routes requests to NodeAPI implementation
- Publishes events to subscribed modules

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/server.rs#L1-L151)

### IPC Client

The module-side IPC client:

- Connects to Unix domain socket
- Sends requests and receives responses
- Subscribes to events
- Handles connection errors

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/ipc/client.rs#L1-L200)

## See Also

- [Module System](module-system.md) - Module system architecture
- [Module Development](../sdk/module-development.md) - Building modules
- [Modules Overview](../modules/overview.md) - Available modules


