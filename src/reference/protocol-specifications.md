# Protocol Specifications

Bitcoin Improvement Proposals (BIPs) implemented in BLLVM. All consensus-critical BIPs are formally verified. See [Formal Verification](../consensus/formal-verification.md) for verification details.

## Consensus-Critical BIPs

**Script Opcodes**:
- **BIP65** (CLTV, opcode 0xb1): Locktime validation (`bllvm-consensus/src/script.rs`) ✅ Kani proofs
- **BIP112** (CSV, opcode 0xb2): Relative locktime via sequence numbers (`bllvm-consensus/src/script.rs`) ✅ Kani proofs
- **BIP68**: Relative locktime sequence encoding (used by BIP112)

**Time Validation**:
- **BIP113**: Median time-past for CLTV timestamp validation (`bllvm-consensus/src/block.rs`) ✅ Kani proofs

**Transaction Features**:
- **BIP125** (RBF): Replace-by-fee with all 5 requirements (`bllvm-consensus/src/mempool.rs`) ✅ Comprehensive tests
- **BIP141/143** (SegWit): Witness validation, weight calculation, P2WPKH/P2WSH (`bllvm-consensus/src/segwit.rs`) ✅ Kani proofs
- **BIP340/341/342** (Taproot): P2TR validation framework (`bllvm-consensus/src/taproot.rs`) ✅ Kani proofs

## Network Protocol BIPs

- **BIP152**: Compact block relay - short transaction IDs, block reconstruction (`bllvm-node/src/network/compact_blocks.rs`)
- **BIP157/158**: Client-side block filtering - GCS filter construction, fully integrated with network layer, works over all transports (`bllvm-node/src/bip157.rs`, `bip158.rs`)
- **BIP331**: Package relay - efficient transaction relay (`bllvm-node/src/network/package_relay.rs`)

## Application-Level BIPs

- **BIP21**: Bitcoin URI scheme (`bllvm-node/src/bip21.rs`)
- **BIP32/39/44**: HD wallets, mnemonic phrases, standard derivation paths (`bllvm-node/src/wallet/`)
- **BIP70**: Payment protocol ⚠️ **Deprecated** (legacy compatibility only, `bllvm-node/src/bip70.rs`)
- **BIP174**: PSBT format for hardware wallet support (`bllvm-node/src/psbt.rs`)
- **BIP350/351**: Bech32m for Taproot (P2TR), Bech32 for SegWit (`bllvm-node/src/bech32m.rs`)

## Experimental Features

Available in [experimental build variant](../getting-started/installation.md#experimental-variant): UTXO commitments, BIP119 CTV (CheckTemplateVerify), Dandelion++ privacy relay, Stratum V2 mining protocol.

