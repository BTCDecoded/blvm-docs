# Configuration Defaults

<!-- Auto-generated from source code -->
<!-- Regenerate: cd bllvm-docs && python3 tools/extract-defaults.py -->

## bllvm-node Defaults

### Storage Configuration

| Setting | Default Value | Source |
|---------|---------------|--------|
| `block.cache.mb` | 100 | `default_block_cache_mb()` |
| `header.cache.mb` | 10 | `default_header_cache_mb()` |
| `pruning.mode` | true | `default_pruning_mode()` |
| `storage.path` | "data" | `default_storage_path()` |
| `utxo.cache.mb` | 50 | `default_utxo_cache_mb()` |

### Network Configuration

| Setting | Default Value | Source |
|---------|---------------|--------|
| `addr.relay.min.interval` | 8640 (2.4 hours) | `default_addr_relay_min_interval()` |
| `address.db.expiration` | 86400 | `default_address_db_expiration()` |
| `address.db.max.addresses` | 10000 | `default_address_db_max_addresses()` |
| `async.request.timeout` | 300 (5 minutes) | `default_async_request_timeout()` |
| `dandelion.stem.timeout` | 10 | `default_dandelion_stem_timeout()` |
| `dos.max.active.connections` | 200 | `default_dos_max_active_connections()` |
| `dos.max.connections.per.window` | 10 | `default_dos_max_connections_per_window()` |
| `max.addresses.from.dns` | 100 | `default_max_addresses_from_dns()` |
| `max.addresses.per.addr.message` | 1000 | `default_max_addresses_per_addr_message()` |
| `module.socket.timeout` | 5 | `default_module_socket_timeout()` |
| `peer.connection.delay` | 2 | `default_peer_connection_delay()` |
| `peer.rate.burst` | 100 | `default_peer_rate_burst()` |
| `peer.rate.rate` | 10 | `default_peer_rate_rate()` |
| `target.peer.count` | 8 | `default_target_peer_count()` |
| `utxo.commitment.timeout` | 30 | `default_utxo_commitment_timeout()` |

### RPC Configuration

| Setting | Default Value | Source |
|---------|---------------|--------|
| `rate.limit.burst` | 100 | `default_rate_limit_burst()` |
| `rate.limit.rate` | 10 | `default_rate_limit_rate()` |

### Modules Configuration

| Setting | Default Value | Source |
|---------|---------------|--------|
| `module.max.child.processes` | 10 | `default_module_max_child_processes()` |
| `module.max.cpu.percent` | 50 | `default_module_max_cpu_percent()` |
| `module.max.file.descriptors` | 256 | `default_module_max_file_descriptors()` |
| `module.max.memory.bytes` | 536870912 | `default_module_max_memory_bytes()` |
| `module.socket.check.interval` | 100 | `default_module_socket_check_interval()` |
| `module.socket.max.attempts` | 50 | `default_module_socket_max_attempts()` |
| `module.startup.wait.millis` | 100 | `default_module_startup_wait_millis()` |
| `modules.data.dir` | "data/modules" | `default_modules_data_dir()` |
| `modules.dir` | "modules" | `default_modules_dir()` |
| `modules.socket.dir` | "data/modules/sockets" | `default_modules_socket_dir()` |

### DoS Protection Configuration

| Setting | Default Value | Source |
|---------|---------------|--------|
| `dos.auto.ban.threshold` | 3 | `default_dos_auto_ban_threshold()` |
| `dos.ban.duration` | 3600 (1 hour) | `default_dos_ban_duration()` |
| `dos.max.message.queue.size` | 10000 | `default_dos_max_message_queue_size()` |
| `dos.window.seconds` | 60 | `default_dos_window_seconds()` |
| `min.ban.duration` | 3600 (1 hour) | `default_min_ban_duration()` |

### Other Configuration

| Setting | Default Value | Source |
|---------|---------------|--------|
| `auto.prune.interval` | 144 (Prune every ~1 day at 10 min/block) | `default_auto_prune_interval()` |
| `commitment.max.age` | 0 (Keep forever by default) | `default_commitment_max_age()` |
| `dandelion.fluff.probability` | 1 (10%) | `default_dandelion_fluff_probability()` |
| `dandelion.max.stem.hops` | 2 | `default_dandelion_max_stem_hops()` |
| `filter.max.age` | 0 (Keep forever by default) | `default_filter_max_age()` |
| `min.blocks` | 144 (~1 day at 10 min/block) | `default_min_blocks()` |
| `min.blocks.for.incremental.prune` | 288 (Start incremental pruning after 288 blocks (~2 days) to ensure stability) | `default_min_blocks_for_incremental_prune()` |
| `min.blocks.to.keep` | 144 (~1 day at 10 min/block) | `default_min_blocks_to_keep()` |
| `min.recent.blocks` | 288 (~2 days at 10 min/block) | `default_min_recent_blocks()` |
| `pending.request.max.age` | 300 (5 minutes) | `default_pending_request_max_age()` |
| `periodic.interval` | 300 (5 minutes) | `default_periodic_interval()` |
| `prune.window.size` | 144 (Keep last 144 blocks (~1 day) during incremental pruning) | `default_prune_window_size()` |
| `relay.max.age` | 3600 (1 hour) | `default_relay_max_age()` |
| `relay.max.tracked.items` | 10000 | `default_relay_max_tracked_items()` |
| `request.cleanup.interval` | 60 | `default_request_cleanup_interval()` |

[Source: bllvm-node/src/config/mod.rs](../../bllvm-node/src/config/mod.rs)

## bllvm-commons Defaults

| Setting | Default Value | Source |
|---------|---------------|--------|
| `network` | "mainnet" | `default_network()` |
| `weight.update.interval` | 86400 (Daily) | `default_weight_update_interval()` |

[Source: bllvm-commons/bllvm-commons/src/config.rs](../../bllvm-commons/bllvm-commons/src/config.rs)
