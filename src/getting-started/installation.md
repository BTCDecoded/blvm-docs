# Installation

Pre-built **`blvm`** binaries, Linux packages, Windows builds, and Docker images are published on GitHub Releases. The book does not pin release numbers — use the install page for the current tag, filenames, and checksum commands.

**Install (downloads + verify):** [btcdecoded.org/install](https://btcdecoded.org/install)

Always verify `checksums.sha256` (or the release checksum file) before running a downloaded artifact.

## Platform / feature notes

Release artifacts are **platform-specific** (see [Release process — Build variants](../development/release-process.md#build-variants)):

- **Linux x86_64** — full `blvm` default feature set (`rest-api`, `bip70-http`, `compression`, `governance`, `iroh`, `dandelion`, `utxo-commitments`, …)
- **Linux aarch64 / Windows x86_64** — portable CI builds (`--no-default-features` subset: typically `sled`, `redb`, `production`, `protocol-verification`, `utxo-commitments`; **no** `bip70-http` / `rest-api` / `compression`)
- **Docker (GHCR)** — tagged per release on [`ghcr.io/btcdecoded/blvm`](https://github.com/BTCDecoded/blvm/pkgs/container/blvm)

Local `cargo build` in the `blvm` repo uses default features unless you pass `--no-default-features` or explicit `--features`.

## Experimental build variant {#experimental-variant}

Stable GitHub Releases ship the **base** binary set per tag (platform-specific features — see [Release process — Build variants](../development/release-process.md#build-variants)). Extra compile-time features — BIP119 CTV, Stratum V2 node demux, sigop counting, Quinn transport, and flags not in your platform artifact — require a **source build** with explicit `--features`.


## Build from source

For other architectures, experimental compile-time features, or development: [blvm on GitHub](https://github.com/BTCDecoded/blvm) and [Release process](../development/release-process.md).

## Managed installs (not ready yet)

> Umbrel App Store — coming soon. Use [btcdecoded.org/install](https://btcdecoded.org/install), Docker on GHCR, or build from source until managed marketplace listings ship.

## Who is this for?

- **Operators:** [Quick Start](../getting-started/quick-start.md) (regtest) → [First Node Setup](../getting-started/first-node.md) → [Mainnet initial sync](../getting-started/mainnet-sync.md)
- **Module developers:** [Building your first module](../getting-started/first-module.md)
- **Researchers:** [Introduction](../introduction.md#who-is-this-for)

## Next steps

- [Quick Start](../getting-started/quick-start.md)
- [Deployment posture](../security/deployment-posture.md) (before mainnet RPC)
- [Node configuration](../node/configuration.md)

## See also

- [Install page](https://btcdecoded.org/install) — current release downloads
- [GitHub Releases (latest)](https://github.com/BTCDecoded/blvm/releases/latest)
