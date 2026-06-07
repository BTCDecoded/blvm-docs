# Migration Guides

## Bitcoin Core datadir

Import a synced Core datadir into BLVM’s native store at `<datadir>/blvm/` (requires `rocksdb`, Core stopped, matching `--network`).

**Procedure:** [Starting from a Bitcoin Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir)

## BLVM version upgrades

Check [GitHub Releases](https://github.com/BTCDecoded/blvm/releases) for breaking config, storage, or RPC changes before upgrading.
