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

**Code**: ```1:48:bllvm-consensus/src/utxo_commitments/mod.rs```

## Merkle Tree Implementation

### Sparse Merkle Tree

The system uses a sparse Merkle tree for efficient incremental updates:

- **Incremental Updates**: Insert/remove UTXOs without full tree rebuild
- **Proof Generation**: Generate Merkle proofs for UTXO inclusion
- **Root Calculation**: Efficient root hash calculation
- **SHA256 Hashing**: Uses SHA256 for all hashing operations

**Code**: ```1:603:bllvm-consensus/src/utxo_commitments/merkle_tree.rs```

### Usage

```rust
use bllvm_consensus::utxo_commitments::{UtxoCommitmentSet, UtxoCommitment};

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

**Code**: ```20:45:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

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

**Code**: ```66:91:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

### Consensus Process

1. **Discover Diverse Peers**: Find peers across different ASNs, countries, subnets
2. **Request Commitments**: Query each peer for UTXO commitment at checkpoint height
3. **Group Responses**: Group commitments by value (merkle root + supply + count + height)
4. **Find Consensus**: Identify group with highest agreement
5. **Verify Threshold**: Check if agreement meets consensus threshold (80%)
6. **Verify Commitment**: Verify consensus commitment against block headers and PoW

**Code**: ```241:350:bllvm-consensus/src/utxo_commitments/peer_consensus.rs```

## Fast Sync Protocol

### Initial Sync Process

1. **Download Headers**: Download block headers from genesis to tip
2. **Select Checkpoint**: Choose checkpoint height (safety margin back from tip)
3. **Request UTXO Sets**: Query diverse peers for UTXO commitment at checkpoint
4. **Find Consensus**: Use peer consensus to verify commitment
5. **Verify Commitment**: Verify against block headers and PoW
6. **Sync Forward**: Download filtered blocks from checkpoint to tip
7. **Update Incrementally**: Update UTXO set incrementally for each block

**Code**: ```1:132:bllvm-consensus/src/utxo_commitments/initial_sync.rs```

### Bandwidth Savings

The fast sync protocol achieves 98% bandwidth savings by:
- **Headers Only**: Download headers instead of full blocks (~80 bytes vs ~1 MB per block)
- **Filtered Blocks**: Download only relevant transactions (~2% of block size)
- **Incremental Updates**: Only download UTXO changes, not full set

**Calculation**:
- Traditional: ~500 GB (full blockchain)
- Fast Sync: ~10 GB (headers + filtered blocks)
- **Savings**: 98%

## Spam Filtering

The system filters spam transactions from commitments:

- **Value Threshold**: Minimum transaction value
- **Fee Rate Filtering**: Minimum fee rate requirements
- **UTXO Count Limits**: Maximum UTXO count per transaction
- **Summary Statistics**: Tracks spam metrics

**Code**: ```1:200:bllvm-consensus/src/utxo_commitments/spam_filter.rs```

## Verification

### Verification Levels

1. **Minimal**: Peer consensus only
2. **Standard**: Peer consensus + PoW + supply checks
3. **Paranoid**: All checks + background genesis verification

**Code**: ```26:35:bllvm-consensus/src/utxo_commitments/config.rs```

### Verification Checks

- **PoW Verification**: Verify block headers have valid proof-of-work
- **Supply Verification**: Verify total supply matches expected value
- **Header Chain Verification**: Verify commitment height matches header chain
- **Merkle Root Verification**: Verify Merkle root matches UTXO set

**Code**: ```1:200:bllvm-consensus/src/utxo_commitments/verification.rs```

## Network Integration

### Transport Support

UTXO Commitments work with both TCP and Iroh transports via the transport abstraction layer:

- **TCP**: Bitcoin P2P compatible
- **Iroh/QUIC**: QUIC with NAT traversal and DERP

**Code**: ```1:520:bllvm-node/src/network/utxo_commitments_client.rs```

### Network Messages

- `GetUTXOSet`: Request UTXO commitment from peer
- `UTXOSet`: Response with UTXO commitment
- `GetFilteredBlock`: Request filtered block (spam-filtered)
- `FilteredBlock`: Response with filtered block

**Code**: ```1:200:bllvm-consensus/src/utxo_commitments/network_integration.rs```

## Configuration

### Sync Modes

- **PeerConsensus**: Use peer consensus for initial sync (fast, trusts N of M peers)
- **Genesis**: Sync from genesis (slow, but no trust required)
- **Hybrid**: Use peer consensus but verify from genesis in background

**Code**: ```15:24:bllvm-consensus/src/utxo_commitments/config.rs```

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

**Code**: ```1:100:bllvm-consensus/src/utxo_commitments/config.rs```

## Formal Verification

The UTXO Commitments module includes 11 Kani proofs verifying:

- Merkle tree operations (insert, remove, root calculation)
- Commitment generation
- Verification logic
- Peer consensus calculations

**Location**: `bllvm-consensus/src/utxo_commitments/`

## Usage

### Initial Sync

```rust
use bllvm_consensus::utxo_commitments::InitialSync;

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

// Complete sync forward
sync.complete_sync_from_checkpoint(
    &mut utxo_tree,
    header_chain,
    network_client,
).await?;
```

### Update After Block

```rust
use bllvm_consensus::utxo_commitments::update_commitments_after_block;

update_commitments_after_block(
    &mut utxo_tree,
    block,
    height,
)?;
```

**Code**: ```1:200:bllvm-consensus/src/utxo_commitments/initial_sync.rs```

## Benefits

1. **Fast Sync**: 98% bandwidth savings vs full blockchain download
2. **Security**: N-of-M peer consensus prevents single peer attacks
3. **Efficiency**: Incremental updates, no full set download
4. **Flexibility**: Multiple sync modes and verification levels
5. **Transport Agnostic**: Works with TCP or QUIC
6. **Formal Verification**: 11 Kani proofs ensure correctness

## Components

The UTXO Commitments system includes:
- Sparse Merkle Tree with incremental updates
- Peer consensus protocol (N-of-M verification)
- Spam filtering
- Commitment verification
- Network integration (TCP and Iroh)
- Fast sync protocol
- 11 Kani proofs

**Location**: `bllvm-consensus/src/utxo_commitments/`, `bllvm-node/src/network/utxo_commitments_client.rs`

