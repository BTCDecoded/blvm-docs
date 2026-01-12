# Installation

This guide covers installing BLVM from pre-built binaries available on GitHub releases.

## Prerequisites

Pre-built binaries are available for Linux, macOS, and Windows on common platforms. No Rust installation required - binaries are pre-compiled and ready to use.

## Installing blvm-node

The reference node is the main entry point for running a BLVM node.

### Quick Start

1. **Download the latest release** from [GitHub Releases](https://github.com/BTCDecoded/blvm/releases)

2. **Extract the archive** for your platform:
   ```bash
   # Linux
   tar -xzf blvm-*-linux-x86_64.tar.gz
   
   # macOS
   tar -xzf blvm-*-macos-x86_64.tar.gz
   
   # Windows
   # Extract the .zip file using your preferred tool
   ```

3. **Move the binary to your PATH** (optional but recommended):
   ```bash
   # Linux/macOS
   sudo mv blvm /usr/local/bin/
   
   # Or add to your local bin directory
   mkdir -p ~/.local/bin
   mv blvm ~/.local/bin/
   export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.bashrc or ~/.zshrc
   ```

4. **Verify installation**:
   ```bash
   blvm --version
   ```

### Release Variants

Releases include two variants:

#### Base Variant (`blvm-{version}-{platform}.tar.gz`)

Stable, minimal release with core Bitcoin node functionality, production optimizations, standard [storage backends](../node/storage-backends.md), and process sandboxing. Use for production deployments prioritizing stability.

#### Experimental Variant (`blvm-experimental-{version}-{platform}.tar.gz`)

Full-featured build with experimental features: [UTXO commitments](../consensus/utxo-commitments.md), BIP119 CTV, [Dandelion++](../node/privacy-relay.md), BIP158, [Stratum V2](../node/mining-stratum-v2.md), and enhanced signature operations counting. See [Protocol Specifications](../reference/protocol-specifications.md#experimental-features) for details.

Use for development, testing, or when experimental capabilities are required.

## Installing blvm-sdk Tools

The SDK tools (`blvm-keygen`, `blvm-sign`, `blvm-verify`) are included in the blvm-node release archives.

After extracting the release archive, you'll find:
- `blvm` - Bitcoin reference node
- `blvm-keygen` - Generate governance keypairs
- `blvm-sign` - Sign governance messages
- `blvm-verify` - Verify signatures and multisig thresholds

All tools are in the same directory. Move them to your PATH as described above.

## Platform-Specific Notes

### Linux

- **x86_64**: Standard 64-bit Linux
- **ARM64**: For ARM-based systems (Raspberry Pi, AWS Graviton, etc.)
- **glibc 2.31+**: Required for Linux binaries

### macOS

- **x86_64**: Intel Macs
- **ARM64**: Apple Silicon (M1/M2/M3)
- **macOS 11.0+**: Required for macOS binaries

### Windows

- **x86_64**: 64-bit Windows
- Extract the `.zip` file and run `blvm.exe` from the extracted directory
- Add the directory to your PATH for command-line access

## Verifying Installation

After installation, verify everything works:

```bash
# Check blvm-node version
blvm --version

# Check SDK tools
blvm-keygen --help
blvm-sign --help
blvm-verify --help
```

## Building from Source (Advanced)

Building from source requires Rust 1.70+ and is primarily for development. Clone the [blvm repository](https://github.com/BTCDecoded/blvm) and follow the build instructions in its README.

## Next Steps

- See [Quick Start](quick-start.md) for running your first node
- See [Node Configuration](../node/configuration.md) for detailed setup options

## See Also

- [Quick Start](quick-start.md) - Run your first node
- [First Node Setup](first-node.md) - Complete setup guide
- [Node Configuration](../node/configuration.md) - Configuration options
- [Node Overview](../node/overview.md) - Node features and capabilities
- [Release Process](../development/release-process.md) - How releases are created
- [GitHub Releases](https://github.com/BTCDecoded/blvm/releases) - Download releases

