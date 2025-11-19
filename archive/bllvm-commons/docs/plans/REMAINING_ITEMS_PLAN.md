# Remaining Items Implementation Plan

## Overview
Two remaining items to address:
1. **Iroh Peer Tracking** - Improve peer identification using NodeId instead of placeholder SocketAddr
2. **UTXO Commitments Async Routing** - Implement request-response pattern for async message handling

## Item 1: Iroh Peer Tracking

### Current State
- `PeerManager` uses `SocketAddr` as key for peer tracking
- Iroh connections use `NodeId` (32-byte public key) as identifier
- Current workaround: Derives placeholder `SocketAddr` from first 4 bytes of public key
- Issue: Multiple Iroh peers could map to same SocketAddr (collision risk)

### Solution Approach
**Option A (Recommended)**: Extend `PeerManager` to support `TransportAddr` as keys
- Change `PeerManager::peers` from `HashMap<SocketAddr, Peer>` to `HashMap<TransportAddr, Peer>`
- Update all `PeerManager` methods to use `TransportAddr`
- Update `Peer` struct to store `TransportAddr` instead of just `SocketAddr`
- Update `NetworkManager` to use `TransportAddr` for peer tracking

**Option B**: Keep dual tracking (SocketAddr for compatibility, NodeId for Iroh)
- Maintain `HashMap<SocketAddr, Peer>` for TCP/Quinn
- Add `HashMap<Vec<u8>, Peer>` for Iroh (keyed by NodeId bytes)
- Requires mapping logic between the two

### Implementation Steps (Option A)
1. Update `Peer` struct to use `TransportAddr` as primary identifier
2. Update `PeerManager` to use `TransportAddr` keys
3. Update `NetworkManager` peer tracking to use `TransportAddr`
4. Extract actual `NodeId` from Iroh connections when available
5. Update all peer lookup/management code paths

### Validation
- ✅ No breaking changes to public API (internal refactoring)
- ✅ Maintains backward compatibility for TCP/Quinn (SocketAddr → TransportAddr::Tcp)
- ✅ Proper Iroh peer identification without collisions
- ✅ Minimal code changes (focused refactoring)

## Item 2: UTXO Commitments Async Routing

### Current State
- Messages are sent via `NetworkManager::send_to_peer`
- No mechanism to await responses
- UTXO commitment requests return error immediately after sending

### Solution Approach
Implement a request-response registry system:

1. **Request ID System**
   - Generate unique request IDs for each request
   - Include request ID in message headers/metadata

2. **Response Registry**
   - `HashMap<RequestId, oneshot::Sender<Response>>` for pending requests
   - Timeout mechanism for expired requests
   - Cleanup of completed/expired requests

3. **Message Routing**
   - Match incoming responses to pending requests by ID
   - Route response to appropriate future/callback
   - Handle timeout and error cases

### Implementation Steps
1. Create `RequestId` type (u64 or UUID)
2. Add `pending_requests: Arc<Mutex<HashMap<RequestId, oneshot::Sender<...>>>>` to `NetworkManager`
3. Update `handle_incoming_wire_tcp` to check for response messages and route to pending requests
4. Update UTXO commitment client to register requests and await responses
5. Add timeout handling (e.g., 30 seconds)
6. Add cleanup task for expired requests

### Validation
- ✅ Non-blocking (uses async/await)
- ✅ Thread-safe (Arc<Mutex>)
- ✅ Handles timeouts gracefully
- ✅ Minimal performance impact
- ✅ Extensible for other request-response patterns

## Implementation Order

1. **Phase 1: Iroh Peer Tracking** (Lower complexity, immediate benefit)
   - Estimated: 2-3 file changes
   - Risk: Low (internal refactoring)
   - Benefit: Proper peer identification

2. **Phase 2: Async Routing** (Higher complexity, enables future features)
   - Estimated: 4-5 file changes
   - Risk: Medium (new async infrastructure)
   - Benefit: Enables UTXO commitments and other request-response patterns

## Decision: Proceed with Phase 1 first

Phase 1 is simpler and provides immediate value. Phase 2 can follow once Phase 1 is validated.

