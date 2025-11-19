# Pruning Implementation Plan

## Overview

This plan implements comprehensive blockchain pruning with UTXO commitments integration, providing maximum configurability for different use cases and feature combinations.

## Key Design Principles

1. **UTXO Commitments Enable Aggressive Pruning**: With UTXO commitments, we can prune blocks more aggressively because we can verify UTXO set state via commitments without needing full block history.

2. **Feature Flag Integration**: Pruning behavior adapts based on enabled features (UTXO commitments, BIP158 filters, etc.).

3. **Maximum Configurability**: Every aspect of pruning is configurable, allowing users to optimize for their specific use case (storage-constrained, archival, light client support, etc.).

4. **Graceful Degradation**: Pruning works even without UTXO commitments, but with more conservative defaults.

## Architecture

### Pruning Modes

```rust
pub enum PruningMode {
    /// No pruning (keep all blocks)
    Disabled,
    
    /// Normal pruning (keep recent blocks for verification)
    /// Requires: Full block history for recent blocks
    Normal {
        /// Keep blocks from this height onwards
        keep_from_height: u64,
        /// Keep at least this many recent blocks
        min_recent_blocks: u64,
    },
    
    /// Aggressive pruning with UTXO commitments
    /// Requires: utxo-commitments feature enabled
    /// Enables: Much more aggressive pruning because state can be verified via commitments
    Aggressive {
        /// Keep blocks from this height onwards
        keep_from_height: u64,
        /// Keep UTXO commitments for all pruned blocks
        keep_commitments: bool,
        /// Keep filtered blocks (spam-filtered) for pruned range
        keep_filtered_blocks: bool,
        /// Minimum blocks to keep (safety margin)
        min_blocks: u64,
    },
    
    /// Custom pruning configuration
    Custom {
        /// Keep block headers (always required for PoW verification)
        keep_headers: bool,
        /// Keep block bodies from this height onwards
        keep_bodies_from_height: u64,
        /// Keep UTXO commitments (if utxo-commitments feature enabled)
        keep_commitments: bool,
        /// Keep BIP158 filters (if BIP157/158 enabled)
        keep_filters: bool,
        /// Keep filtered blocks (spam-filtered)
        keep_filtered_blocks: bool,
        /// Keep witness data (for SegWit verification)
        keep_witnesses: bool,
        /// Keep transaction index
        keep_tx_index: bool,
    },
}
```

## Configuration Structure

### Pruning Configuration

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PruningConfig {
    /// Pruning mode
    #[serde(default = "default_pruning_mode")]
    pub mode: PruningMode,
    
    /// Automatic pruning (prune periodically as chain grows)
    #[serde(default = "default_true")]
    pub auto_prune: bool,
    
    /// Automatic pruning interval (blocks)
    /// Prune every N blocks if auto_prune is enabled
    #[serde(default = "default_auto_prune_interval")]
    pub auto_prune_interval: u64,
    
    /// Minimum blocks to keep (safety margin)
    /// Even with aggressive pruning, keep at least this many blocks
    #[serde(default = "default_min_blocks")]
    pub min_blocks_to_keep: u64,
    
    /// Prune on startup (prune old blocks when node starts)
    #[serde(default = "default_false")]
    pub prune_on_startup: bool,
    
    /// UTXO commitments integration
    #[cfg(feature = "utxo-commitments")]
    pub utxo_commitments: Option<UtxoCommitmentsPruningConfig>,
    
    /// BIP158 filter integration
    #[cfg(feature = "bip158")]
    pub bip158_filters: Option<Bip158PruningConfig>,
}

#[cfg(feature = "utxo-commitments")]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UtxoCommitmentsPruningConfig {
    /// Keep UTXO commitments for pruned blocks
    #[serde(default = "default_true")]
    pub keep_commitments: bool,
    
    /// Keep filtered blocks (spam-filtered) for pruned range
    #[serde(default = "default_false")]
    pub keep_filtered_blocks: bool,
    
    /// Generate commitments before pruning (if not already generated)
    #[serde(default = "default_true")]
    pub generate_before_prune: bool,
    
    /// Maximum age for commitments (days, 0 = keep forever)
    #[serde(default = "default_commitment_max_age")]
    pub max_commitment_age_days: u32,
}

