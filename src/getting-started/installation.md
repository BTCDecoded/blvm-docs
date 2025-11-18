# Installation

This guide covers installing BLLVM from pre-built binaries available on GitHub releases.

## Prerequisites

Pre-built binaries are available for Linux, macOS, and Windows on common platforms. No Rust installation required - binaries are pre-compiled and ready to use.

## Installing bllvm-node

The reference node is the main entry point for running a BLLVM node.

### Quick Start

1. **Download the latest release** from [GitHub Releases](https://github.com/BTCDecoded/bllvm-node/releases)

2. **Extract the archive** for your platform:
   ```bash
   # Linux
   tar -xzf bllvm-*-linux-x86_64.tar.gz
   
   # macOS
   tar -xzf bllvm-*-macos-x86_64.tar.gz
   
   # Windows
   # Extract the .zip file using your preferred tool
   ```

3. **Move the binary to your PATH** (optional but recommended):
   ```bash
   # Linux/macOS
   sudo mv bllvm /usr/local/bin/
   
   # Or add to your local bin directory
   mkdir -p ~/.local/bin
   mv bllvm ~/.local/bin/
   export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.bashrc or ~/.zshrc
   ```

4. **Verify installation**:
   ```bash
   bllvm --version
   ```

### Release Variants

Releases include two variants:

#### Base Variant (`bllvm-{version}-{platform}.tar.gz`)

Stable, minimal release with core Bitcoin node functionality, production optimizations, standard storage backends, and process sandboxing. **Use this variant for**: Production deployments, stability priority.

#### Experimental Variant (`bllvm-experimental-{version}-{platform}.tar.gz`)

Full-featured build with experimental features enabled: UTXO commitments, BIP119 CTV, Dandelion++, BIP158, Stratum V2, and enhanced signature operations counting. See [Protocol Specifications](../reference/protocol-specifications.md#experimental-features) for details.

**Use this variant for**: Development, testing, advanced features, or if you need any experimental capabilities.

## Installing bllvm-sdk Tools

The SDK tools (`bllvm-keygen`, `bllvm-sign`, `bllvm-verify`) are included in the bllvm-node release archives.

After extracting the release archive, you'll find:
- `bllvm` - Bitcoin reference node
- `bllvm-keygen` - Generate governance keypairs
- `bllvm-sign` - Sign governance messages
- `bllvm-verify` - Verify signatures and multisig thresholds

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
- Extract the `.zip` file and run `bllvm.exe` from the extracted directory
- Add the directory to your PATH for command-line access

## Verifying Installation

After installation, verify everything works:

```bash
# Check bllvm-node version
bllvm --version

# Check SDK tools
bllvm-keygen --help
bllvm-sign --help
bllvm-verify --help
```

## Building from Source (Advanced)

Building from source requires Rust 1.70+ and is primarily for development. Clone the [bllvm-node repository](https://github.com/BTCDecoded/bllvm-node) and follow the build instructions in its README.

## Next Steps

- See [Quick Start](quick-start.md) for running your first node
- See [Node Configuration](../node/configuration.md) for detailed setup options

