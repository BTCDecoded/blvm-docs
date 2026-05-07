<!-- Generated from src/install/install-content.json. Do not edit by hand. Run: node scripts/render-installation.mjs -->

# Installation

Pre-built packages for Linux and Windows. Each release ships with a SHA-256 checksum and a detached GPG signature. Verify before running.

**Current release:** [v0.1.0 on GitHub →](https://github.com/BTCDecoded/blvm-node/releases/tag/v0.1.0)  
**All builds:** [GitHub Releases (latest)](https://github.com/BTCDecoded/blvm-node/releases/latest)

Each artifact ships with a `.sha256` file and a detached GPG signature (`.sig`). See the [signature verification guide](https://docs.thebitcoincommons.org/nodes/verification.html).

## Pre-built packages

### Debian / Ubuntu (`.deb`)

Ubuntu 22.04+, Debian 11+, and any dpkg-based distro.

**Download:** get `blvm_0.1.0_amd64.deb` from [GitHub Releases](https://github.com/BTCDecoded/blvm-node/releases/latest).

**Install:**

```bash
sudo dpkg -i blvm_0.1.0_amd64.deb
sudo apt-get install -f    # pull in any missing deps
```

**Verify checksum:**

```bash
sha256sum --check blvm_0.1.0_amd64.deb.sha256
```

Detached signature: `blvm_0.1.0_amd64.deb.sig`.

### Fedora / RHEL (`.rpm`)

Fedora 38+, RHEL 9, CentOS Stream 9, and RPM-based distros.

**Download:** get `blvm-0.1.0-1.x86_64.rpm` from [GitHub Releases](https://github.com/BTCDecoded/blvm-node/releases/latest).

**Install:**

```bash
sudo rpm -i blvm-0.1.0-1.x86_64.rpm
# or via dnf:
sudo dnf install ./blvm-0.1.0-1.x86_64.rpm
```

**Verify checksum:**

```bash
sha256sum --check blvm-0.1.0-1.x86_64.rpm.sha256
```

Detached signature: `blvm-0.1.0-1.x86_64.rpm.sig`.

### Windows (`.exe`)

Windows 10 / 11 (64-bit). Signed installer: blvm registers as a background service via the Windows Service Manager.

**Download:** get `blvm-setup-0.1.0.exe` from [GitHub Releases](https://github.com/BTCDecoded/blvm-node/releases/latest).

**Install:**

```bash
# Run the installer, accept the UAC prompt, choose your data directory.
# blvm registers itself as a Windows service and starts automatically on boot.
```

**Verify checksum:**

```bash
# PowerShell checksum verify:
(Get-FileHash blvm-setup-0.1.0.exe -Algorithm SHA256).Hash
```

Detached signature: `blvm-setup-0.1.0.exe.sig`.

## Managed installs (Not ready yet)

> These paths are not live yet. Use the packages above or build from source until Umbrel listing and Docker image publish.

Prefer a one-click install? blvm is planned as a managed package on Umbrel and as an official Docker image.

### Umbrel

Available in the Umbrel App Store as "Bitcoin Commons". Runs on a Raspberry Pi or any Linux machine with a one-click node stack.

1. Open your Umbrel dashboard and go to the App Store.
1. Search for "Bitcoin Commons" and click Install.
1. Wait for initial sync to complete; this may take several hours on first run.
1. Access node settings and RPC credentials from the app detail page.

- [Full documentation](https://docs.thebitcoincommons.org/nodes/umbrel.html)
- [Umbrel support](https://community.getumbrel.com)

### Docker

Run blvm in a container on any platform that supports Docker or Podman. The official image is planned for Docker Hub as btccommons/blvm.

1. Pull the image: docker pull btccommons/blvm:0.1.0
1. Create a persistent data volume: docker volume create blvm-data
1. Run the node: docker run -d --name blvm -v blvm-data:/data -p 8333:8333 -p 8332:8332 btccommons/blvm:0.1.0
1. Check logs: docker logs -f blvm

- [Full documentation](https://docs.thebitcoincommons.org/nodes/docker.html)
- [Docker Hub →](https://hub.docker.com/r/btccommons/blvm)

## Build from source

For other architectures or development, see [build instructions](https://docs.thebitcoincommons.org/nodes/build.html).

## Next steps

- [Quick Start](../getting-started/quick-start.md) for running your first node
- [Node configuration](../node/configuration.md) for detailed setup

## See also

- [GitHub Releases](https://github.com/BTCDecoded/blvm-node/releases/latest) for downloads