#[cfg(feature = "bip158")]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Bip158PruningConfig {
    /// Keep BIP158 filters for pruned blocks
    #[serde(default = "default_true")]
    pub keep_filters: bool,
    
    /// Keep filter header chain (always required for verification)
    #[serde(default = "default_true")]
    pub keep_filter_headers: bool,
    
    /// Maximum age for filters (days, 0 = keep forever)
    #[serde(default = "default_filter_max_age")]
    pub max_filter_age_days: u32,
}
```

### Enhanced Feature Configurations

We'll also enhance configurability for other features:

```rust
/// Enhanced network configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkConfig {
    /// Transport preferences (existing)
    pub transport_preference: TransportPreferenceConfig,
    
    /// Maximum peers
    pub max_peers: Option<usize>,
    
    /// Connection timeout (seconds)
    #[serde(default = "default_connection_timeout")]
    pub connection_timeout_seconds: u64,
    
    /// Message rate limiting
    pub rate_limiting: Option<RateLimitingConfig>,
    
    /// DoS protection
    pub dos_protection: Option<DosProtectionConfig>,
    
    /// Ban list sharing (existing)
    pub ban_list_sharing: Option<BanListSharingConfig>,
}

/// Enhanced storage configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageConfig {
    /// Database backend selection
    #[serde(default = "default_database_backend")]
    pub database_backend: DatabaseBackendConfig,
    
    /// Storage path
    #[serde(default = "default_storage_path")]
    pub data_dir: String,
    
    /// Pruning configuration
    pub pruning: Option<PruningConfig>,
    
    /// Cache sizes
    pub cache: Option<StorageCacheConfig>,
}

