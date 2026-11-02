# Node configuration guide

The `blvm` binary merges one file with a thin overlay.

**Precedence, highest first:** CLI, then environment, then the config file, then the built-in default. An omitted table stays at the built-in default. A present table fills every key from that table's defaults. Unknown keys are ignored.

Search order: `--config`, `./blvm.toml`, `~/.config/blvm/blvm.toml`, `/etc/blvm/blvm.toml`. TOML and JSON are both accepted.

`protocol_version` accepts `mainnet`, `testnet`, `testnet4`, `signet`, and `regtest`. `BitcoinV1` and `Testnet3` are aliases. The binary writes the five names above.

The field list is the [configuration reference](../reference/configuration-reference.md).

## Assume-valid

`[block_validation]` has `assume_valid_height` and `assume_valid_hash`. Signatures skip only when the connected block is below that height, chainwork is at least the minimum, and the hash is set. A height with no hash does not skip.

With no `[block_validation]` table, the binary seeds mainnet `912683` with the checked header hash, testnet `4550000`, and signet `267665`. Testnet and signet leave the hash unset, so script checks still run there. Testnet4 and regtest seed `0`.

`BLVM_ASSUME_VALID_HEIGHT` overrides the height only. There is no hash environment variable. `--assumevalid` with 64 hex digits sets the hash and keeps the seeded or file height. `--noassumevalid` and `--assumevalid 0` clear both. A 64-character block id is stored in the internal byte order `connect_block` compares.

## Logging

The subscriber uses `RUST_LOG`, then `BLVM_LOG_LEVEL`, then `[logging].filter` (alias `level`), then `--verbose` (`blvm=debug,blvm_node=debug`), then `blvm=info,blvm_node=info`.

`json_format` emits JSON only when the `json-logging` feature is compiled in. That feature is off the default build. Without it, the process keeps the text subscriber and warns once.

## Storage

RocksDB file settings follow environment, then file, then the built-in default. Heed3 map size follows a caller override, then the environment, then the file, then disk auto-tune.

## Mempool

`[mempool]` is the node pool. When `[mempool]` or `[rbf]` is present, those sizes are copied onto the consensus mempool global. Admission does not call the consensus mempool checker.

## Modules

Each module reads `{modules.data_dir}/{manifest name}/config.toml`. `[modules.<manifest name>]` overrides only fields that module marks for the environment overlay. The manifest name is the table key.

A `[payment]` table in the node file is ignored. `blvm-payment` reads its own module file.

`[stratum_v2]` only sets `p2p_stratum_demux` (default true). Miner TCP is `[modules.blvm-stratum-v2]`, not `[stratum_v2]` and not `[modules.stratum-v2]`. An omitted `max_connections` does not limit the accept loop.

## Binary environment variables

The variables the `blvm` binary reads are listed in the crate's `CONFIGURATION.md`. Node-library variables such as `BLVM_ASSUME_VALID_HEIGHT`, `BLVM_LOG_LEVEL`, and the RocksDB and Heed3 names are separate from that list. IBD bench latches stay environment variables. They are not keys in `[ibd]`.
