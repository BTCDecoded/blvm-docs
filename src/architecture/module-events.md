# Module Events

Delivery reliability, timing guarantees, and integration patterns for the module event system. For the full event type catalog and subscription API, see [Module system](module-system.md#event-system). For maintenance event payloads, see [Janitorial events](janitorial-events.md).

## Event timing

Event types follow fixed timing so modules subscribe before receiving `ModuleLoaded`.

### ModuleLoaded

`ModuleLoaded` events are **only published after a module has subscribed** (startup complete).

**Flow:**

1. Module process is spawned
2. Module connects via IPC and sends Handshake
3. Module sends `SubscribeEvents`
4. At subscription time:
   - Module receives `ModuleLoaded` for all already-loaded modules
   - `ModuleLoaded` is published for the newly subscribing module (if loaded)
5. Module is operational

**Why:** subscription completes before `ModuleLoaded`, so hotloaded modules receive existing modules and ordering is always subscription → `ModuleLoaded`.

**Startup (Module A first):** spawn → connect → subscribe → `ModuleLoaded` for A.

**Hotload (Module B later):** B subscribes → receives `ModuleLoaded` for A → `ModuleLoaded` published for B.

### DataMaintenance

Single event for flush/cleanup (replaces `StorageFlush` and `DataCleanup`).

**Payload:** `operation` (`flush`, `cleanup`, `both`), `urgency` (`low`, `medium`, `high`), `reason`, optional `target_age_days`, optional `timeout_seconds`.

```rust
// Shutdown flush
DataMaintenance { operation: "flush", urgency: "high", reason: "shutdown", timeout_seconds: Some(5) }

// Periodic cleanup
DataMaintenance { operation: "cleanup", urgency: "low", reason: "periodic", target_age_days: Some(30) }
```

**Migration from old events:**

```rust
// Old: separate StorageFlush / DataCleanup handlers
// New: one DataMaintenance handler keyed on operation + urgency
match event_type {
    EventType::DataMaintenance => {
        if let EventPayload::DataMaintenance { operation, .. } = payload {
            if operation == "flush" || operation == "both" { flush_data().await?; }
            if operation == "cleanup" || operation == "both" { cleanup_data().await?; }
        }
    }
    _ => {}
}
```

## Delivery and backpressure

### Reliability model

- **At-most-once** per subscriber; full channel drops the event (no retry)
- **Best-effort** — slow or dead modules may miss events; statistics track success/failure
- **Per-module ordering** on a single channel; no cross-module ordering guarantee

### Channel behavior

- **Buffer:** 100 events per module (hardcoded today)
- **Non-blocking publish:** `try_send`; publisher never blocks
- **Channel full:** event dropped with warning; subscription kept (module is slow, not dead)
- **Channel closed:** subscription removed (module dead)

```rust
let stats = event_manager.get_delivery_stats("module_id").await;
// Option<(successful_deliveries, failed_deliveries, channel_full_count)>
```

### Hotload and missed events

Newly subscribing modules receive `ModuleLoaded` for all already-loaded modules so late starters get a consistent view without replaying the full event log.

## Event categories (summary)

Full enum lists and subscription examples: [Module system → Event System](module-system.md#event-system).

| Category | Examples |
|----------|----------|
| Blockchain | `NewBlock`, `NewTransaction`, `BlockDisconnected`, `ChainReorg` |
| Governance | `GovernanceProposalCreated`, `GovernanceProposalVoted`, `GovernanceProposalMerged`, `GovernanceForkDetected` |
| Network | `PeerConnected`, `PeerDisconnected`, `PeerBanned`, `MessageReceived` |
| Module lifecycle | `ModuleLoaded`, `ModuleUnloaded`, `ModuleCrashed`, `ModuleHealthChanged` |
| Maintenance | `DataMaintenance`, `MaintenanceStarted`, `MaintenanceCompleted`, `HealthCheck` |
| Resources | `DiskSpaceLow`, `ResourceLimitWarning` |
| Node lifecycle | `NodeStartupCompleted`, `NodeShutdown`, `NodeShutdownCompleted` |

## Monitoring

```rust
let stats = event_manager.get_delivery_stats("module_id").await;
let all_stats = event_manager.get_all_delivery_stats().await;
let subscribers = event_manager.get_subscribers(EventType::NewBlock).await;
event_manager.reset_delivery_stats("module_id").await; // testing
```

## Module developer checklist

1. Subscribe immediately after handshake
2. Handle `ModuleLoaded` to discover peer modules
3. Keep handlers non-blocking
4. Handle `NodeShutdown` and high-urgency `DataMaintenance`
5. Monitor delivery statistics if events seem missing

## Node developer checklist

1. Publish through `EventPublisher` at stable code points
2. Log delivery warnings
3. Watch per-module channel-full counts for slow consumers
4. Cover startup, hotload, and slow-module paths in integration tests

## Extending events

1. Add variants to `EventType` and `EventPayload`
2. Add publisher helpers on `EventPublisher`
3. Follow existing patterns (e.g. `DataMaintenance` for maintenance)

## See Also

- [Module system (design)](module-system.md) — IPC, lifecycle, event catalog
- [Janitorial events](janitorial-events.md) — maintenance event payloads
- [Module IPC Protocol](module-ipc-protocol.md) — wire protocol