/// Enhanced RPC configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RpcConfig {
    /// RPC server address
    pub listen_addr: Option<SocketAddr>,
    
    /// Authentication (existing)
    pub auth: Option<RpcAuthConfig>,
    
    /// Rate limiting per method
    pub method_rate_limits: Option<HashMap<String, RateLimitConfig>>,
    
    /// Enable/disable specific methods
    pub enabled_methods: Option<Vec<String>>,
    
    /// CORS configuration
    pub cors: Option<CorsConfig>,
}
```

## Implementation Plan

### Phase 1: Configuration Infrastructure

**Tasks**:
1. Add `PruningConfig` to `NodeConfig`
2. Add `UtxoCommitmentsPruningConfig` (feature-gated)
3. Add `Bip158PruningConfig` (feature-gated)
4. Add enhanced configurations for other features
5. Implement configuration validation
6. Add configuration file examples

**Files to Modify**:
- `bllvm-node/src/config/mod.rs` - Add pruning and enhanced configs
- `bllvm-node/src/config/examples/` - Add example config files

### Phase 2: Pruning Manager

**Tasks**:
1. Create `PruningManager` struct
2. Implement pruning logic for each mode
3. Integrate with UTXO commitments (if enabled)
4. Integrate with BIP158 filters (if enabled)
5. Implement automatic pruning
6. Add pruning metrics

**Files to Create**:
- `bllvm-node/src/storage/pruning.rs` - Pruning manager
- `bllvm-node/src/storage/pruning_manager.rs` - Core pruning logic

**Files to Modify**:
- `bllvm-node/src/storage/mod.rs` - Integrate pruning manager
- `bllvm-node/src/storage/blockstore.rs` - Add pruning methods

### Phase 3: UTXO Commitments Integration

**Tasks**:
1. Generate UTXO commitments before pruning (if enabled)
2. Store commitments for pruned blocks
3. Verify commitments can be used for state verification
4. Integrate with `UtxoCommitmentsConfig::StorageConfig`

**Files to Modify**:
- `bllvm-node/src/storage/pruning.rs` - UTXO commitments integration
- `bllvm-node/src/network/protocol_extensions.rs` - Commitment generation before prune

### Phase 4: BIP158 Filter Integration

**Tasks**:
1. Keep filters for pruned blocks (if enabled)
2. Maintain filter header chain
3. Integrate with `BlockFilterService`

**Files to Modify**:
- `bllvm-node/src/storage/pruning.rs` - BIP158 filter integration
- `bllvm-node/src/network/filter_service.rs` - Filter retention logic

### Phase 5: RPC Integration

**Tasks**:
1. Complete `pruneblockchain` RPC method
2. Add `getpruneinfo` RPC method
3. Add pruning status to `getblockchaininfo`
4. Add pruning metrics to RPC

**Files to Modify**:
- `bllvm-node/src/rpc/blockchain.rs` - Complete pruning RPC methods
- `bllvm-node/src/rpc/server.rs` - Route new methods

### Phase 6: Testing

**Tasks**:
1. Unit tests for pruning logic
2. Integration tests for pruning with UTXO commitments
3. Integration tests for pruning with BIP158 filters
4. Tests for configuration validation
5. Performance tests for pruning operations

**Files to Create**:
- `bllvm-node/tests/storage/pruning_tests.rs`
- `bllvm-node/tests/integration/pruning_integration_tests.rs`

## Detailed Implementation

### Pruning Modes Explained

#### 1. Disabled Mode
- **Behavior**: Keep all blocks, no pruning
- **Use Case**: Archival nodes, full history required
- **Storage**: Maximum (full blockchain)

#### 2. Normal Mode
- **Behavior**: Keep recent blocks (configurable height)
- **Use Case**: Standard nodes with limited storage
- **Storage**: Reduced (recent blocks only)
- **Requirements**: Full blocks needed for verification

#### 3. Aggressive Mode (UTXO Commitments Required)
- **Behavior**: Prune aggressively, keep only commitments
- **Use Case**: Storage-constrained nodes with UTXO commitments
- **Storage**: Minimal (headers + commitments + recent blocks)
- **Requirements**: `utxo-commitments` feature enabled
- **Advantage**: Can verify state via commitments, don't need full blocks

#### 4. Custom Mode
- **Behavior**: Fine-grained control over what to keep
- **Use Case**: Specialized nodes (light client servers, analysis nodes)
- **Storage**: Configurable based on needs

### UTXO Commitments Integration

When `utxo-commitments` feature is enabled and aggressive pruning is configured:

1. **Before Pruning**:
   - Generate UTXO commitment for blocks to be pruned
   - Store commitment in dedicated storage
   - Verify commitment is valid

2. **During Pruning**:
   - Remove block bodies
   - Keep block headers (always required)
   - Keep UTXO commitments
   - Optionally keep filtered blocks

3. **After Pruning**:
   - State can be verified via commitments
   - New blocks can be validated against commitments
   - UTXO set can be reconstructed from commitments if needed

### Configuration Examples

#### Example 1: Storage-Constrained Node with UTXO Commitments

```json
{
  "storage": {
    "pruning": {
      "mode": "aggressive",
      "keep_from_height": 0,
      "keep_commitments": true,
      "keep_filtered_blocks": false,
      "min_blocks": 144
    },
    "utxo_commitments": {
      "keep_commitments": true,
      "generate_before_prune": true,
      "max_commitment_age_days": 0
    }
  }
}
```

**Result**: Keeps only headers + UTXO commitments + last 144 blocks. Can verify state via commitments.

#### Example 2: Light Client Server

```json
{
  "storage": {
    "pruning": {
      "mode": "custom",
      "keep_headers": true,
      "keep_bodies_from_height": 0,
      "keep_commitments": false,
      "keep_filters": true,
      "keep_filtered_blocks": false,
      "keep_witnesses": false,
      "keep_tx_index": false
    },
    "bip158_filters": {
      "keep_filters": true,
      "keep_filter_headers": true
    }
  }
}
```

**Result**: Keeps headers + BIP158 filters for light client support, prunes everything else.

#### Example 3: Normal Pruning (No UTXO Commitments)

```json
{
  "storage": {
    "pruning": {
      "mode": "normal",
      "keep_from_height": 0,
      "min_recent_blocks": 288
    }
  }
}
```

**Result**: Keeps last 288 blocks (2 days at 10 min/block), prunes older blocks.

## Validation Plan

### Configuration Validation

1. **Feature Flag Validation**:
   - Aggressive mode requires `utxo-commitments` feature
   - BIP158 filter config requires `bip158` feature
   - Validate feature availability before allowing config

2. **Pruning Height Validation**:
   - Cannot prune to height >= tip height
   - Must keep minimum blocks (safety margin)
   - Validate against current chain state

3. **UTXO Commitments Validation**:
   - If aggressive mode enabled, verify UTXO commitments feature available
   - Validate commitment storage is available
   - Check commitment generation capability

### Implementation Validation

1. **Pruning Correctness**:
   - Verify pruned blocks are actually removed
   - Verify headers are kept
   - Verify UTXO set remains consistent
   - Verify commitments are generated and stored

2. **State Verification**:
   - After pruning, verify state can be verified via commitments
   - Verify new blocks can be validated
   - Verify UTXO set queries work correctly

3. **Performance**:
   - Measure pruning operation time
   - Measure storage space savings
   - Measure impact on block processing

## Enhanced Configurability for Other Features

### Network Configuration Enhancements

```rust
pub struct NetworkConfig {
    // Existing fields...
    
