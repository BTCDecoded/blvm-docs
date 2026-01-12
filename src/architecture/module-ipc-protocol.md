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

**Code**: ```1:56:blvm-node/src/module/ipc/mod.rs```

### Message Types

The protocol supports four message types:

1. **Request**: Module → Node (API calls)
2. **Response**: Node → Module (API responses)
3. **Event**: Node → Module (event notifications)
4. **Log**: Module → Node (logging)

**Code**: ```16:49:blvm-node/src/module/ipc/protocol.rs```

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

**Code**: ```51:150:blvm-node/src/module/ipc/protocol.rs```

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

**Code**: ```152:207:blvm-node/src/module/ipc/protocol.rs```

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

**Code**: ```209:234:blvm-node/src/module/ipc/protocol.rs```

### Log Message

```rust
pub struct LogMessage {
    pub level: LogLevel,
    pub message: String,
    pub module_id: String,
}
```

**Log Levels**: `Error`, `Warn`, `Info`, `Debug`, `Trace`

**Code**: ```236:250:blvm-node/src/module/ipc/protocol.rs```

## Communication Flow

### Request-Response Pattern

1. **Module sends Request**: Module sends request message with correlation ID
2. **Node processes Request**: Node processes request and generates response
3. **Node sends Response**: Node sends response with matching correlation ID
4. **Module receives Response**: Module matches response to request using correlation ID

**Code**: ```138:200:blvm-node/src/module/ipc/server.rs```

### Event Subscription Pattern

1. **Module subscribes**: Module sends `SubscribeEvents` request with event types
2. **Node confirms**: Node sends subscription confirmation
3. **Node publishes Events**: Node sends event messages as they occur
4. **Module receives Events**: Module processes events asynchronously

**Code**: ```200:300:blvm-node/src/module/ipc/server.rs```

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

**Code**: ```148:200:blvm-node/src/module/ipc/server.rs```

### Connection Lifecycle

1. **Connect**: Module connects to Unix domain socket
2. **Handshake**: Module sends handshake, node validates
3. **Active**: Connection active, ready for requests/events
4. **Disconnect**: Connection closed (graceful or error)

**Code**: ```139:200:blvm-node/src/module/ipc/server.rs```

## Security

### Process Isolation

- Modules run in separate processes with isolated memory
- No shared memory between node and modules
- Module crashes don't affect the base node

**Code**: ```1:132:blvm-node/src/module/process/spawner.rs```

### Permission System

Modules request capabilities that are validated before API access:

- `ReadBlockchain` - Read-only blockchain access
- `ReadUTXO` - Query UTXO set (read-only)
- `ReadChainState` - Query chain state (height, tip)
- `SubscribeEvents` - Subscribe to node events
- `SendTransactions` - Submit transactions to mempool

**Code**: ```1:100:blvm-node/src/module/security/permissions.rs```

### Sandboxing

Modules run in sandboxed environments with:

- Resource limits (CPU, memory, file descriptors)
- Filesystem restrictions
- Network restrictions (modules cannot open network connections)
- Permission-based API access

**Code**: ```1:200:blvm-node/src/module/sandbox/mod.rs```

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

**Code**: ```1:100:blvm-node/src/module/traits.rs```

### Error Recovery

- **Connection Errors**: Automatic reconnection with exponential backoff
- **Protocol Errors**: Clear error messages, connection termination
- **Permission Errors**: Detailed error messages, request rejection
- **Timeout Errors**: Request timeout, connection remains active

**Code**: ```1:200:blvm-node/src/module/ipc/client.rs```

## Performance

### Message Serialization

- **Format**: bincode (binary encoding)
- **Size**: Compact binary representation
- **Speed**: Fast serialization/deserialization

**Code**: ```1:56:blvm-node/src/module/ipc/protocol.rs```

### Connection Pooling

- **Persistent Connections**: Connections remain open for multiple requests
- **Concurrent Requests**: Multiple requests can be in-flight simultaneously
- **Correlation IDs**: Match responses to requests asynchronously

**Code**: ```1:200:blvm-node/src/module/ipc/client.rs```

## Implementation Details

### IPC Server

The node-side IPC server:

- Listens on Unix domain socket
- Accepts module connections
- Routes requests to NodeAPI implementation
- Publishes events to subscribed modules

**Code**: ```1:151:blvm-node/src/module/ipc/server.rs```

### IPC Client

The module-side IPC client:

- Connects to Unix domain socket
- Sends requests and receives responses
- Subscribes to events
- Handles connection errors

**Code**: ```1:200:blvm-node/src/module/ipc/client.rs```

## See Also

- [Module System](module-system.md) - Module system architecture
- [Module Development](../sdk/module-development.md) - Building modules
- [Modules Overview](../modules/overview.md) - Available modules


