# UTXO Commitments

## Overview

UTXO Commitments enable fast synchronization of the Bitcoin UTXO set without requiring full blockchain download. The system uses cryptographic Merkle tree commitments with peer consensus verification, achieving 98% bandwidth savings compared to traditional full block download.

## Architecture

### Core Components

1. **Merkle Tree**: Sparse Merkle Tree for incremental UTXO set updates
2. **Peer Consensus**: N-of-M diverse peer verification model
3. **Spam Filtering**: Filters spam transactions from commitments
4. **Verification**: PoW-based commitment verification
5. **Network Integration**: Works with TCP and Iroh transports

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/mod.rs#L1-L48)

## Merkle Tree Implementation

### Sparse Merkle Tree

The system uses a sparse Merkle tree for efficient incremental updates:

- **Incremental Updates**: Insert/remove UTXOs without full tree rebuild
- **Proof Generation**: Generate Merkle proofs for UTXO inclusion
- **Root Calculation**: Efficient root hash calculation
- **SHA256 Hashing**: Uses SHA256 for all hashing operations

**Code**: [merkle_tree.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/merkle_tree.rs#L1-L603)

### Usage

```rust
use blvm_consensus::utxo_commitments::{UtxoCommitmentSet, UtxoCommitment};

// Create UTXO commitment set
let mut commitment_set = UtxoCommitmentSet::new();

// Add UTXO
let outpoint = OutPoint { hash: [1; 32], index: 0 };
let utxo = UTXO { value: 1000, script_pubkey: vec![], height: 0 };
commitment_set.insert(outpoint, utxo)?;

// Generate commitment
let commitment = commitment_set.generate_commitment(block_hash, height)?;
```

## Peer Consensus Protocol

### N-of-M Verification Model

The peer consensus protocol discovers diverse peers and finds consensus among them to verify UTXO commitments without trusting any single peer.

### Peer Diversity

Peers are selected for diversity across:
- **ASN (Autonomous System Number)**: Maximum 2 peers per ASN
- **Country**: Geographic distribution
- **Subnet**: /16 subnet distribution
- **Implementation**: Different Bitcoin implementations (Bitcoin Core, btcd, etc.)

**Code**: [peer_consensus.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/peer_consensus.rs#L20-L45)

### Consensus Configuration

```rust
pub struct ConsensusConfig {
    pub min_peers: usize,              // Minimum: 5
    pub target_peers: usize,           // Target: 10
    pub consensus_threshold: f64,      // 0.8 (80% agreement)
    pub max_peers_per_asn: usize,      // 2
    pub safety_margin: Natural,        // 2016 blocks (~2 weeks)
}
```

**Code**: [peer_consensus.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/peer_consensus.rs#L66-L91)

### Consensus Process

1. **Discover Diverse Peers**: Find peers across different ASNs, countries, subnets
2. **Request Commitments**: Query each peer for UTXO commitment at checkpoint height
3. **Group Responses**: Group commitments by value (merkle root + supply + count + height)
4. **Find Consensus**: Identify group with highest agreement
5. **Verify Threshold**: Check if agreement meets consensus threshold (80%)
6. **Verify Commitment**: Verify consensus commitment against block headers and PoW

**Code**: [peer_consensus.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/peer_consensus.rs#L241-L350)

## Fast Sync Protocol

### Initial Sync Process

1. **Download Headers**: Download block headers from genesis to tip
2. **Select Checkpoint**: Choose checkpoint height (safety margin back from tip)
3. **Request UTXO Sets**: Query diverse peers for UTXO commitment at checkpoint
4. **Find Consensus**: Use peer consensus to verify commitment
5. **Verify Commitment**: Verify against block headers and PoW
6. **Sync Forward**: Download filtered blocks from checkpoint to tip
7. **Update Incrementally**: Update UTXO set incrementally for each block

**Code**: [initial_sync.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/initial_sync.rs#L1-L132)

### Bandwidth Savings

The fast sync protocol achieves 98% bandwidth savings by:
- **Headers Only**: Download headers instead of full blocks (~80 bytes vs ~1 MB per block)
- **Filtered Blocks**: Download only relevant transactions (~2% of block size)
- **Incremental Updates**: Only download UTXO changes, not full set

**Calculation**:
- Traditional: ~500 GB (full blockchain)
- Fast Sync: ~10 GB (headers + filtered blocks)
- **Savings**: 98%

## Spam Filtering Integration

UTXO Commitments use spam filtering to reduce bandwidth during sync. Spam filtering is a general-purpose feature that can be used independently of UTXO commitments.

**For detailed spam filtering documentation, see**: [Spam Filtering](spam-filtering.md)

### Integration with UTXO Commitments

When processing blocks for UTXO commitments, spam filtering is applied:

- **Location**: [initial_sync.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/initial_sync.rs#L206-L310)
- **Process**: All transactions are processed, but spam outputs are filtered out
- **Benefit**: 40-60% bandwidth reduction during ongoing sync
- **Critical Design**: INPUTS are always removed (maintains UTXO consistency), OUTPUTS are filtered (bandwidth savings)

### Bandwidth Savings

- **40-60% bandwidth reduction** during ongoing sync
- Maintains consensus correctness
- Enables efficient UTXO commitment synchronization

## BIP158 Compact Block Filters

The node implements BIP158 compact block filters for light client support. While this is implemented at the node level, it integrates with UTXO commitments for efficient filtered block serving.

### Location
- **Node Implementation**: `blvm-node/src/bip158.rs`
- **Service**: `blvm-node/src/network/filter_service.rs`
- **Integration**: Used for light client support

### Capabilities

#### Filter Generation
- **Golomb-Rice Coded Sets (GCS)** for efficient encoding
- **False Positive Rate**: ~1 in 524,288 (P=19)
- **Filter Contents**:
  1. All spendable output scriptPubKeys in the block
  2. All scriptPubKeys from outputs spent by block's inputs

#### Filter Header Chain
- Maintains filter header chain for efficient verification
- Checkpoints every 1000 blocks (per BIP157)
- Enables light clients to verify filter integrity

### Algorithm

1. **Collect Scripts**: All output scriptPubKeys from block transactions and all scriptPubKeys from UTXOs being spent
2. **Hash to Range**: Hash each script with SHA256, map to range [0, N*M) where N = number of elements, M = 2^19
3. **Golomb-Rice Encoding**: Sort hashed values, compute differences, encode using Golomb-Rice
4. **Filter Matching**: Light clients hash their scripts and check if script hash is in set

### Integration with UTXO Commitments

BIP158 filters can be included in `FilteredBlockMessage` alongside spam-filtered transactions and UTXO commitments, enabling efficient light client synchronization.

**Code**: [bip158.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/bip158.rs#L1-L200)

## Verification

### Verification Levels

1. **Minimal**: Peer consensus only
2. **Standard**: Peer consensus + PoW + supply checks
3. **Paranoid**: All checks + background genesis verification

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/config.rs#L26-L35)

### Verification Checks

- **PoW Verification**: Verify block headers have valid proof-of-work
- **Supply Verification**: Verify total supply matches expected value
- **Header Chain Verification**: Verify commitment height matches header chain
- **Merkle Root Verification**: Verify Merkle root matches UTXO set

**Code**: [verification.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/verification.rs#L1-L200)

## Network Integration

### Transport Support

UTXO Commitments work with both TCP and Iroh transports via the transport abstraction layer:

- **TCP**: Bitcoin P2P compatible
- **Iroh/QUIC**: QUIC with NAT traversal and DERP

**Code**: [utxo_commitments_client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/utxo_commitments_client.rs#L1-L520)

### Network Messages

- `GetUTXOSet`: Request UTXO commitment from peer
- `UTXOSet`: Response with UTXO commitment
- `GetFilteredBlock`: Request filtered block (spam-filtered)
- `FilteredBlock`: Response with filtered block

**Code**: [network_integration.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/network_integration.rs#L1-L200)

## Configuration

### Sync Modes

- **PeerConsensus**: Use peer consensus for initial sync (fast, trusts N of M peers)
- **Genesis**: Sync from genesis (slow, but no trust required)
- **Hybrid**: Use peer consensus but verify from genesis in background

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/config.rs#L15-L24)

### Configuration Example

```toml
[utxo_commitments]
sync_mode = "PeerConsensus"  # or "Genesis" or "Hybrid"
verification_level = "Standard"  # or "Minimal" or "Paranoid"

[utxo_commitments.consensus]
min_peers = 5
target_peers = 10
consensus_threshold = 0.8
max_peers_per_asn = 2
safety_margin = 2016

[utxo_commitments.spam_filter]
min_value = 546  # dust threshold
min_fee_rate = 1  # sat/vB
```

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/config.rs#L1-L100)

## Formal Verification

The UTXO Commitments module includes blvm-spec-lock proofs verifying:

- Merkle tree operations (insert, remove, root calculation)
- Commitment generation
- Verification logic
- Peer consensus calculations

**Location**: `blvm-consensus/src/utxo_commitments/`

## Usage

### Initial Sync

```rust
use blvm_consensus::utxo_commitments::InitialSync;

let sync = InitialSync::new(
    peer_consensus,
    network_client,
    config,
);

// Sync from checkpoint
let commitment = sync.sync_from_checkpoint(
    header_chain,
    diverse_peers,
).await?;

// Complete sync forward with full validation
// Note: checkpoint_utxo_set should be obtained from the verified commitment
// For now, passing None starts with empty set (commitment verified at checkpoint)
sync.complete_sync_from_checkpoint(
    &mut utxo_tree,
    checkpoint_height,
    current_tip,
    network_client,
    get_block_hash_fn,
    peer_id,
    Network::Mainnet,
    network_time,
    Some(&header_chain),
    None, // checkpoint_utxo_set - can be obtained separately if needed
).await?;
```

### Update After Block

```rust
use blvm_consensus::utxo_commitments::update_commitments_after_block;

update_commitments_after_block(
    &mut utxo_tree,
    block,
    height,
)?;
```

**Code**: [initial_sync.rs](https://github.com/BTCDecoded/blvm-consensus/blob/main/src/utxo_commitments/initial_sync.rs#L1-L200)

## Benefits

1. **Fast Sync**: 98% bandwidth savings vs full blockchain download
2. **Security**: N-of-M peer consensus prevents single peer attacks
3. **Efficiency**: Incremental updates, no full set download
4. **Flexibility**: Multiple sync modes and verification levels
5. **Transport Agnostic**: Works with TCP or QUIC
6. **Formal Verification**: blvm-spec-lock proofs ensure correctness

## Components

The UTXO Commitments system includes:
- Sparse Merkle Tree with incremental updates
- Peer consensus protocol (N-of-M verification)
- Spam filtering
- Commitment verification
- Network integration (TCP and Iroh)
- Fast sync protocol
- blvm-spec-lock proofs

**Location**: `blvm-consensus/src/utxo_commitments/`, `blvm-node/src/network/utxo_commitments_client.rs`

## See Also

- [Consensus Overview](overview.md) - Consensus layer introduction
- [Consensus Architecture](architecture.md) - Consensus layer design
- [Network Protocol](../protocol/network-protocol.md) - Network protocol details
- [Node Configuration](../node/configuration.md) - UTXO commitment configuration
- [Storage Backends](../node/storage-backends.md) - Storage backend details