    /// Connection management
    pub connection: ConnectionConfig,
    
    /// Message handling
    pub messages: MessageConfig,
    
    /// Peer discovery
    pub peer_discovery: PeerDiscoveryConfig,
}

pub struct ConnectionConfig {
    /// Connection timeout
    pub timeout_seconds: u64,
    
    /// Retry configuration
    pub retry: RetryConfig,
    
    /// Keep-alive settings
    pub keep_alive: KeepAliveConfig,
}

pub struct MessageConfig {
    /// Maximum message size
    pub max_message_size: usize,
    
    /// Message queue size
    pub queue_size: usize,
    
    /// Message processing threads
    pub processing_threads: usize,
}
```

### Storage Configuration Enhancements

```rust
pub struct StorageConfig {
    // Existing fields...
    
    /// Cache configuration
    pub cache: CacheConfig,
    
    /// Index configuration
    pub indexes: IndexConfig,
    
    /// Backup configuration
    pub backup: BackupConfig,
}

pub struct CacheConfig {
    /// Block cache size (MB)
    pub block_cache_mb: usize,
    
    /// UTXO cache size (MB)
    pub utxo_cache_mb: usize,
    
    /// Header cache size (MB)
    pub header_cache_mb: usize,
}
```

### RPC Configuration Enhancements

```rust
pub struct RpcConfig {
    // Existing fields...
    
    /// Method-specific configuration
    pub methods: HashMap<String, MethodConfig>,
    
    /// Batch request limits
    pub batch: BatchConfig,
    
    /// WebSocket configuration (future)
    pub websocket: Option<WebSocketConfig>,
}

pub struct MethodConfig {
    /// Enable/disable method
    pub enabled: bool,
    
    /// Rate limit for this method
    pub rate_limit: Option<RateLimitConfig>,
    
    /// Timeout for this method
    pub timeout_seconds: Option<u64>,
}
```

## Implementation Order

1. **Phase 1**: Configuration infrastructure (foundation)
2. **Phase 2**: Basic pruning manager (normal mode)
3. **Phase 3**: UTXO commitments integration (aggressive mode)
4. **Phase 4**: BIP158 filter integration
5. **Phase 5**: RPC integration
6. **Phase 6**: Enhanced configurability for other features
7. **Phase 7**: Testing and validation

## Success Criteria

1. ✅ Pruning works in all modes (disabled, normal, aggressive, custom)
2. ✅ UTXO commitments enable aggressive pruning
3. ✅ All pruning operations are configurable
4. ✅ Configuration is validated and provides clear errors
5. ✅ Pruning integrates with existing features (BIP158, spam filtering)
6. ✅ RPC methods provide pruning status and control
7. ✅ Enhanced configurability for network, storage, RPC features
8. ✅ Comprehensive tests cover all pruning modes and integrations

## Important Notes

### Pruning Irreversibility

**⚠️ WARNING**: Pruning is **irreversible**. Once blocks are pruned, they cannot be recovered unless:
- You have a backup
- You re-download from peers
- You have UTXO commitments (for state verification, not block recovery)

**Recommendation**: Always backup your data directory before enabling pruning, especially aggressive pruning.

### Pruning During IBD

**⚠️ RESTRICTION**: Pruning should **NOT** be performed during initial block download (IBD). The implementation will:
- Validate that IBD is complete before allowing pruning
- Prevent automatic pruning during IBD
- Return an error if manual pruning is attempted during IBD

### UTXO Commitments Requirement

**⚠️ REQUIREMENT**: Aggressive pruning mode **requires** the `utxo-commitments` feature to be enabled. The implementation will:
- Validate feature availability before allowing aggressive mode
- Return a clear error if aggressive mode is configured without the feature
- Suggest normal mode as an alternative

