# Mainnet initial sync

For **release tarball** users. Do not use bare `blvm --network mainnet` for first sync — use the example config or script (pruning, IBD tuning, modules off during sync).

Details also in the [blvm README](https://github.com/BTCDecoded/blvm#first-mainnet-sync-release-binary).

## Start

```bash
tar xzf blvm-vX.Y.Z-linux-x86_64.tar.gz
cd blvm-vX.Y.Z-linux-x86_64
sha256sum -c SHA256SUMS-blvm-linux-x86_64

./scripts/start-ibd-mainnet.sh
# BLVM_BACKGROUND=1 ./scripts/start-ibd-mainnet.sh   # background → ~/.local/share/blvm-mainnet/ibd.log
```

Expected in the first minute:

- Config loads without TOML errors
- `Network: Mainnet` (or equivalent) in logs
- After peer discovery (often 15–60s): `IBD: <height> / <tip>` lines as sync progresses

Uses bundled `blvm-mainnet-ibd.toml.example`, mainnet, and `~/.local/share/blvm-mainnet`. The bundled script does not set `BLVM_IBD_*` env vars. LAN Core is auto-discovered; on WAN-only networks, **`parallel` mode uses multi-peer work-stealing by default** — set **`BLVM_IBD_WAN_SINGLE_PEER=1`** to force a single download peer.

Optional: enable the age-tiered UTXO engine with **`BLVM_IBD_ENGINE=1`** before start (see [IBD UTXO engine](../node/ibd-engine.md)); the example TOML leaves it off.

**Manual:** `blvm --config blvm-mainnet-ibd.toml.example --network mainnet --data-dir ~/.local/share/blvm-mainnet --verbose`

**Monitor:** `blvm --network mainnet --config blvm-mainnet-ibd.toml.example --data-dir ~/.local/share/blvm-mainnet sync` (same `--network`, `--config`, and `--data-dir` as start). During sync, `IBD: <height> / <tip>` in logs is authoritative.

**Resume:** same `--data-dir` every run; do not delete the active backend directory (`heed3/`, `rocksdb/`, …).

## Expectations

- **Disk / RAM:** ~15 GB+ pruned; 4 GB+ RAM typical
- **Time:** hours (WAN-only); much faster with LAN Core
- **Startup delay:** 15–60s peer discovery before `IBD:` lines
- **Slowdown ~900k+:** assume-valid phase ended — normal full validation

## Optional overrides

- `BLVM_IBD_PEERS=<ip>:8333` — pin download peer
- `BLVM_IBD_MODE=sequential|earliest|parallel` — change mode (default `parallel`)
- `BLVM_IBD_WAN_SINGLE_PEER=1` — WAN-only: use one peer instead of multi-peer work-stealing
- `BLVM_IBD_ENGINE=1` — age-tiered UTXO engine during sync ([IBD UTXO engine](../node/ibd-engine.md))
- Port **8333** in use — stop Core or change `listen_addr`

## Troubleshooting

[Mainnet IBD](../appendices/troubleshooting.md#mainnet-ibd)
