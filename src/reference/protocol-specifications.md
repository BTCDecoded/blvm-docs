# Protocol Specifications

Bitcoin Improvement Proposals (BIPs) implemented in BLLVM.

## Consensus-Critical BIPs

### BIP65 - OP_CHECKLOCKTIMEVERIFY (CLTV)
- **Status**: ✅ Implemented
- **Location**: `bllvm-consensus/src/script.rs` (opcode 0xb1)
- **Features**: Validates transaction locktime >= stack value, locktime type matching
- **Verification**: Kani proofs + integration tests

### BIP112 - OP_CHECKSEQUENCEVERIFY (CSV)
- **Status**: ✅ Implemented
- **Location**: `bllvm-consensus/src/script.rs` (opcode 0xb2)
- **Features**: Validates relative locktime using sequence numbers (BIP68)
- **Verification**: Kani proofs + integration tests

### BIP68 - Relative Lock-Time
- **Status**: ✅ Implemented
- **Location**: `bllvm-consensus/src/script.rs` (used by BIP112)
- **Features**: Sequence number encoding/decoding for relative locktime

### BIP113 - Median Time-Past
- **Status**: ✅ Implemented
- **Location**: `bllvm-consensus/src/block.rs`
- **Features**: Median time-past calculation for CLTV timestamp validation
- **Verification**: Kani proofs + integration tests

### BIP125 - Replace-by-Fee (RBF)
- **Status**: ✅ Fully Compliant
- **Location**: `bllvm-consensus/src/mempool.rs`
- **Features**: Complete BIP125 implementation with all 5 requirements
- **Verification**: Comprehensive test coverage

### BIP141/143 - Segregated Witness (SegWit)
- **Status**: ✅ Complete
- **Location**: `bllvm-consensus/src/segwit.rs`
- **Features**: Witness validation, weight calculation, P2WPKH/P2WSH support
- **Verification**: Kani proofs + integration tests

### BIP340/341/342 - Taproot
- **Status**: ✅ Complete
- **Location**: `bllvm-consensus/src/taproot.rs`
- **Features**: P2TR validation framework
- **Verification**: Kani proofs + integration tests

## Network Protocol BIPs

### BIP152 - Compact Block Relay
- **Status**: ✅ Complete
- **Location**: `bllvm-node/src/network/compact_blocks.rs`
- **Features**: Short transaction IDs, block reconstruction, Iroh integration

### BIP157/158 - Client-Side Block Filtering
- **Status**: ✅ Fully Integrated
- **Location**: `bllvm-node/src/bip157.rs`, `bllvm-node/src/bip158.rs`
- **Features**: Compact block filter construction (GCS), network protocol integration
- **Integration**: Fully integrated with network layer, works over all transports

### BIP331 - Package Relay
- **Status**: ✅ Implemented
- **Location**: `bllvm-node/src/network/package_relay.rs`
- **Features**: Package transaction relay for improved efficiency

## Application-Level BIPs

### BIP21 - Bitcoin URI Scheme
- **Status**: ✅ Implemented
- **Location**: `bllvm-node/src/bip21.rs`
- **Features**: Bitcoin payment URI parsing and generation

### BIP32/39/44 - HD Wallets
- **Status**: ✅ Implemented
- **Location**: `bllvm-node/src/wallet/`
- **Features**: Hierarchical deterministic wallets, mnemonic phrases, standard derivation paths

### BIP70 - Payment Protocol
- **Status**: ⚠️ Implemented (Deprecated)
- **Location**: `bllvm-node/src/bip70.rs`
- **Note**: BIP70 deprecated by Bitcoin Core. Implementation provided for legacy compatibility only.

### BIP174 - Partially Signed Bitcoin Transactions (PSBT)
- **Status**: ✅ Implemented
- **Location**: `bllvm-node/src/psbt.rs`
- **Features**: PSBT format for hardware wallet support

### BIP350/351 - Bech32m Address Format
- **Status**: ✅ Implemented
- **Location**: `bllvm-node/src/bech32m.rs`
- **Features**: Bech32m encoding for Taproot addresses (P2TR), Bech32 for SegWit addresses

## Experimental Features

The following BIPs are available in the experimental build variant:

- **UTXO Commitments**: Experimental UTXO commitment system
- **BIP119 CTV**: CheckTemplateVerify (proposed soft fork) support
- **Dandelion++**: Privacy-preserving transaction relay
- **Stratum V2**: Modern mining protocol

See [Installation](../getting-started/installation.md) for details on experimental builds.

