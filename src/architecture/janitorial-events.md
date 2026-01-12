# Janitorial and Maintenance Events

## Overview

The module system provides comprehensive janitorial and maintenance events that allow modules to participate in node lifecycle, resource management, and data maintenance operations. This ensures modules can perform their own cleanup, maintenance, and resource management in sync with the node.

## Event Categories

### 1. Node Lifecycle Events

#### NodeShutdown
**When**: Node is shutting down (before components stop)
**Purpose**: Allow modules to clean up gracefully
**Payload**:
- `reason`: String - Shutdown reason ("graceful", "signal", "rpc", "error")
- `timeout_seconds`: u64 - Graceful shutdown timeout

**Module Action**: 
- Save state
- Close connections
- Flush data
- Clean up resources

#### NodeShutdownCompleted
**When**: Node shutdown is complete
**Purpose**: Notify modules that shutdown finished
**Payload**:
- `duration_ms`: u64 - Shutdown duration

#### NodeStartupCompleted
**When**: Node startup is complete (all components initialized)
**Purpose**: Notify modules that node is fully operational
**Payload**:
- `duration_ms`: u64 - Startup duration
- `components`: Vec<String> - Components that were initialized

**Module Action**:
- Initialize connections
- Load state
- Start processing

### 2. Storage Events

#### DataMaintenance (Unified)
**When**: Data maintenance is requested (shutdown, periodic, low disk, manual)
**Purpose**: Allow modules to flush data and/or clean up old data
**Payload**:
- `operation`: String - "flush", "cleanup", or "both"
- `urgency`: String - "low", "medium", or "high"
- `reason`: String - "periodic", "shutdown", "low_disk", "manual"
- `target_age_days`: Option<u64> - Target age for cleanup (if operation includes cleanup)
- `timeout_seconds`: Option<u64> - Timeout for high urgency operations

**Module Action**:
- **Flush**: Write pending data to disk
- **Cleanup**: Delete old data based on target_age_days
- **Both**: Flush and cleanup

**Urgency Levels**:
- **Low**: Periodic maintenance, can be done asynchronously
- **Medium**: Scheduled maintenance, should complete soon
- **High**: Urgent (shutdown, low disk), must complete quickly

### 3. Maintenance Events

#### MaintenanceStarted
**When**: Maintenance operation started
**Purpose**: Allow modules to prepare for maintenance
**Payload**:
- `maintenance_type`: String - "backup", "cleanup", "prune"
- `estimated_duration_seconds`: Option<u64> - Estimated duration

**Module Action**:
- Pause non-critical operations
- Prepare for maintenance

#### MaintenanceCompleted
**When**: Maintenance operation completed
**Purpose**: Notify modules that maintenance finished
**Payload**:
- `maintenance_type`: String - Maintenance type
- `success`: bool - Success status
- `duration_ms`: u64 - Duration in milliseconds
- `results`: Option<String> - Results/statistics (optional JSON)

**Module Action**:
- Resume normal operations
- Process results if needed

#### HealthCheck
**When**: Health check performed
**Purpose**: Allow modules to report their health status
**Payload**:
- `check_type`: String - "periodic", "manual", "startup"
- `node_healthy`: bool - Node health status
- `health_report`: Option<String> - Health report (optional JSON)

**Module Action**:
- Report module health status
- Perform internal health checks

### 4. Resource Management Events

#### DiskSpaceLow
**When**: Disk space is low
**Purpose**: Allow modules to clean up data to free space
**Payload**:
- `available_bytes`: u64 - Available space in bytes
- `total_bytes`: u64 - Total space in bytes
- `percent_free`: f64 - Percentage free
- `disk_path`: String - Disk path

**Module Action**:
- Clean up old data
- Reduce data retention
- Flush and compress data

#### ResourceLimitWarning
**When**: Resource limit approaching
**Purpose**: Allow modules to reduce resource usage
**Payload**:
- `resource_type`: String - "memory", "cpu", "disk", "network"
- `usage_percent`: f64 - Current usage percentage
- `current_usage`: u64 - Current usage value
- `limit`: u64 - Limit value
- `threshold_percent`: f64 - Warning threshold percentage

**Module Action**:
- Reduce resource usage
- Clean up resources
- Optimize operations

## Usage Examples

### Handling Shutdown

```rust
match event_type {
    EventType::NodeShutdown => {
        if let EventPayload::NodeShutdown { reason, timeout_seconds } = payload {
            info!("Node shutting down: {}, timeout: {}s", reason, timeout_seconds);
            
            // Save state
            save_state().await?;
            
            // Close connections
            close_connections().await?;
            
            // Flush data
            flush_data().await?;
        }
    }
    _ => {}
}
```

### Handling Data Maintenance

```rust
match event_type {
    EventType::DataMaintenance => {
        if let EventPayload::DataMaintenance { operation, urgency, reason, target_age_days, timeout_seconds } = payload {
            match operation.as_str() {
                "flush" => {
                    flush_pending_data().await?;
                }
                "cleanup" => {
                    let age_days = target_age_days.unwrap_or(30);
                    cleanup_old_data(age_days).await?;
                }
                "both" => {
                    flush_pending_data().await?;
                    let age_days = target_age_days.unwrap_or(30);
                    cleanup_old_data(age_days).await?;
                }
                _ => {}
            }
            
            if urgency == "high" {
                // High urgency - must complete quickly
                if let Some(timeout) = timeout_seconds {
                    tokio::time::timeout(
                        Duration::from_secs(timeout),
                        maintenance_operation()
                    ).await?;
                }
            }
        }
    }
    _ => {}
}
```

### Handling Disk Space Low

```rust
match event_type {
    EventType::DiskSpaceLow => {
        if let EventPayload::DiskSpaceLow { available_bytes, percent_free, .. } = payload {
            warn!("Disk space low: {} bytes available, {:.2}% free", available_bytes, percent_free);
            
            // Clean up old data
            cleanup_old_data(7).await?; // Keep only last 7 days
            
            // Compress data
            compress_data().await?;
        }
    }
    _ => {}
}
```

## Best Practices

1. **Always Handle Shutdown**: Modules must handle `NodeShutdown` and `DataMaintenance` (urgency: "high")
2. **Non-Blocking Operations**: Keep maintenance operations fast and non-blocking
3. **Respect Timeouts**: For high urgency operations, respect timeout_seconds
4. **Clean Up Resources**: Always clean up resources on shutdown
5. **Monitor Health**: Report health status during `HealthCheck` events

## Integration Timing

### Startup Sequence
1. Node starts
2. Modules load
3. Modules subscribe to events
4. `NodeStartupCompleted` published
5. Modules can start processing

### Shutdown Sequence
1. `NodeShutdown` published (with timeout)
2. Modules clean up (within timeout)
3. `DataMaintenance` published (urgency: "high", operation: "flush")
4. Modules flush data
5. Node components stop
6. `NodeShutdownCompleted` published

### Periodic Maintenance
1. `DataMaintenance` published (urgency: "low", operation: "cleanup", reason: "periodic")
2. Modules clean up old data
3. `MaintenanceCompleted` published

## See Also

- [Module System](module-system.md) - Module system architecture
- [Event System Integration](event-system-integration.md) - Complete integration guide
- [Event Consistency](event-consistency.md) - Event timing and consistency guarantees
- [Module IPC Protocol](module-ipc-protocol.md) - IPC communication details

