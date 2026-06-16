# Configuration Reference

Reference for BLVM node configuration options. Configuration can be provided via TOML file, JSON file, command-line arguments, or environment variables. See [Node Configuration](../node/configuration.md) for usage examples.

**Precedence:** CLI > ENV > config file > defaults. **Canonical defaults:** This reference is the source of truth; other docs (e.g. first-node, storage-backends) give examples—use this page when you need exact defaults.

**Path expansion:** Path fields (`storage.data_dir`, `modules.modules_dir`, `ibd.dump_dir`, `ibd.snapshot_dir`) expand `~` to the home directory when loading from file.

**Operator security:** Exposure classes (RPC / P2P / QUIC), **`[rpc_auth]`** expectations, and maturity language (**required / recommended / unsupported**) — **[Deployment posture](../security/deployment-posture.md)** and **[RPC transport × authentication](../security/rpc-transport-auth-matrix.md)**.

## Configuration File Format

Configuration files support both TOML (`.toml`) and JSON (`.json`) formats. TOML is recommended for readability.

### Example Configuration File

```toml
# blvm.toml
listen_addr = "127.0.0.1:8333"
transport_preference = "tcponly"  # TOML: tcponly | irohonly | quinnonly | hybrid | all
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

## Primary settings

This section documents **BLVM `NodeConfig`** fields (the `blvm` / `blvm-node` configuration model). It is **not** a description of **Bitcoin Core**’s `bitcoin.conf`; Core uses different option names and file format. For mapping from Core, see [Bitcoin Core bitcoin.conf versus BLVM](../node/configuration.md#bitcoin-core-bitcoinconf-versus-blvm).

### Network settings

#### `listen_addr`
- **Type**: `SocketAddr` (e.g., `"127.0.0.1:8333"`)
- **Default**: `"127.0.0.1:8333"`
- **Description**: Network address to listen on for incoming P2P connections.
- **Example**: `listen_addr = "0.0.0.0:8333"` (listen on all interfaces)

#### `transport_preference`
- **Type**: `string` (enum)
- **Default** (library): TCP-only
- **TOML / JSON file**: serde uses **concatenated lowercase** variant names, e.g. **`tcponly`**, **`irohonly`**, **`quinnonly`**, **`hybrid`**, **`all`** (see `TransportPreferenceConfig` in `blvm-node`).
- **`blvm` CLI / `BLVM_NODE_TRANSPORT`**: human-readable forms such as **`tcp_only`**, **`iroh_only`**, **`hybrid`**.
- **Options** (semantic):
  - TCP-only — Bitcoin P2P compatible (default)
  - Quinn-only — requires `quinn` feature
  - Iroh-only — requires `iroh` feature
  - Hybrid — TCP + Iroh; requires `iroh` feature
  - All — requires both `quinn` and `iroh` features
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

## Block validation

Assume-valid settings map to Bitcoin Core **`-assumevalid`** / **`-assumevalidhash`**. The node merges this table into consensus **`BlockValidationConfig`** at startup.

### `block_validation.assume_valid_height`
- **Type**: `integer` (block height)
- **Default**: Network-dependent when unset — mainnet **912 683**, testnet **4 550 000**, regtest **0** (see `default_assume_valid_height_for_network` in `blvm-node`)
- **Description**: Skip script/signature verification for blocks below this height during connect. Block structure, Merkle roots, and proof-of-work are still validated.
- **Example**: `assume_valid_height = 0` (validate all scripts)

### `block_validation.assume_valid_hash`
- **Type**: `string` (32-byte block hash, hex) or omitted
- **Default**: none
- **Description**: When set, verify the block at **`assume_valid_height`** matches this hash before skipping ancestor script checks. Takes precedence over height-only configuration.

**Environment:** **`BLVM_ASSUME_VALID_HEIGHT`** overrides **`assume_valid_height`** from file.

## IBD Configuration

Parallel download and validation tuning under **`[ibd]`** (`IbdConfig`). Default **`mode = "parallel"`**. LAN peers are auto-preferred; WAN-only **`parallel`** sync uses multi-peer work-stealing unless **`BLVM_IBD_WAN_SINGLE_PEER=1`**. Bandwidth limits when **serving** IBD to peers: **`[ibd_protection]`** — [IBD Bandwidth Protection](../node/ibd-protection.md). Optional UTXO engine: **`BLVM_IBD_ENGINE=1`** — [IBD UTXO engine](../node/ibd-engine.md).

### `ibd.chunk_size`
- **Type**: `integer`
- **Default**: `128`
- **Description**: Blocks requested per download chunk. ENV **`BLVM_IBD_CHUNK_SIZE`** (allowed range 16–2000).

### `ibd.download_timeout_secs`
- **Type**: `integer` (seconds)
- **Default**: `30`
- **Description**: Per-block download timeout. ENV **`BLVM_IBD_DOWNLOAD_TIMEOUT_SECS`**.

### `ibd.mode`
- **Type**: `string`
- **Default**: `"parallel"`
- **Options**: `"parallel"`, `"sequential"`, `"earliest"` (via **`BLVM_IBD_MODE`**)
- **Description**: Download scheduler mode. **`sequential`** uses single-peer Core-like fetch.

### `ibd.preferred_peers`
- **Type**: `array` of `string` (host:port)
- **Default**: `[]`
- **Description**: Pin download peers. ENV **`BLVM_IBD_PEERS`** (comma-separated) overrides discovery.

### `ibd.max_ahead_blocks`
- **Type**: `integer` or omitted
- **Default**: none (RAM-adaptive **`MemoryGuard`**)
- **Description**: Cap blocks buffered ahead of validation. ENV **`BLVM_IBD_MAX_AHEAD`**.

### `ibd.memory_only`
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Keep IBD UTXO state in memory only (testing / constrained disk). ENV **`BLVM_IBD_MEMORY_ONLY=1`**.

### `ibd.dump_dir` / `ibd.snapshot_dir`
- **Type**: `string` (path) or omitted
- **Default**: none
- **Description**: Optional dump and snapshot directories for IBD tooling. ENV **`BLVM_IBD_DUMP_DIR`**, **`BLVM_IBD_SNAPSHOT_DIR`**.

### `ibd.yield_interval`
- **Type**: `integer` (blocks)
- **Default**: `1000`
- **Description**: Validation loop yield cadence. ENV **`BLVM_IBD_YIELD_INTERVAL`**.

### `ibd.eviction`
- **Type**: `string`
- **Default**: `"fifo"`
- **Options**: `"fifo"`, `"lifo"`, `"dynamic"` (ENV **`BLVM_IBD_EVICTION`**)

### `ibd.earliest_first`
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Assign all chunks to the fastest peer (Core-like). ENV **`BLVM_IBD_EARLIEST_FIRST=1`**.

### `ibd.prefetch_workers` / `ibd.prefetch_queue_size`
- **Type**: `integer` or omitted
- **Default**: none (auto from RAM tier)
- **Description**: UTXO prefetch pool sizing during legacy IBD path.

### `ibd.utxo_prefetch_lookahead`
- **Type**: `integer`
- **Default**: `64`
- **Description**: Blocks ahead to prefetch UTXOs for.

### `ibd.max_blocks_in_transit_per_peer`
- **Type**: `integer`
- **Default**: `128` (must stay ≥ **`chunk_size`**)
- **Description**: In-flight block permit count per peer. ENV **`BLVM_IBD_MAX_BLOCKS_IN_TRANSIT`**.

### `ibd.headers_timeout_secs`
- **Type**: `integer`
- **Default**: `30`
- **Description**: Header download timeout. ENV **`BLVM_IBD_HEADERS_TIMEOUT`**.

### `ibd.headers_max_failures`
- **Type**: `integer`
- **Default**: `10`
- **Description**: Header fetch failures before peer penalty. ENV **`BLVM_IBD_HEADERS_MAX_FAILURES`**.

**Additional IBD environment variables** (no `[ibd]` table key): **`BLVM_IBD_ENGINE`**, **`BLVM_IBD_ENGINE_PATH`**, **`BLVM_IBD_WAN_SINGLE_PEER`**, **`BLVM_IBD_CHECKPOINT_INTERVAL`**, **`BLVM_IBD_DEFER_CHECKPOINT_INTERVAL`**, **`BLVM_IBD_EXPORT_HEIGHT_OVERRIDE`**, **`BLVM_IBD_MAX_PARALLEL`**, **`BLVM_IBD_PIPELINE_DEPTH`**. See [IBD UTXO engine](../node/ibd-engine.md) and [Mainnet initial sync](../getting-started/mainnet-sync.md).

**Code**: [config/ibd.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/ibd.rs), [parallel_ibd/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/parallel_ibd/mod.rs)

## Storage Configuration

### `storage.data_dir`
- **Type**: `string` (path)
- **Default**: `"data"`
- **Description**: Directory for storing blockchain data (blocks, UTXO set, indexes).

### `storage.database_backend`
- **Type**: `string` (enum)
- **Default**: `"auto"`
- **Options**:
  - `"auto"` - Select by build features: heed3 when `heed3` feature enabled (typical default), else RocksDB, else TidesDB, else Redb, else Sled
  - `"rocksdb"` - Use RocksDB (requires `rocksdb` feature; reads common LevelDB/`blk*.dat` layouts)
  - `"tidesdb"` - Use TidesDB (if available)
  - `"heed3"` - Use heed3 / LMDB (requires `heed3` feature; UTXO values use rkyv encoding)
  - `"redb"` - Use redb (pure Rust; common when building **without** RocksDB)
  - `"sled"` - Use sled database (beta, fallback option)
- **Description**: Database backend selection. System automatically falls back if preferred backend fails.

#### `storage.heed3.map_size_mb`
- **Type**: `integer` (megabytes), optional
- **Default**: `max(65536, dbcache_mb * 128)` when unset
- **Description**: LMDB virtual memory map size. Must be large enough for the full UTXO set; cannot shrink after creation without reopening.

#### `storage.heed3.max_readers`
- **Type**: `integer`, optional
- **Default**: `512`
- **Description**: Maximum concurrent LMDB read transactions (MVCC readers).

#### `storage.heed3.max_dbs`
- **Type**: `integer`, optional
- **Default**: `KNOWN_TREE_NAMES + 8`
- **Description**: Maximum named LMDB sub-databases (trees). Set once at environment creation.

### `storage.auto_migrate_core`
- **Type**: `boolean`
- **Default**: `true`
- **Description**: When `true` and `--datadir` contains a Bitcoin Core layout (`chainstate/` + `blocks/`), **`blvm start`** runs a one-time migration into **`storage.core_migrate_destination`** or **`<datadir>/blvm/`** before opening the BLVM store. Requires **`rocksdb`** feature. Disabled by **`--no-auto-migrate`** or **`BLVM_NO_AUTO_MIGRATE_CORE=1`**.

### `storage.core_migrate_destination`
- **Type**: `string` (path), optional
- **Default**: unset (use **`<datadir>/blvm/`** when migrating from a Core datadir)
- **Description**: Override BLVM native store path for Core drop-in migration. Overridden by **`--migrate-destination`** or **`BLVM_CORE_MIGRATE_DESTINATION`**.

### `storage.reuse_core_block_files`
- **Type**: `boolean`
- **Default**: `false`
- **Description**: During Core migration, migrate UTXOs and indexes only; leave Core `blocks/` in place and read block bodies from Core `blk*.dat` via a fallback reader. Saves disk; requires Core block files to remain available. Overridden by **`BLVM_REUSE_CORE_BLOCK_FILES=1`**.

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
- `keep_filters`: Keep BIP158 filters when pruning (requires filter data on disk)
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

### BIP158 Filter Pruning

**Requires**: BIP158 filter data (always available in default node builds).

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

### `modules.registry_url`
- **Type**: `string` (URL)
- **Default**: `https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json`
- **Description**: Discovery index (`modules.json`) for bootstrap-download of pinned modules missing on disk. Requires the `governance` feature on the `blvm` build (on by default).

### `modules.enabled_modules` (version pins)
- **Type**: map of module name → semver constraint (inline `[modules]` keys, `[modules.enabled_modules]` table, or legacy array)
- **Default**: `{}` (empty — no bootstrap; discover and auto-load only modules already under `modules_dir`)
- **Description**: Allowlist of modules to auto-load. Each entry may include a **version constraint**. When `registry_url` is set, missing modules (or on-disk versions that do not match the constraint) are **bootstrap-downloaded** from each module’s GitHub Releases (highest release matching the constraint).
- **Constraints**: `0.1.*` (same major/minor), `0.*` (same major), exact `0.1.2`, or `*` / legacy array entry (unpinned — manifest from `main`, floating version).
- **Example (inline pins)**:
```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-miniscript = "0.1.*"
blvm-zmq = "0.3.*"
```
- **Example (spawn overrides + pin — use `version` in the module table; inline `name = "…"` conflicts with `[modules.name]` in TOML)**:
```toml
[modules.blvm-zmq]
version = "0.3.*"
hashblock = "tcp://127.0.0.1:28332"
```
- **Legacy (unpinned)**:
```toml
enabled_modules = ["blvm-miniscript", "blvm-zmq"]
```

### `modules.disabled_modules`
- **Type**: `array` of `string`
- **Default**: `[]`
- **Description**: Module manifest names to never auto-load or bootstrap. Wins over `enabled_modules` if both list the same name.

### `modules.module_configs`
- **Type**: per-module override tables under `[modules.<name>]`
- **Default**: none
- **Description**: Module-specific configuration overrides (merged into module spawn env). Use a `version = "0.1.*"` key in the same table when the module also needs spawn settings (see above).
- **Example**:
```toml
[modules.lightning-module]
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
- **See also**: [RPC transport × authentication](../security/rpc-transport-auth-matrix.md) (TCP HTTP vs QUIC vs REST).

