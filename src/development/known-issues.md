# Known Issues

This document tracks known technical issues in the codebase that require attention. These are validated issues confirmed through code inspection and static analysis.

## Critical Issues

### MutexGuard Held Across Await Points

**Status**: Known issue  
**Severity**: Critical  
**Location**: `blvm-node/src/network/mod.rs` and related files

#### Problem

Multiple instances where `std::sync::Mutex` guards are held across await points, causing deadlock risks. The async runtime may yield while holding a blocking mutex guard, and another task trying to acquire the same lock will block, potentially causing deadlock.

#### Code Pattern

```rust
// Problematic pattern
let mut peer_states = self.peer_states.lock().unwrap();  // std::sync::Mutex
// ... code that uses peer_states ...
if let Err(e) = self.send_to_peer(peer_addr, wire_msg).await {  // AWAIT WITH LOCK HELD!
    // MutexGuard still held here - DEADLOCK RISK
}
```

#### Impact

- **Deadlock risk**: Holding a `std::sync::Mutex` guard across an `await` point can cause deadlocks
- The async runtime may yield, and another task trying to acquire the same lock will block
- If that task is on the same executor thread, deadlock occurs

#### Root Cause

- `peer_states` uses `Arc<Mutex<...>>` with `std::sync::Mutex` instead of `tokio::sync::Mutex`
- Guard is held while calling async function `send_to_peer().await`

#### Recommended Fix

```rust
// Option 1: Drop guard before await
{
    let mut peer_states = self.peer_states.lock().unwrap();
    // ... use peer_states ...
} // Guard dropped here
if let Err(e) = self.send_to_peer(peer_addr, wire_msg).await {
    // ...
}

// Option 2: Use tokio::sync::Mutex (preferred for async code)
// Change field type to Arc<tokio::sync::Mutex<...>>
let mut peer_states = self.peer_states.lock().await;
```

#### Affected Locations

- `blvm-node/src/network/mod.rs`: Multiple locations
- `blvm-node/src/network/utxo_commitments_client.rs`: Lines 156, 165, 257, 349, 445

---

### Mixed Mutex Types

**Status**: Known issue  
**Severity**: Critical  
**Location**: `blvm-node/src/network/mod.rs`

#### Problem

NetworkManager uses `Arc<Mutex<...>>` with `std::sync::Mutex` (blocking) in async contexts, causing deadlock risks. All Mutex fields in NetworkManager are `std::sync::Mutex` but used in async code.

#### Current State

```rust
pub struct NetworkManager {
    peer_manager: Arc<Mutex<PeerManager>>,  // std::sync::Mutex
    peer_states: Arc<Mutex<HashMap<...>>>,  // std::sync::Mutex
    // ... many more Mutex fields
}
```

#### Recommended Fix

1. **Audit all Mutex fields** in NetworkManager
2. **Convert to tokio::sync::Mutex** for async contexts
3. **Update all `.lock().unwrap()` to `.lock().await`**
4. **Remove blocking locks from async functions**

#### Affected Fields

- `peer_manager: Arc<Mutex<PeerManager>>`
- `peer_states: Arc<Mutex<HashMap<...>>>`
- `persistent_peers: Arc<Mutex<HashSet<...>>>`
- `ban_list: Arc<Mutex<HashMap<...>>>`
- `socket_to_transport: Arc<Mutex<HashMap<...>>>`
- `pending_requests: Arc<Mutex<HashMap<...>>>`
- `request_id_counter: Arc<Mutex<u32>>`
- `address_database: Arc<Mutex<...>>`
- And more...

---

### Unwrap() on Mutex Locks

**Status**: Known issue  
**Severity**: High  
**Location**: Multiple files

#### Problem

Using `.unwrap()` on mutex locks can cause panics if the lock is poisoned (a thread panicked while holding the lock).

```rust
let mut db = self.address_database.lock().unwrap();  // Can panic!
let peer_states = network.peer_states.lock().unwrap();  // Can panic!
```

#### Impact

- If a thread panics while holding a Mutex, the lock becomes "poisoned"
- `.unwrap()` will panic, potentially crashing the entire node
- No graceful error handling

#### Recommended Fix

```rust
// Option 1: Handle poisoning gracefully
match self.address_database.lock() {
    Ok(guard) => { /* use guard */ }
    Err(poisoned) => {
        warn!("Mutex poisoned, recovering...");
        let guard = poisoned.into_inner();
        // use guard
    }
}

// Option 2: Use tokio::sync::Mutex (doesn't poison)
```

#### Affected Locations

- `blvm-node/src/network/mod.rs`: Multiple locations (19+ instances)
- `blvm-node/src/network/utxo_commitments_client.rs`: Lines 156, 165, 257, 349, 445
- `blvm-consensus/src/script.rs`: Multiple locations

---

## Medium Priority Issues

### Transport Abstraction Not Fully Integrated

**Status**: Known issue  
**Severity**: Medium  
**Location**: `blvm-node/src/network/`

#### Problem

Transport abstraction exists (`Transport` trait, `TcpTransport`, `IrohTransport`), but `Peer` struct still uses raw `TcpStream` directly in some places, not using the transport abstraction consistently.

#### Impact

- Code duplication
- Inconsistent error handling
- Harder to add new transports

#### Recommended Fix

- Audit all `Peer` creation sites
- Ensure all use `from_transport_connection`
- Remove direct `TcpStream` usage

---

### Nested Locking Patterns

**Status**: Known issue  
**Severity**: Medium  
**Location**: `blvm-node/src/network/utxo_commitments_client.rs`

#### Problem

Nested locking where `RwLock` read guard is held while acquiring inner `Mutex` locks, which can cause deadlocks.

```rust
let network = network_manager.read().await;  // RwLock read
// ...
network.socket_to_transport.lock().unwrap();  // Mutex lock inside
```

#### Recommended Fix

- Review locking strategy
- Consider flattening the lock hierarchy
- Or ensure consistent lock ordering

---

## Testing Gaps

### Missing Concurrency Tests

**Status**: Known gap  
**Severity**: Low

#### Problem

- No tests for Mutex deadlock scenarios
- No tests for lock ordering
- No stress tests for concurrent access

#### Recommendation

- Add tests that spawn multiple tasks accessing shared Mutex
- Test lock ordering to prevent deadlocks
- Add timeout tests for lock acquisition

---

## Priority Summary

### Priority 1 (Critical - Fix Immediately)
1. Fix MutexGuard held across await
2. Convert all `std::sync::Mutex` to `tokio::sync::Mutex` in async contexts
3. Replace `.unwrap()` on locks with proper error handling

### Priority 2 (High - Fix Soon)
4. Review and fix nested locking patterns
5. Complete transport abstraction integration

### Priority 3 (Medium - Fix When Possible)
6. Add concurrency stress tests

---

## Files Requiring Immediate Attention

1. **blvm-node/src/network/mod.rs** - Multiple critical issues
2. **blvm-node/src/network/utxo_commitments_client.rs** - MutexGuard across await
3. **blvm-consensus/src/script.rs** - Unwrap() on locks

---

## See Also

- [Contributing Guide](contributing.md) - How to contribute fixes
- [Testing Guide](testing.md) - Testing practices
- [PR Process](pr-process.md) - Pull request workflow
