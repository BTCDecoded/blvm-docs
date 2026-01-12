# Protocol Specifications

Bitcoin Improvement Proposals (BIPs) implemented in BLVM. Consensus-critical BIPs are [formally verified](../consensus/formal-verification.md). See [Formal Verification](../consensus/formal-verification.md) for verification details.

## Consensus-Critical BIPs

**Script Opcodes**:
- **BIP65** (CLTV, opcode 0xb1): Locktime validation (`blvm-consensus/src/script.rs`) ✅ Kani proofs
- **BIP112** (CSV, opcode 0xb2): Relative locktime via sequence numbers (`blvm-consensus/src/script.rs`) ✅ Kani proofs
- **BIP68**: Relative locktime sequence encoding (used by BIP112)

**Time Validation**:
- **BIP113**: Median time-past for CLTV timestamp validation (`blvm-consensus/src/block.rs`) ✅ Kani proofs

**Transaction Features**:
- **BIP125** (RBF): Replace-by-fee with all 5 requirements (`blvm-consensus/src/mempool.rs`) ✅ Tests
- **BIP141/143** (SegWit): Witness validation, weight calculation, P2WPKH/P2WSH (`blvm-consensus/src/segwit.rs`) ✅ Kani proofs
- **BIP340/341/342** (Taproot): P2TR validation framework (`blvm-consensus/src/taproot.rs`) ✅ Kani proofs

## Network Protocol BIPs

- **BIP152**: Compact block relay - short transaction IDs, block reconstruction (see [Compact Blocks](../node/transport-abstraction.md#compact-blocks))
- **BIP157/158**: Client-side block filtering - GCS filter construction, integrated with network layer, works over all transports (see [BIP157/158](../node/transport-abstraction.md#bip157-158))
- **BIP331**: Package relay - efficient transaction relay (see [Package Relay](../node/package-relay.md))

## Application-Level BIPs

- **BIP21**: Bitcoin URI scheme (`blvm-node/src/bip21.rs`)
- **BIP32/39/44**: HD wallets, mnemonic phrases, standard derivation paths (`blvm-node/src/wallet/`)
- **BIP70**: Payment protocol ⚠️ **Deprecated** (legacy compatibility only, `blvm-node/src/bip70.rs`)
- **BIP174**: PSBT format for hardware wallet support (`blvm-node/src/psbt.rs`)
- **BIP350/351**: Bech32m for Taproot (P2TR), Bech32 for SegWit (`blvm-node/src/bech32m.rs`)

## Experimental Features

Available in [experimental build variant](../getting-started/installation.md#experimental-variant): [UTXO commitments](../consensus/utxo-commitments.md), BIP119 CTV (CheckTemplateVerify), [Dandelion++ privacy relay](../node/privacy-relay.md), [Stratum V2 mining protocol](../node/mining-stratum-v2.md).

