# Configuration Integration Status

## Overview

This document tracks the integration of new configuration options into the runtime components.

## Completed ✅

1. **Config Structs Added** - All new configuration structs are defined in `bllvm-node/src/config/mod.rs`:
   - `DosProtectionConfig`
   - `RelayConfig`
   - `AddressDatabaseConfig`
   - `DandelionConfig` (feature-gated)
   - `PeerRateLimitingConfig`

2. **DosProtectionManager Updated** - Added support for configurable ban duration:
   - Added `ban_duration_seconds` field
   - Added `with_ban_settings()` method
   - Added `ban_duration_seconds()` getter method

## In Progress ⏳

3. **NetworkManager Integration** - Need to:
   - Add method to create DosProtectionManager from config
   - Add method to create AddressDatabase from config
   - Update `NetworkManager::new()` to accept optional config
   - Replace hardcoded `3600` ban duration with config value

4. **RelayManager Integration** - Need to:
   - Update `RelayManager` to use `RelayConfig`
   - Apply relay settings from config

5. **Dandelion Integration** - Need to:
   - Update Dandelion initialization to use `DandelionConfig`
   - Apply Dandelion settings from config

6. **Peer Rate Limiting Integration** - Need to:
   - Update peer rate limiter initialization to use `PeerRateLimitingConfig`
   - Apply rate limiting settings from config

## Pending ❌

7. **ENV Variable Support** - Need to add ENV variable parsing for:
   - DoS protection settings
   - Relay settings
   - Address database settings
   - Dandelion settings
   - Peer rate limiting settings

8. **Node Integration** - Need to:
   - Pass config from `Node::new()` to `NetworkManager`
   - Apply all config sections to respective components

## Implementation Notes

### NetworkManager Changes Needed

```rust
impl NetworkManager {
    /// Create with configuration
    pub fn with_config(
        listen_addr: SocketAddr,
        max_peers: usize,
        preference: TransportPreference,
        config: Option<&NodeConfig>,
    ) -> Self {
        // Use config for DoS protection
        let dos_config = config
            .and_then(|c| c.dos_protection.as_ref())
            .unwrap_or(&DosProtectionConfig::default());
        
        let dos_protection = Arc::new(
            DosProtectionManager::with_ban_settings(
                dos_config.max_connections_per_window,
                dos_config.window_seconds,
                dos_config.max_message_queue_size,
                dos_config.max_active_connections,
                dos_config.auto_ban_threshold,
                dos_config.ban_duration_seconds,
            )
        );
        
        // Use config for address database
        let addr_db_config = config
            .and_then(|c| c.address_database.as_ref())
            .unwrap_or(&AddressDatabaseConfig::default());
        
        let address_database = Arc::new(Mutex::new(
            AddressDatabase::with_expiration(
                addr_db_config.max_addresses,
                addr_db_config.expiration_seconds,
            )
        ));
        
        // ... rest of initialization
    }
}
```

### Hardcoded Values to Replace

1. **Ban Duration** (3 locations in `network/mod.rs`):
   - Line ~897: `+ 3600` → use `dos_protection.ban_duration_seconds()`
   - Line ~1002: `+ 3600` → use `dos_protection.ban_duration_seconds()`
   - Line ~1582: `+ 3600` → use `dos_protection.ban_duration_seconds()`

2. **Address Database** (2 locations):
   - Line ~450: `AddressDatabase::new(10000)` → use config
   - Line ~514: `AddressDatabase::new(10000)` → use config

3. **DoS Protection** (2 locations):
   - Line ~447: `DosProtectionManager::default()` → use config
   - Line ~511: `DosProtectionManager::default()` → use config

## Testing Checklist

- [ ] DoS protection uses config values
- [ ] Address database uses config values
- [ ] Relay manager uses config values
- [ ] Dandelion uses config values (if feature enabled)
- [ ] Peer rate limiting uses config values
- [ ] ENV variables override config file
- [ ] CLI overrides ENV and config file
- [ ] Defaults work when no config provided