### `rpc_auth.tokens`
- **Type**: `array` of `string`
- **Default**: `[]`
- **Description**: Bearer tokens (`Authorization: Bearer …`). Read-only unless also listed in `admin_tokens`.
- **Example**: `tokens = ["token1", "token2"]`

### `rpc_auth.admin_tokens`
- **Type**: `array` of `string`
- **Default**: `[]`
- **Description**: Tokens with admin privileges (`getblocktemplate`, `submitblock`, `generatetoaddress`, `stop`, etc.). Bearer tokens in `tokens` / `token_file` must appear here (or use `[rpc_auth].password` for HTTP Basic) to call admin methods; an empty list means no bearer token is admin by default.
- **Example**: `admin_tokens = ["mining-admin-token"]`

### `rpc_auth.username`
- **Type**: `string` (optional)
- **Default**: none
- **Description**: HTTP Basic auth username (Bitcoin Core / ckpool `auth`). If omitted, any username is accepted when the password matches.

### `rpc_auth.password`
- **Type**: `string` (optional)
- **Default**: none
- **Description**: HTTP Basic auth password (ckpool `pass`, `curl -u`). Automatically registered as **admin** when set. Use only on loopback RPC or behind TLS.

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
target_peer_count = 8                    # Target outbound peers (typical deployments use a similar range)
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
# Optional pool / upstream URL for merge-mining or related orchestration (not the miner-facing TCP bind)
pool_url = "tcp://pool.example.com:3333"
# Informational on the node config only — dedicated miner TCP is bound by the blvm-stratum-v2 module
listen_addr = "127.0.0.1:3333"
p2p_stratum_demux = true                   # false = disable P2P Stratum TLV demux (module miner TCP unchanged)
transport_preference = "tcponly"
merge_mining_enabled = false
secondary_chains = []
```

**Note:** `transport_preference` inside `[stratum_v2]` follows the same serde rules as the top-level field; in TOML prefer `tcponly` / variants per `TransportPreferenceConfig`.

## Command-Line Arguments

Configuration can be overridden via command-line arguments. CLI overrides ENV and config file.

**Global:** `--network` / `-n`, `--rpc-addr` / `-r`, `--listen-addr` / `-l`, `--data-dir` / `-d`, `--config` / `-c`, `--verbose` / `-v`

**Advanced:** `--assumevalid`, `--noassumevalid`, `--assumeutxo`, `--target-peer-count`, `--async-request-timeout`, `--module-max-cpu-percent`, `--module-max-memory-bytes`

**Feature flags:** `--enable-stratum-v2`, `--enable-dandelion`, `--enable-sigop` and `--disable-*` counterparts (each requires the matching **compile-time** feature in the `blvm` / `blvm-node` binary). **`--enable-bip158` / `--disable-bip158`** only record **logged** preference—BIP158 filter code is **always** included in default builds (no `bip158` Cargo feature).

| `--verbose` | `-v` | false | Verbose logging |
| `--no-auto-migrate` | | false | Skip Core datadir auto-migration on start (`rocksdb` builds) |
| `--migrate-destination` | | — | BLVM store path for Core migration (default `<datadir>/blvm`) |
| `--migrate-core-only` | | false | Migrate from Core datadir and exit |

**Commands:** `start` (default), `status`, `health`, `version`, `chain`, `peers`, `network`, `sync`, `config show|validate|path`, `migrate core` (`rocksdb`), `rpc`

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
export BLVM_ASSUME_VALID_HEIGHT=912683
export BLVM_IBD_EVICTION=dynamic
export BLVM_IBD_ENGINE=1
export BLVM_IBD_WAN_SINGLE_PEER=1
export BLVM_NETWORK_TARGET_PEER_COUNT=125
```

