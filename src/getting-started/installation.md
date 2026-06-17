<!-- Generated from src/install/install-content.json. Do not edit by hand. Run: node scripts/fetch-blvm-release.mjs && node scripts/render-installation.mjs -->

# Installation

Pre-built binaries and Linux packages from GitHub Releases. Each release ships `checksums.sha256` — verify before running.

**Current release:** [v0.1.39 on GitHub →](https://github.com/BTCDecoded/blvm/releases/tag/v0.1.39)  
**All builds:** [GitHub Releases (latest)](https://github.com/BTCDecoded/blvm/releases/latest)

Download checksums.sha256 from the release page and verify each artifact before running.

## Pre-built packages

### Linux package managers

#### Debian / Ubuntu (`.deb`)

Ubuntu 22.04+, Debian 11+, and any dpkg-based distro.

**Download:** [`blvm_0.1.39_amd64.deb`](https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/blvm_0.1.39_amd64.deb) · [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest)

**Install:**

```bash
sudo dpkg -i blvm_0.1.39_amd64.deb
sudo apt-get install -f    # pull in any missing deps
```

**Verify:**

```bash
# Run in the folder where you saved blvm_0.1.39_amd64.deb
curl -LO https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/checksums.sha256
grep 'blvm_0.1.39_amd64.deb' checksums.sha256 | sha256sum --check
```

#### Fedora / RHEL (`.rpm`)

Fedora 38+, RHEL 9, CentOS Stream 9, and RPM-based distros.

**Download:** [`blvm-0.1.39-1.x86_64.rpm`](https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/blvm-0.1.39-1.x86_64.rpm) · [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest)

**Install:**

```bash
sudo rpm -i blvm-0.1.39-1.x86_64.rpm
# or via dnf:
sudo dnf install ./blvm-0.1.39-1.x86_64.rpm
```

**Verify:**

```bash
# Run in the folder where you saved blvm-0.1.39-1.x86_64.rpm
curl -LO https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/checksums.sha256
grep 'blvm-0.1.39-1.x86_64.rpm' checksums.sha256 | sha256sum --check
```

#### Arch Linux (`.pkg.tar.gz`)

Arch and other pacman-based distros (x86_64).

**Download:** [`blvm-0.1.39-x86_64.pkg.tar.gz`](https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/blvm-0.1.39-x86_64.pkg.tar.gz) · [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest)

**Install:**

```bash
sudo pacman -U blvm-0.1.39-x86_64.pkg.tar.gz
```

**Verify:**

```bash
# Run in the folder where you saved blvm-0.1.39-x86_64.pkg.tar.gz
curl -LO https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/checksums.sha256
grep 'blvm-0.1.39-x86_64.pkg.tar.gz' checksums.sha256 | sha256sum --check
```

### Standalone binaries

#### Linux x86_64 (`binary`)

Single static binary for 64-bit Linux (glibc). Base release build (`production` features); not the full local `cargo build` default set.

**Download:** [`blvm-0.1.39-linux-x86_64`](https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/blvm-0.1.39-linux-x86_64) · [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest)

**Install:**

```bash
chmod +x blvm-0.1.39-linux-x86_64
sudo mv blvm-0.1.39-linux-x86_64 /usr/local/bin/blvm
```

**Verify:**

```bash
# Run in the folder where you saved blvm-0.1.39-linux-x86_64
curl -LO https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/checksums.sha256
grep 'blvm-0.1.39-linux-x86_64' checksums.sha256 | sha256sum --check
```

#### ARM64 Linux (`binary`)

64-bit ARM Linux binary (Raspberry Pi 4/5 with 64-bit OS, Apple Silicon Linux VMs, etc.).

**Download:** [`blvm-0.1.39-linux-aarch64`](https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/blvm-0.1.39-linux-aarch64) · [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest)

**Install:**

```bash
chmod +x blvm-0.1.39-linux-aarch64
sudo mv blvm-0.1.39-linux-aarch64 /usr/local/bin/blvm
```

**Verify:**

```bash
# Run in the folder where you saved blvm-0.1.39-linux-aarch64
curl -LO https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/checksums.sha256
grep 'blvm-0.1.39-linux-aarch64' checksums.sha256 | sha256sum --check
```

#### Windows (`.exe`)

Portable Windows 10 / 11 build (64-bit). Download, verify against `checksums.sha256`, then run the `.exe` from PowerShell.

**Download:** [`blvm-0.1.39-windows-x86_64.exe`](https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/blvm-0.1.39-windows-x86_64.exe) · [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest)

**Run:**

```bash
# PowerShell — after download + verify
.\blvm-0.1.39-windows-x86_64.exe --help
```

**Verify:**

```powershell
# PowerShell — same folder as blvm-0.1.39-windows-x86_64.exe
Invoke-WebRequest -Uri 'https://github.com/BTCDecoded/blvm/releases/download/v0.1.39/checksums.sha256' -OutFile checksums.sha256
$expected = ((Get-Content checksums.sha256 | Select-String -SimpleMatch 'blvm-0.1.39-windows-x86_64.exe').Line -split '\s+')[0]
$actual = (Get-FileHash blvm-0.1.39-windows-x86_64.exe -Algorithm SHA256).Hash
if ($expected.ToUpper() -eq $actual) { 'Checksum OK' } else { throw 'Checksum MISMATCH' }
```

## Docker

Official image on GHCR, published on every stable release.

**Pull:**

```bash
docker pull ghcr.io/btcdecoded/blvm:0.1.39
```

**Run:**

```bash
docker run -d --name blvm \
  -v blvm-data:/data \
  -p 8333:8333 -p 8332:8332 \
  ghcr.io/btcdecoded/blvm:0.1.39
```

[View on GHCR →](https://github.com/BTCDecoded/blvm/pkgs/container/blvm)

## Managed installs (Not ready yet)

> Umbrel App Store — coming soon. Use the packages above, Docker on GHCR, or build from source until managed marketplace listings ship.

## Experimental build variant {#experimental-variant}

Stable GitHub Releases ship the **base** binary only (`production` Cargo features — see [Release process — Build variants](../development/release-process.md#build-variants)). Extra compile-time features — UTXO commitments, Dandelion++ privacy relay, BIP119 CTV, Stratum V2 integration, sigop counting, Iroh transport, and related flags — require a **source build** with the experimental feature set or explicit `--features`.


## Build from source

For other architectures, experimental features, or development, see [build instructions](https://github.com/BTCDecoded/blvm) and [Release process](../development/release-process.md).

## Who is this for?

- **Operators:** [Quick Start](../getting-started/quick-start.md) → [Mainnet initial sync](../getting-started/mainnet-sync.md) or [First Node (regtest)](../getting-started/first-node.md)
- **Module developers:** [Building your first module](../getting-started/first-module.md)
- **Researchers:** [Introduction](../introduction.md#who-is-this-for)

## Next steps

- [Quick Start](../getting-started/quick-start.md)
- [Deployment posture](../security/deployment-posture.md) (before mainnet RPC)
- [Node configuration](../node/configuration.md)

## See also

- [GitHub Releases](https://github.com/BTCDecoded/blvm/releases/latest)
