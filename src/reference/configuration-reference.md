# Configuration Reference

Reference for BLVM node configuration options. Configuration can be provided via TOML file, JSON file, command-line arguments, or environment variables. See [Node Configuration](../node/configuration.md) for usage examples.

**Precedence:** CLI > ENV > config file > defaults. **Canonical defaults:** This reference is the single source of truth for default values; other docs (e.g. first-node, storage-backends) may show examples and should point here for authoritative defaults.

**Path expansion:** Path fields (`storage.data_dir`, `modules.modules_dir`, `ibd.dump_dir`, `ibd.snapshot_dir`) expand `~` to the home directory when loading from file.

## Configuration File Format

Configuration files support both TOML (`.toml`) and JSON (`.json`) formats. TOML is recommended for readability.

### Example Configuration File

```toml
# blvm.toml
listen_addr = "127.0.0.1:8333"
transport_preference = "tcp_only"
max_peers = 100
protocol_version = "BitcoinV1"

[storage]
data_dir = "/var/lib/blvm"
database_backend = "auto"

[storage.cache]
block_cache_mb = 100
utxo_cache_mb = 50
header_cache_mb = 10

[storage.pruning]
mode = { type = "normal", keep_from_height = 0, min_recent_blocks = 288 }
auto_prune = true
auto_prune_interval = 144

[modules]
enabled = true
modules_dir = "modules"
data_dir = "data/modules"

[rpc_auth]
required = false
rate_limit_burst = 100
rate_limit_rate = 10
```

## Core Configuration

### Network Settings

#### `listen_addr`
- **Type**: `SocketAddr` (e.g., `"127.0.0.1:8333"`)
- **Default**: `"127.0.0.1:8333"`
- **Description**: Network address to listen on for incoming P2P connections.
- **Example**: `listen_addr = "0.0.0.0:8333"` (listen on all interfaces)

#### `transport_preference`
- **Type**: `string` (enum)
- **Default**: `"tcp_only"`
- **Options**:
  - `"tcp_only"` - Use only TCP transport (Bitcoin P2P compatible, default)
  - `"quinn_only"` - Use only Quinn/QUIC transport (requires `quinn` feature)
  - `"iroh_only"` - Use only Iroh transport (requires `iroh` feature, experimental)
  - `"hybrid"` - Use both TCP and Iroh simultaneously (requires `iroh` feature)
  - `"all"` - Use all available transports (requires both `quinn` and `iroh` features)
- **Description**: Transport protocol selection. See [Transport Abstraction](../node/transport-abstraction.md) for details.

#### `max_peers`
- **Type**: `integer`
- **Default**: `100`
- **Description**: Maximum number of simultaneous peer connections.

