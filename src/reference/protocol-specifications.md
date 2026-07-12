# Protocol Specifications

Bitcoin Improvement Proposals (BIPs) implemented in BLVM. Consensus-critical behavior lives in **`blvm-consensus`** with tests, review, and **BLVM Specification Lock** proofs. See [Formal Verification](../consensus/formal-verification.md).

## Consensus-Critical BIPs

**Script Opcodes**:
- **BIP65** (CLTV, opcode 0xb1): Locktime validation (`blvm-consensus/src/script/`)
- **BIP112** (CSV, opcode 0xb2): Relative locktime via sequence numbers (`blvm-consensus/src/script/`)
- **BIP68**: Relative locktime sequence encoding (used by BIP112)

**Time Validation**:
- **BIP113**: Median time-past for CLTV timestamp validation (`blvm-consensus/src/block/mod.rs`)

**Transaction Features**:
- **BIP125** (RBF): Replace-by-fee with all 5 requirements (`blvm-consensus/src/mempool.rs`) with tests
- **BIP141/143** (SegWit): Witness validation, weight calculation, P2WPKH/P2WSH (`blvm-consensus/src/segwit.rs`)
- **BIP340/341/342** (Taproot): P2TR validation framework (`blvm-consensus/src/taproot.rs`)

## Network Protocol BIPs

- **BIP152**: Compact block relay - short transaction IDs, block reconstruction (see [Compact block relay (BIP152)](../protocol/overview.md#compact-blocks))
- **BIP157/158**: Client-side block filtering - GCS filter construction, integrated with network layer, works over all transports (see [BIP157/158](../protocol/overview.md#bip157-158))
- **BIP155** addrv2: Varint-length peer addresses (`addrv2`) on P2P wire ([serialization in **blvm-protocol `wire`**](https://github.com/BTCDecoded/blvm-protocol/blob/main/src/wire/mod.rs), `deserialize_addrv2` / `serialize_addrv2`; node handling in **`blvm-node`** [protocol_adapter.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/protocol_adapter.rs), [wire_dispatch.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/wire_dispatch.rs))
- **BIP331**: Package relay - efficient transaction relay (see [Package Relay](../node/package-relay.md))

## Application-Level BIPs

- **BIP21**: Bitcoin URI scheme (`blvm-node/src/bip21.rs`)
- **BIP32/39/44**: HD wallets, mnemonic phrases, standard derivation paths (`blvm-node/src/wallet/`)
- **BIP70**: Payment protocol (full reimplementation, `blvm-node/src/network/bip70_handler.rs`)
- **BIP174**: PSBT format for hardware wallet support (`blvm-node/src/psbt.rs`)
- **BIP350/351**: Bech32m for Taproot (P2TR), Bech32 for SegWit (`blvm-node/src/bech32m.rs`)

## Experimental Features

Available with compile-time features (platform-dependent: see [Release process: Build variants](../development/release-process.md#build-variants)): [UTXO commitments](../node/utxo-commitments.md) and [Dandelion++](../node/privacy-relay.md) in **`blvm` default features** (omitted from portable Windows/aarch64 release CI); BIP119 CTV, [Stratum V2 node demux](../node/mining-stratum-v2.md), sigop counting, and Quinn transport typically require explicit `--features`.

