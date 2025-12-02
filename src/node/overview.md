# Node Implementation Overview

The node implementation (`bllvm-node`) provides a minimal, production-ready Bitcoin node that adds only non-consensus infrastructure to the consensus and protocol layers. All consensus logic comes from `bllvm-consensus`, and protocol abstraction comes from `bllvm-protocol`.

## Architecture

The node follows a layered architecture:

```
┌─────────────────────────────────────┐
│         bllvm-node                  │
│  ┌───────────────────────────────┐ │
│  │  Network Manager              │ │  ← P2P networking, peer management
│  │  Storage Layer                │ │  ← Block/UTXO storage (redb/sled)
│  │  RPC Server                   │ │  ← JSON-RPC 2.0 API
│  │  Module Manager               │ │  ← Process-isolated modules
│  │  Mempool Manager              │ │  ← Transaction mempool
│  │  Mining Coordinator           │ │  ← Block template generation
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
              │
              ├─→ bllvm-protocol (protocol abstraction)
              └─→ bllvm-consensus (consensus validation)
```

## Key Components

### Network Manager
- P2P protocol implementation (Bitcoin wire protocol)
- Multi-transport support (TCP, Quinn QUIC, Iroh)
- Peer connection management
- Message routing and relay
- Privacy protocols (Dandelion++, Fibre)
- Package relay (BIP331)

**Code**: ```1:2680:bllvm-node/src/network/mod.rs```

### Storage Layer
- Database abstraction with multiple backends
- Automatic backend fallback on failure
- Block storage and indexing
- UTXO set management
- Chain state tracking
- Transaction indexing
- Pruning support

**Code**: ```1:89:bllvm-node/src/storage/mod.rs```

### RPC Server
- JSON-RPC 2.0 compliant API
- REST API (optional feature, runs alongside JSON-RPC)
- Optional QUIC transport support
- Authentication and rate limiting
- Comprehensive method coverage

**Code**: ```1:47:bllvm-node/src/rpc/mod.rs```

### Module System
- Process-isolated modules
- IPC communication (Unix domain sockets)
- Security sandboxing
- Permission-based API access
- Hot reload support

**Code**: ```1:520:bllvm-node/src/module/manager.rs```

### Mempool Manager
- Transaction validation and storage
- Fee-based transaction selection
- RBF (Replace-By-Fee) support
- Mempool policies and limits
- Transaction expiry

**Code**: ```1:200:bllvm-node/src/node/mempool.rs```

### Mining Coordinator
- Block template generation
- Stratum V2 protocol support
- Merge mining coordination
- Mining job distribution

**Code**: ```1:531:bllvm-node/src/node/miner.rs```

### Payment Processing
- Lightning Network integration
- Payment vaults
- Covenant support
- Payment state management

**Code**: ```1:10:bllvm-node/src/payment/mod.rs```

### Governance Integration
- Webhook handlers for governance events
- User signaling support
- Economic node integration

**Code**: ```1:3:bllvm-node/src/governance/mod.rs```

## Design Principles

1. **Zero Consensus Re-implementation**: All consensus logic delegated to `bllvm-consensus`
2. **Protocol Abstraction**: Uses `bllvm-protocol` for variant support (mainnet, testnet, regtest)
3. **Pure Infrastructure**: Only adds storage, networking, RPC, orchestration
4. **Production Ready**: Full Bitcoin node functionality with performance optimizations

## Features

### Network Features
- Multi-transport architecture (TCP, QUIC)
- Privacy-preserving relay (Dandelion++)
- High-performance block relay (Fibre)
- Package relay (BIP331)
- UTXO commitments support

### Storage Features
- Multiple database backends with abstraction layer
- Automatic backend fallback on failure
- Pruning support
- Transaction indexing
- UTXO set management

### Module Features
- Process isolation
- IPC communication
- Security sandboxing
- Hot reload
- Module registry

### Mining Features
- Block template generation
- Stratum V2 protocol
- Merge mining support
- Mining pool coordination

### Payment Features
- Lightning Network module support
- Payment vault management
- Covenant enforcement
- Payment state machines

### Integration Features
- Governance webhook integration
- ZeroMQ notifications (optional)
- REST API alongside JSON-RPC
- Module registry (P2P discovery)

## Node Lifecycle

1. **Initialization**: Load configuration, initialize storage, create network manager
2. **Startup**: Connect to P2P network, discover peers, load modules
3. **Sync**: Download and validate blockchain history
4. **Running**: Validate blocks/transactions, relay messages, serve RPC requests
5. **Shutdown**: Graceful shutdown of all components

**Code**: ```76:1094:bllvm-node/src/node/mod.rs```

## Metrics and Monitoring

The node includes comprehensive metrics collection:

- **Network Metrics**: Peer count, bytes sent/received, connection statistics
- **Storage Metrics**: Block count, UTXO count, database size
- **RPC Metrics**: Request count, error rate, response times
- **Performance Metrics**: Block validation time, transaction processing time
- **System Metrics**: CPU usage, memory usage, disk I/O

**Code**: ```1:71:bllvm-node/src/node/metrics.rs```

## See Also

- [Installation](../getting-started/installation.md) - Installing the node
- [Quick Start](../getting-started/quick-start.md) - Running your first node
- [Node Configuration](configuration.md) - Configuration options
- [Node Operations](operations.md) - Node management and operations
- [RPC API Reference](rpc-api.md) - JSON-RPC API documentation
- [Mining Integration](mining.md) - Mining functionality
- [Module System](../architecture/module-system.md) - Module system architecture
- [Storage Backends](storage-backends.md) - Storage backend details

