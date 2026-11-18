# Peer Consensus Protocol

> **Layer**: N-of-M peer verification for [UTXO commitments](utxo-commitments.md) (**blvm-protocol** / **blvm-node**). Distinct from Bitcoin *consensus* (block/script rules in **blvm-consensus**).

## Overview

Bitcoin Commons implements an N-of-M peer consensus protocol for UTXO set verification. The protocol discovers diverse peers and finds consensus among them to verify UTXO commitments without trusting any single peer.

## Architecture

### N-of-M Consensus Model

The protocol uses an N-of-M consensus model:

- **N**: Minimum number of peers required
- **M**: Target number of diverse peers
- **Threshold**: `consensus_threshold` defaults to 0.8
- **Diversity**: Peers must be diverse across ASNs, subnets, geographic regions


### Peer Information

`PeerInfo` in `blvm-protocol/src/utxo_commitments/peer_consensus.rs` records the address, ASN, country, implementation, and /16 subnet.


## Diverse Peer Discovery

### Diversity Requirements

Peers must be diverse across:

- **ASNs**: Maximum N peers per ASN
- **Subnets**: No peers from same /16 subnet
- **Geographic Regions**: Geographic diversity
- **Bitcoin Implementations**: Implementation diversity


### Discovery Process

1. **Collect All Peers**: Gather all available peers
2. **Filter by ASN**: Limit peers per ASN
3. **Filter by Subnet**: Remove duplicate subnets
4. **Select Diverse Set**: Select diverse peer set
5. **Stop at Target**: Stop when target number reached


## Consensus Finding

### Commitment Grouping

Commitments are grouped by their values:

- **Merkle Root**: UTXO commitment Merkle root
- **Total Supply**: Total Bitcoin supply
- **UTXO Count**: Number of UTXOs
- **Block Height**: Block height of commitment


### Consensus Threshold

Consensus threshold check:

- **Threshold**: `consensus_threshold` defaults to 0.8
- **Agreement Count**: Number of peers agreeing
- **Required Count**: `ceil(total_peers * threshold)`
- **Verification**: Check if agreement count >= required count


### Mathematical Invariants

Consensus finding maintains invariants:

- `required_agreement_count <= total_peers`
- `required_agreement_count >= 1`
- `best_agreement_count <= total_peers`
- If `agreement_count >= required_agreement_count`, then `agreement_count/total_peers >= threshold`


## Checkpoint Height Determination

### Median-Based Checkpoint

Checkpoint height determined from peer chain tips:

- **Median Calculation**: Uses median of peer tips
- **Safety Margin**: Subtracts safety margin to prevent deep reorgs
- **Mathematical Invariants**:
 - Median is always between min(tips) and max(tips)
 - Checkpoint height is always >= 0
 - Checkpoint height <= median_tip


## Ban List Sharing

### Ban List Protocol

Nodes share ban lists to protect against malicious peers:

- **Ban List Messages**: `GetBanList`, `BanList` protocol messages
- **Hash Verification**: Ban list hash verification
- **Merging**: Ban list merging from multiple peers
- **Network-Wide Protection**: Protects entire network


### Ban List Validation

Ban list entries are validated:

- **Entry Validation**: Each entry validated
- **Hash Verification**: Ban list hash verified
- **Merging Logic**: Merged with local ban list
- **Duplicate Prevention**: Duplicate entries prevented


### Ban List Merging

Ban lists are merged from multiple peers:

- **Hash Verification**: Verify ban list hash
- **Entry Validation**: Validate each ban entry
- **Merging**: Merge with local ban list
- **Conflict Resolution**: Resolve conflicts (longest ban wins)


## Filtered Blocks

### Filtered Block Protocol

Nodes can request filtered blocks:

- **GetFilteredBlock**: Request filtered block
- **FilteredBlock**: Response with filtered block
- **Efficiency**: More efficient than full blocks
- **Privacy**: Better privacy for light clients


## Network-Wide Malicious Peer Protection

### Protection Mechanisms

Network-wide protection against malicious peers:

- **Ban List Sharing**: Share ban lists across network
- **Peer Reputation**: Track peer reputation
- **Auto-Ban**: Automatic banning of abusive peers
- **Eclipse Prevention**: Prevent eclipse attacks


## Configuration

### Consensus Configuration

`ConsensusConfig` in `blvm-protocol/src/utxo_commitments/peer_consensus.rs` defaults to 5 minimum peers, 10 target peers, a threshold of 0.8, 2 peers per ASN, and a safety margin of 2016 blocks.


## Source

- [peer_consensus.rs](https://github.com/BTCDecoded/blvm-protocol/blob/main/src/utxo_commitments/peer_consensus.rs)
- [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/mod.rs)
- [ban_list_merging.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/ban_list_merging.rs)
- [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/protocol.rs)
- [security policy](https://github.com/BTCDecoded/blvm-node/blob/main/SECURITY.md)
## See Also

- [Node overview](overview.md)
- [UTXO Commitments](utxo-commitments.md)
- [Network Protocol](../protocol/network-protocol.md)