**Key ENV categories:** Node (`BLVM_DATA_DIR`, `BLVM_NETWORK`, `BLVM_LISTEN_ADDR`, `BLVM_RPC_ADDR`), Core drop-in (`BLVM_AUTO_MIGRATE_CORE`, `BLVM_NO_AUTO_MIGRATE_CORE`, `BLVM_CORE_MIGRATE_DESTINATION`, `BLVM_REUSE_CORE_BLOCK_FILES`, `BLVM_CORE_MIGRATE_BLOCK_WORKERS`, `BLVM_CORE_MIGRATE_BLOCK_BATCH`), Block validation (`BLVM_ASSUME_VALID_HEIGHT`), Network timing (`BLVM_NETWORK_TARGET_PEER_COUNT`, `BLVM_NETWORK_PEER_CONNECTION_DELAY`), Request timeouts (`BLVM_REQUEST_ASYNC_TIMEOUT`, etc.), Module limits (`BLVM_MODULE_MAX_*`), IBD (`BLVM_IBD_*`, including `BLVM_IBD_ENGINE`, `BLVM_IBD_WAN_SINGLE_PEER`), Storage (`BLVM_DBCACHE_MB`, `BLVM_ROCKSDB_*`), External (`RPC_AUTH_TOKENS`, `COMMONS_API_KEY`, `RUST_LOG`).

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
- [Storage Backends](../node/storage-backends.md) - Backend selection and Core drop-in
- [Transport Abstraction](../protocol/network-protocol.md#transport-abstraction-layer) - Transport options
- [Building modules](../sdk/module-development.md) - Module system details
