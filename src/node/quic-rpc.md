# QUIC RPC

## Overview

Bitcoin Commons optionally supports JSON-RPC over QUIC using Quinn, providing improved performance and security compared to the standard TCP RPC server. QUIC RPC is an alternative transport protocol that runs alongside the standard TCP RPC server.

## Features

- **Encryption**: Built-in TLS encryption via QUIC
- **Multiplexing**: Multiple concurrent requests over single connection
- **Better Performance**: Lower latency, better congestion control
- **Backward Compatible**: TCP RPC server always available

**Code**: ```1:13:blvm-node/docs/QUIC_RPC.md```

## Usage

### Basic (TCP Only - Default)

```rust
use blvm_node::rpc::RpcManager;
use std::net::SocketAddr;

let tcp_addr: SocketAddr = "127.0.0.1:8332".parse().unwrap();
let mut rpc_manager = RpcManager::new(tcp_addr);
rpc_manager.start().await?;
```

**Code**: ```16:25:blvm-node/docs/QUIC_RPC.md```

### With QUIC Support

```rust
use blvm_node::rpc::RpcManager;
use std::net::SocketAddr;

let tcp_addr: SocketAddr = "127.0.0.1:8332".parse().unwrap();
let quinn_addr: SocketAddr = "127.0.0.1:18332".parse().unwrap();

// Option 1: Create with both transports
#[cfg(feature = "quinn")]
let mut rpc_manager = RpcManager::with_quinn(tcp_addr, quinn_addr);

// Option 2: Enable QUIC after creation
let mut rpc_manager = RpcManager::new(tcp_addr);
#[cfg(feature = "quinn")]
rpc_manager.enable_quinn(quinn_addr);

rpc_manager.start().await?;
```

**Code**: ```27:46:blvm-node/docs/QUIC_RPC.md```

## Configuration

### Feature Flag

QUIC RPC requires the `quinn` feature flag:

```toml
[dependencies]
blvm-node = { path = "../blvm-node", features = ["quinn"] }
```

**Code**: ```48:55:blvm-node/docs/QUIC_RPC.md```

### Build with QUIC

```bash
cargo build --features quinn
```

**Code**: ```57:61:blvm-node/docs/QUIC_RPC.md```

## QUIC RPC Server

### Server Implementation

The `QuinnRpcServer` provides JSON-RPC over QUIC:

- **Certificate Generation**: Self-signed certificates for development
- **Connection Handling**: Accepts incoming QUIC connections
- **Stream Management**: Manages bidirectional streams
- **Request Processing**: Processes JSON-RPC requests

**Code**: ```1:50:blvm-node/src/rpc/quinn_server.rs```

### Certificate Management

QUIC uses TLS certificates:

- **Development**: Self-signed certificates
- **Production**: Should use proper certificate management
- **Certificate Generation**: Automatic certificate generation

**Code**: ```31:44:blvm-node/src/rpc/quinn_server.rs```

## Client Usage

### QUIC Client

Clients need QUIC support. Example with `quinn`:

```rust
use quinn::Endpoint;
use std::net::SocketAddr;

let server_addr: SocketAddr = "127.0.0.1:18332".parse().unwrap();
let endpoint = Endpoint::client("0.0.0.0:0".parse().unwrap())?;
let connection = endpoint.connect(server_addr, "localhost")?.await?;

// Open bidirectional stream
let (mut send, mut recv) = connection.open_bi().await?;

// Send JSON-RPC request
let request = r#"{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}"#;
send.write_all(request.as_bytes()).await?;
send.finish().await?;

// Read response
let mut response = Vec::new();
recv.read_to_end(&mut response).await?;
let response_str = String::from_utf8(response)?;
```

**Code**: ```70:94:blvm-node/docs/QUIC_RPC.md```

## Benefits Over TCP

1. **Encryption**: Built-in TLS, no need for separate TLS layer
2. **Multiplexing**: Multiple requests without head-of-line blocking
3. **Connection Migration**: Survives IP changes
4. **Lower Latency**: Better congestion control
5. **Stream-Based**: Natural fit for request/response patterns

**Code**: ```96:103:blvm-node/docs/QUIC_RPC.md```

## Limitations

- **Bitcoin Core Compatibility**: Bitcoin Core only supports TCP RPC
- **Client Support**: Requires QUIC-capable clients
- **Certificate Management**: Self-signed certs need proper handling for production
- **Network Requirements**: Some networks may block UDP/QUIC

**Code**: ```104:110:blvm-node/docs/QUIC_RPC.md```

## Security Notes

- **Self-Signed Certificates**: Uses self-signed certificates for development. Production deployments require proper certificate management.
- **Authentication**: QUIC provides transport encryption but not application-level auth
- **Same Security Boundaries**: QUIC RPC has same security boundaries as TCP RPC (no wallet access)

**Code**: ```63:69:blvm-node/docs/QUIC_RPC.md```

## When to Use

- **High-Performance Applications**: When you need better performance than TCP
- **Modern Infrastructure**: When all clients support QUIC
- **Enhanced Security**: When you want built-in encryption without extra TLS layer
- **Internal Services**: When you control both client and server

**Code**: ```111:117:blvm-node/docs/QUIC_RPC.md```

## When Not to Use

- **Bitcoin Core Compatibility**: Need compatibility with Bitcoin Core tooling
- **Legacy Clients**: Clients that only support TCP/HTTP
- **Simple Use Cases**: TCP RPC is simpler and sufficient for most cases

**Code**: ```118:122:blvm-node/docs/QUIC_RPC.md```

## Components

The QUIC RPC system includes:
- Quinn RPC server implementation
- Certificate generation and management
- Connection and stream handling
- JSON-RPC protocol over QUIC
- Client support examples

**Location**: `blvm-node/src/rpc/quinn_server.rs`, `blvm-node/docs/QUIC_RPC.md`

