# Configuration reference

`NodeConfig` is the node file. The `blvm` binary merges CLI, then the environment variables it reads, then this file, then the built-in default. An omitted table stays at that default. A present table fills every key in the table. Unknown keys are ignored.

`protocol_version` accepts `mainnet`, `testnet`, `testnet4`, `signet`, and `regtest`. `BitcoinV1` and `Testnet3` are aliases. The binary writes the five names above.

There is no `[payment]` table on `NodeConfig`. `blvm-payment` reads its own module file. `[stratum_v2]` has one field, `p2p_stratum_demux` (default true). Miner TCP is the `blvm-stratum-v2` module.

## Top level

| Key | Meaning |
|---|---|
| `listen_addr` | P2P bind. Absent uses the network default port. |
| `rpc_addr` | RPC bind. Absent uses the network default. CLI and `BLVM_RPC_ADDR` win. |
| `max_peers` | Maximum outbound peers. |
| `protocol_version` | Chain name. |
| `transport_preference` | `tcponly`, `irohonly`, `quinnonly`, `hybrid`, or `all`. |
| `signet_challenge` | Hex script for a custom signet. |
| `enable_self_advertisement` | Send this node's address to peers. |
| `serve_compact_filters` | Serve BIP158 filters. |
| `persistent_peers` | Socket addresses to dial on start. |
| `assumeutxo_blockhash` | Block hash of an AssumeUTXO snapshot. |

`[block_validation]` holds `assume_valid_height` and `assume_valid_hash`. A 64-character block id is stored in internal byte order. Signatures skip only when the block height is below that height, chainwork meets the minimum, and the hash is set. The mainnet seed stores the checked hash at height `912683`. A seeded height with no hash, which is still the case for testnet and signet, does not skip. `BLVM_ASSUME_VALID_HEIGHT` overrides the height only.

## `[logging]`

`filter` (alias `level`) and `json_format`. The subscriber uses `RUST_LOG`, then `BLVM_LOG_LEVEL`, then `filter`, then `--verbose` (`blvm=debug,blvm_node=debug`), then `blvm=info,blvm_node=info`. `json_format` emits JSON only when the `json-logging` feature is compiled in. That feature is off the default build. Without it, the process keeps the text subscriber and warns once.

## `[mempool]` and `[rbf]`

`[mempool]` is the node pool: `max_mempool_mb`, `max_mempool_txs`, `min_relay_fee_rate`, `bytes_per_sigop`, `count_sigops`, `min_tx_fee`, `incremental_relay_fee`, `max_ancestor_count`, `max_ancestor_size`, `max_descendant_count`, `max_descendant_size`, `eviction_strategy`, `mempool_expiry_hours`, `persist_mempool`, `mempool_persistence_path`, `tx_rate_limit_burst`, `tx_rate_limit_per_sec`, `tx_byte_rate_limit`, `tx_byte_rate_burst`, `require_standard`, `reject_spam_in_mempool`, `spam_filter`.

When `[mempool]` or `[rbf]` is present, those sizes are copied onto the consensus mempool global. Admission does not call the consensus mempool checker.

`[rbf]`: `mode` (`disabled`, `conservative`, `standard`, `aggressive`), `min_fee_rate_multiplier`, `min_fee_bump_satoshis`, `min_confirmations`, `allow_package_replacements`, `max_replacements_per_tx`, `cooldown_seconds`.

## `[storage]`

`database_backend`, `data_dir`, `dbcache_mb`, `auto_migrate_core`, `core_migrate_destination`, `reuse_core_block_files`.

`[storage.rocksdb]`: `parallelism`, `max_background_compactions`, `max_background_flushes`, `level0_compaction_trigger`, `write_buffer_mb`. The environment wins over the file, and the file wins over the built-in default.

`[storage.heed3]`: `map_size_mb`, `max_readers`, `max_dbs`. A caller override wins, then the environment, then the file, then disk auto-tune for the map size.

`[storage.cache]`: `block_cache_mb`, `utxo_cache_mb`, `header_cache_mb`.

`[storage.indexing]`: `enable_address_index`, `enable_value_index`, `strategy`, `max_indexed_addresses`, `enable_compression`, `background_indexing`.

`[storage.compression]`: `block_compression_enabled`, `block_compression_level`, `utxo_compression_enabled`, `utxo_compression_level`, `witness_compression_enabled`, `witness_compression_level`.

`[storage.pruning]`: `mode`, `auto_prune`, `auto_prune_interval`, `min_blocks_to_keep`, `prune_on_startup`, `incremental_prune_during_ibd`, `prune_window_size`, `min_blocks_for_incremental_prune`, `utxo_commitments`, `bip158_filters`.

## `[ibd]`