#### `protocol_version`
- **Type**: `string`
- **Default**: `"BitcoinV1"`
- **Options**: `"BitcoinV1"` (mainnet), `"Testnet3"` (testnet), `"Regtest"` (regtest)
- **Description**: Bitcoin protocol variant. See [Network Variants](../protocol/network-protocol.md#network-variants).

#### `persistent_peers`
- **Type**: `array` of `SocketAddr`
- **Default**: `[]`
- **Description**: List of peer addresses to connect to on startup. Format: `["192.168.1.1:8333", "example.com:8333"]`
- **Example**: `persistent_peers = ["192.168.1.1:8333", "10.0.0.1:8333"]`

#### `enable_self_advertisement`
- **Type**: `boolean`
- **Default**: `true`
- **Description**: Whether to advertise own address to peers. Set to `false` for privacy.

## IBD Configuration

Initial block download uses parallel IBD only. **`[ibd]`** (top-level): chunk_size, download_timeout_secs, mode, eviction, max_blocks_in_transit_per_peer, headers_timeout_secs, headers_max_failures; optional: preferred_peers, max_ahead_blocks, memory_only, dump_dir, snapshot_dir, yield_interval, earliest_first, prefetch_*, utxo_prefetch_lookahead. **`[ibd_protection]`** (top-level): bandwidth limits per peer/IP/subnet. `max_concurrent_per_peer` is fixed at 64 in code (not in config). See [Node Configuration](../node/configuration.md#ibd-configuration) and [IBD Protection](../node/ibd-protection.md); ENV: `BLVM_IBD_*`.

## Storage Configuration

### `storage.data_dir`
- **Type**: `string` (path)
- **Default**: `"data"`
- **Description**: Directory for storing blockchain data (blocks, UTXO set, indexes).

### `storage.database_backend`
- **Type**: `string` (enum)
- **Default**: `"auto"`
- **Options**:
  - `"auto"` - Select by build features: RocksDB when `rocksdb` feature enabled (typical default), else TidesDB, else Redb, else Sled
  - `"rocksdb"` - Use RocksDB (requires `rocksdb` feature, Bitcoin Core compatible)
  - `"redb"` - Use redb database (production-ready)
  - `"sled"` - Use sled database (beta, fallback option)
  - `"tidesdb"` - Use TidesDB (if available)
- **Description**: Database backend selection. System automatically falls back if preferred backend fails.

### Storage Cache

#### `storage.cache.block_cache_mb`
- **Type**: `integer` (megabytes)
- **Default**: `100`
- **Description**: Size of block cache in megabytes. Caches recently accessed blocks.

#### `storage.cache.utxo_cache_mb`
- **Type**: `integer` (megabytes)
- **Default**: `50`
- **Description**: Size of UTXO cache in megabytes. Caches frequently accessed UTXOs.

#### `storage.cache.header_cache_mb`
- **Type**: `integer` (megabytes)
- **Default**: `10`
- **Description**: Size of header cache in megabytes. Caches block headers.

### Pruning Configuration

#### `storage.pruning.mode`
- **Type**: `object` (enum with variants)
- **Default**: Aggressive (configurable; for full archival nodes use Disabled or Normal)
- **Options**: Disabled, Normal (`keep_from_height`, `min_recent_blocks`), Aggressive (`keep_from_height`, `keep_commitments`, `keep_filtered_blocks`, `min_blocks`), Custom (fine-grained control)
- **Description**: Pruning mode configuration. See [Pruning Modes](#pruning-modes) below.

#### `storage.pruning.auto_prune`
- **Type**: `boolean`
- **Default**: `true` (if mode is Aggressive), `false` otherwise
- **Description**: Automatically prune old blocks periodically as chain grows.

#### `storage.pruning.auto_prune_interval`
- **Type**: `integer` (blocks)
- **Default**: `144` (~1 day at 10 min/block)
- **Description**: Prune every N blocks when `auto_prune` is enabled.

#### `storage.pruning.min_blocks_to_keep`
- **Type**: `integer` (blocks)
- **Default**: `144` (~1 day at 10 min/block)
- **Description**: Minimum number of blocks to keep as safety margin, even with aggressive pruning.

#### `storage.pruning.prune_on_startup`
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Prune old blocks when node starts (if they exceed configured limits).

#### `storage.pruning.incremental_prune_during_ibd`
- **Type**: `boolean`
- **Default**: `true` (if Aggressive mode)
- **Description**: Prune old blocks incrementally during initial block download (IBD), keeping only a sliding window. Requires UTXO commitments.

#### `storage.pruning.prune_window_size`
- **Type**: `integer` (blocks)
- **Default**: `144` (~1 day)
- **Description**: Number of recent blocks to keep during incremental pruning (sliding window).

#### `storage.pruning.min_blocks_for_incremental_prune`
- **Type**: `integer` (blocks)
- **Default**: `288` (~2 days)
- **Description**: Minimum blocks before starting incremental pruning during IBD.

### Pruning Modes

#### Disabled Mode
```toml
[storage.pruning]
mode = { type = "disabled" }
```
Keep all blocks. No pruning performed.

#### Normal Mode
```toml
[storage.pruning]
mode = { type = "normal", keep_from_height = 0, min_recent_blocks = 288 }
```
- `keep_from_height`: Keep blocks from this height onwards (default: `0`)
- `min_recent_blocks`: Keep at least this many recent blocks (default: `288` = ~2 days)

#### Aggressive Mode
```toml
[storage.pruning]
mode = { type = "aggressive", keep_from_height = 0, keep_commitments = true, keep_filtered_blocks = false, min_blocks = 144 }
```
**Requires**: `utxo-commitments` feature enabled.

- `keep_from_height`: Keep blocks from this height onwards (default: `0`)
- `keep_commitments`: Keep UTXO commitments for pruned blocks (default: `true`)
- `keep_filtered_blocks`: Keep spam-filtered blocks for pruned range (default: `false`)
- `min_blocks`: Minimum blocks to keep as safety margin (default: `144` = ~1 day)

#### Custom Mode
```toml
[storage.pruning]
mode = { 
    type = "custom",
    keep_headers = true,              # Always required for PoW verification
    keep_bodies_from_height = 0,
    keep_commitments = false,
    keep_filters = false,
    keep_filtered_blocks = false,
    keep_witnesses = false,
    keep_tx_index = false
}
```
Fine-grained control over what data to keep:
- `keep_headers`: Keep block headers (always required, default: `true`)
- `keep_bodies_from_height`: Keep block bodies from this height onwards
- `keep_commitments`: Keep UTXO commitments (if feature enabled)
- `keep_filters`: Keep BIP158 filters (if feature enabled)
- `keep_filtered_blocks`: Keep spam-filtered blocks
- `keep_witnesses`: Keep witness data (for SegWit verification)
- `keep_tx_index`: Keep transaction index

### UTXO Commitments Pruning (Experimental)

**Requires**: `utxo-commitments` feature enabled.

```toml
[storage.pruning.utxo_commitments]
keep_commitments = true
keep_filtered_blocks = false
generate_before_prune = true
max_commitment_age_days = 0  # 0 = keep forever
```

### BIP158 Filter Pruning (Experimental)

**Requires**: `bip158` feature enabled.

```toml
[storage.pruning.bip158_filters]
keep_filters = true
keep_filter_headers = true  # Always required for verification
max_filter_age_days = 0  # 0 = keep forever
```

## Module System Configuration

### `modules.enabled`
- **Type**: `boolean`
- **Default**: `true`
- **Description**: Enable the module system. Set to `false` to disable all modules.

### `modules.modules_dir`
- **Type**: `string` (path)
- **Default**: `"modules"`
- **Description**: Directory containing module binaries and manifests.

### `modules.data_dir`
- **Type**: `string` (path)
- **Default**: `"data/modules"`
- **Description**: Directory for module data (state, configs, logs).

### `modules.socket_dir`
- **Type**: `string` (path)
- **Default**: `"data/modules/sockets"`
- **Description**: Directory for IPC sockets used for module communication.

### `modules.enabled_modules`
- **Type**: `array` of `string`
- **Default**: `[]` (empty = auto-discover all modules)
- **Description**: List of module names to enable. Empty list enables all discovered modules.
- **Example**: `enabled_modules = ["lightning-module", "mining-module"]`

### `modules.module_configs`
- **Type**: `object` (nested key-value pairs)
- **Default**: `{}`
- **Description**: Module-specific configuration overrides.
- **Example**:
```toml
[modules.module_configs.lightning-module]
port = "9735"
network = "mainnet"
```

### Module Resource Limits

```toml
[module_resource_limits]
default_max_cpu_percent = 50              # CPU limit (0-100%)
default_max_memory_bytes = 536870912     # Memory limit (512 MB)
default_max_file_descriptors = 256       # File descriptor limit
default_max_child_processes = 10         # Child process limit
module_startup_wait_millis = 100         # Startup wait time
module_socket_timeout_seconds = 5        # Socket timeout
module_socket_check_interval_millis = 100
module_socket_max_attempts = 50
```

## RPC Configuration

### `rpc_auth.required`
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Require authentication for RPC requests. Set to `true` for production.

### `rpc_auth.tokens`
- **Type**: `array` of `string`
- **Default**: `[]`
- **Description**: Valid authentication tokens for RPC access.
- **Example**: `tokens = ["token1", "token2"]`

### `rpc_auth.certificates`
- **Type**: `array` of `string`
- **Default**: `[]`
- **Description**: Valid certificate fingerprints for certificate-based authentication.

### `rpc_auth.rate_limit_burst`
- **Type**: `integer`
- **Default**: `100`
- **Description**: RPC rate limit burst size (token bucket).

### `rpc_auth.rate_limit_rate`
- **Type**: `integer`
- **Default**: `10`
- **Description**: RPC rate limit (requests per second).

## Network Configuration

### Network Timing

```toml
[network_timing]
target_peer_count = 8                    # Target number of peers (Bitcoin Core uses 8-125)
peer_connection_delay_seconds = 2         # Wait before connecting to database peers
addr_relay_min_interval_seconds = 8640   # Min interval between addr broadcasts (2.4 hours)
max_addresses_per_addr_message = 1000   # Max addresses per addr message
max_addresses_from_dns = 100             # Max addresses from DNS seeds
```

### Request Timeouts

```toml
[request_timeouts]
async_request_timeout_seconds = 300       # Timeout for async requests (getheaders, getdata)
utxo_commitment_request_timeout_seconds = 30
request_cleanup_interval_seconds = 60    # Cleanup interval for expired requests
pending_request_max_age_seconds = 300    # Max age before cleanup
```

### DoS Protection

```toml
[dos_protection]
max_connections_per_window = 10           # Max connections per IP per window
window_seconds = 60                       # Time window for rate limiting
max_message_queue_size = 10000           # Max message queue size
max_active_connections = 200             # Max active connections
auto_ban_threshold = 3                   # Violations before auto-ban
ban_duration_seconds = 3600              # Ban duration (1 hour)
```

### Relay Configuration

```toml
[relay]
max_relay_age = 3600                     # Max age for relayed items (1 hour)
max_tracked_items = 10000                # Max items to track
enable_block_relay = true                # Enable block relay
enable_tx_relay = true                   # Enable transaction relay
enable_dandelion = false                 # Enable Dandelion++ privacy relay
```

### Address Database

```toml
[address_database]
max_addresses = 10000                    # Max addresses to store
expiration_seconds = 86400               # Address expiration (24 hours)
```

### Peer Rate Limiting

```toml
[peer_rate_limiting]
default_burst = 100                      # Token bucket burst size
default_rate = 10                        # Messages per second
```

### Ban List Sharing

```toml
[ban_list_sharing]
enabled = true                           # Enable ban list sharing
share_mode = "periodic"                  # "immediate", "periodic", or "disabled"
periodic_interval_seconds = 300          # Sharing interval (5 minutes)
min_ban_duration_to_share = 3600         # Min ban duration to share (1 hour)
```

## Experimental Features

### Dandelion++ Privacy Relay

**Requires**: `dandelion` feature enabled.

```toml
[dandelion]
stem_timeout_seconds = 10               # Stem phase timeout
fluff_probability = 0.1                 # Probability of fluffing at each hop (10%)
max_stem_hops = 2                       # Max stem hops before forced fluff
```

### Stratum V2 Mining

**Requires**: `stratum-v2` feature enabled.

```toml
[stratum_v2]
enabled = false
pool_url = "tcp://pool.example.com:3333"  # Pool URL for miner mode
listen_addr = "127.0.0.1:3333"            # Listen address for server mode
transport_preference = "tcp_only"
merge_mining_enabled = false
secondary_chains = []
```

## Command-Line Arguments

Configuration can be overridden via command-line arguments. CLI overrides ENV and config file.

**Global:** `--network` / `-n`, `--rpc-addr` / `-r`, `--listen-addr` / `-l`, `--data-dir` / `-d`, `--config` / `-c`, `--verbose` / `-v`

**Advanced:** `--assumevalid`, `--noassumevalid`, `--assumeutxo`, `--target-peer-count`, `--async-request-timeout`, `--module-max-cpu-percent`, `--module-max-memory-bytes`

**Feature flags:** `--enable-stratum-v2`, `--enable-bip158`, `--enable-dandelion`, `--enable-sigop` and `--disable-*` counterparts

**Commands:** `start` (default), `status`, `health`, `version`, `chain`, `peers`, `network`, `sync`, `config show|validate|path`, `rpc`

```bash
blvm --config /path/to/config.toml
blvm --network mainnet --data-dir /var/lib/blvm
blvm config show
```

CLI behavior is documented in this section; run `blvm --help` for the full generated flag list.

## Environment Variables

Configuration can also be set via environment variables (prefixed with `BLVM_`). ENV overrides config file.

```bash
export BLVM_NETWORK=testnet
export BLVM_DATA_DIR=/var/lib/blvm
export BLVM_RPC_ADDR=127.0.0.1:8332
export BLVM_IBD_EVICTION=dynamic
export BLVM_NETWORK_TARGET_PEER_COUNT=125
```

**Key ENV categories:** Node (`BLVM_DATA_DIR`, `BLVM_NETWORK`, `BLVM_LISTEN_ADDR`, `BLVM_RPC_ADDR`), Network timing (`BLVM_NETWORK_TARGET_PEER_COUNT`, `BLVM_NETWORK_PEER_CONNECTION_DELAY`), Request timeouts (`BLVM_REQUEST_ASYNC_TIMEOUT`, etc.), Module limits (`BLVM_MODULE_MAX_*`), IBD (`BLVM_IBD_*`), Storage (`BLVM_DBCACHE_MB`, `BLVM_ROCKSDB_*`), External (`RPC_AUTH_TOKENS`, `COMMONS_API_KEY`, `RUST_LOG`).

Additional or experimental `BLVM_*` names may exist; use `blvm --help` and the node’s config schema as the source of truth in this repository.

## Configuration Precedence

1. **Command-line arguments** (highest priority)
2. **Environment variables** (e.g. `BLVM_DATA_DIR`, `BLVM_IBD_EVICTION`)
3. **Configuration file**
4. **Default values** (lowest priority)

**Config-file-only options:** `relay`, `fibre`, `dandelion`, `peer_rate_limiting`, `rest_api`, `ban_list_sharing` have no ENV overrides. Use CLI flags (e.g. `--enable-dandelion`) or config file.

## Validation

The node validates configuration on startup. Invalid configurations will cause the node to exit with an error message indicating the problem.

Common validation errors:
- Pruning mode requires features that aren't enabled
- Invalid network addresses
- Resource limits set to zero
- Conflicting transport preferences

## See Also

- [Node Configuration](../node/configuration.md) - Quick start guide
- [Storage Backends](../node/configuration.md#storage-backends) - Backend selection details
- [Transport Abstraction](../protocol/network-protocol.md#transport-abstraction-layer) - Transport options
- [Module Development](../sdk/module-development.md) - Module system details
