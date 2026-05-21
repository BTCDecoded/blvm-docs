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

Uses bundled `blvm-mainnet-ibd.toml.example`, mainnet, and `~/.local/share/blvm-mainnet`. No `BLVM_IBD_*` env vars. LAN Core is auto-discovered; WAN-only uses one fastest peer (`parallel` mode).

**Manual:** `blvm --config blvm-mainnet-ibd.toml.example --network mainnet --data-dir ~/.local/share/blvm-mainnet --verbose`

**Monitor:** same flags as start — `blvm --network mainnet --config blvm-mainnet-ibd.toml.example sync`. During sync, `IBD: <height> / <tip>` in logs is authoritative.

**Resume:** same `--data-dir` every run; do not delete `rocksdb/`.

## Expectations

- **Disk / RAM:** ~15 GB+ pruned; 4 GB+ RAM typical
- **Time:** hours (WAN-only); much faster with LAN Core
- **Startup delay:** 15–60s peer discovery before `IBD:` lines
- **Slowdown ~900k+:** assume-valid phase ended — normal full validation

## Optional overrides

- `BLVM_IBD_PEERS=<ip>:8333` — pin download peer
- `BLVM_IBD_MODE=sequential|earliest` — change mode (default `parallel`)
- Port **8333** in use — stop Core or change `listen_addr`

## Troubleshooting

[Mainnet IBD](../appendices/troubleshooting.md#mainnet-ibd)