Operator surface, including `dump_dir`. Fields: `chunk_size`, `download_timeout_secs`, `mode`, `preferred_peers`, `max_ahead_blocks`, `memory_only`, `dump_dir`, `snapshot_dir`, `yield_interval`, `eviction`, `earliest_first`, `prefetch_workers`, `prefetch_queue_size`, `utxo_prefetch_lookahead`, `max_blocks_in_transit_per_peer`, `headers_timeout_secs`, `headers_max_failures`, `dedicated`, `utxo_engine`, `checkpoint_interval`, `checkpoint_min_interval`, `checkpoint_max_interval`, `checkpoint_target_secs`, `muhash_persist_interval`.

The parallel IBD assignment checkpoint stays a code constant. Bench and dest latches stay environment variables. They are not keys in this table.

## Network, RPC, and limits

`[dos_protection]`: `max_connections_per_window`, `window_seconds`, `max_message_queue_size`, `max_active_connections`, `auto_ban_threshold`, `ban_duration_seconds`.

`[spam_ban]`: `spam_ban_threshold`, `spam_ban_duration_seconds`.

`[relay]`: `max_relay_age`, `max_tracked_items`, `enable_block_relay`, `enable_tx_relay`, `enable_dandelion`.

`[address_database]`: `max_addresses`, `expiration_seconds`.

`[dandelion]`, when the feature is compiled in: `stem_timeout_seconds`, `fluff_probability`, `max_stem_hops`.

`[peer_rate_limiting]`: `default_burst`, `default_rate`.

`[network_timing]`: `target_outbound_peers`, `peer_connection_delay_seconds`, `addr_relay_min_interval_seconds`, `max_addresses_per_addr_message`, `max_addresses_from_dns`.

`[request_timeouts]`: `async_request_timeout_seconds`, `utxo_commitment_request_timeout_seconds`, `request_cleanup_interval_seconds`, `pending_request_max_age_seconds`, `storage_timeout_seconds`, `network_timeout_seconds`, `rpc_timeout_seconds`, `handshake_timeout_secs`, `connect_timeout_secs`, `checkpoint_request_timeout_secs`, `protocol_verify_timeout_secs`, `headers_verify_timeout_secs`.

`[protocol_limits]`: `max_protocol_message_length`, `max_addr_to_send`, `max_inv_sz`, `max_headers_results`.

`[background_tasks]`: `dos_cleanup_interval_secs`, `ban_cleanup_interval_secs`, `ban_cleanup_outer_interval_secs`, `chain_sync_check_interval_secs`, `chain_sync_timeout_secs`, `peer_eviction_interval_secs`, `ping_timeout_check_interval_secs`, `ping_interval_secs`, `peer_reconnection_interval_secs`, `ping_timeout_secs`, `peer_reconnection_stale_secs`.

`[replay_protection]`: `cleanup_interval_secs`, `message_id_expiration_secs`, `request_id_expiration_secs`, `future_tolerance_secs`.

`[ibd_protection]`: per-peer, per-IP, and per-subnet bandwidth caps, `max_concurrent_ibd_serving`, `ibd_request_cooldown_seconds`, `suspicious_reconnection_threshold`, `reputation_ban_threshold`, `reputation_penalty_per_request`, `enable_emergency_throttle`, `emergency_throttle_percent`.

## RPC, ban list, governance, modules

`[rpc]`: `max_request_size_bytes`, `rate_limit_when_auth_disabled`, `ip_rate_limit_burst`, `ip_rate_limit_rate`, `max_connections_per_ip_per_minute`, `batch_rate_multiplier_cap`, `connection_rate_limit_window_seconds`.

`[rpc_auth]`: `required`, `tokens`, `token_file`, `admin_tokens`, `certificates`, `username`, `password`, `rate_limit_burst`, `rate_limit_rate`, and the same IP rate-limit fields as `[rpc]`.

`[rest_api]`: `enabled`, `listen_addr`, `payment_endpoints_enabled`.

`[ban_list_sharing]`: `enabled` (default true), `share_mode` (`immediate`, `periodic`, `disabled`; default `periodic`), `periodic_interval_seconds` (default 300), `min_ban_duration_to_share` (default 3600).

`[governance]`, when the feature is compiled in: `enabled`, `commons_url`, `api_key`. An empty `api_key` uses `COMMONS_API_KEY`.

`[modules]`: `enabled`, `modules_dir`, `data_dir`, `socket_dir`, `enabled_modules`, `disabled_modules`, `registry_url`, `module_database_backend`, per-module tables, `watch_enabled`, `watch_auto_load`, `watch_auto_unload`, `marketplace_fetch_enabled`.

`[module_resource_limits]`: `default_max_cpu_percent`, `default_max_memory_bytes`, `default_max_file_descriptors`, `default_max_child_processes`, `module_startup_wait_millis`, `module_socket_timeout_seconds`, `module_socket_check_interval_millis`, `module_socket_max_attempts`.

Each module has its own file at `{modules.data_dir}/{manifest name}/config.toml`. `[modules.<manifest name>]` overrides only the fields that module marks for the environment overlay. The manifest name is the table key. `[modules.blvm-stratum-v2]` is the miner TCP overlay. `[modules.stratum-v2]` is not.
