# Mining Integration

The reference node includes mining coordination functionality as part of the Bitcoin protocol. The system provides block template generation, mining coordination, and optional Stratum V2 protocol support.

## Block Template Generation

Block templates are created using a formally verified algorithm from `blvm-consensus` that ensures correctness per Orange Paper Section 12.4.

### Algorithm Overview

1. **Get Chain State**: Retrieve current chain tip, height, and difficulty
2. **Get Mempool Transactions**: Fetch transactions from mempool
3. **Get UTXO Set**: Load UTXO set for fee calculation
4. **Select Transactions**: Choose transactions based on fee priority
5. **Create Coinbase**: Generate coinbase transaction with subsidy + fees
6. **Calculate Merkle Root**: Compute merkle root from transaction list
7. **Build Template**: Construct block header with all components

**Code**: [mining.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/mining.rs#L183-L228)

### Transaction Selection

Transactions are selected using a fee-based priority algorithm:

1. **Prioritize by Fee Rate**: Transactions sorted by fee rate (satoshis per byte)
2. **Size Limits**: Respect maximum block size (1MB) and weight (4M weight units)
3. **Minimum Fee**: Filter transactions below minimum fee rate (1 sat/vB default)
4. **UTXO Validation**: Verify all transaction inputs exist in UTXO set

**Code**: [miner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/miner.rs#L69-L105)

### Fee Calculation

Transaction fees are calculated using the UTXO set:

```rust
fee = sum(input_values) - sum(output_values)
fee_rate = fee / transaction_size
```

The coinbase transaction includes:
- **Block Subsidy**: Calculated based on halving schedule
- **Transaction Fees**: Sum of all fees from selected transactions

**Code**: [miner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/miner.rs#L107-L200)

### Block Template Structure

```rust
pub struct Block {
    header: BlockHeader {
        version: 1,
        prev_block_hash: [u8; 32],
        merkle_root: [u8; 32],
        timestamp: u32,
        bits: u32,
        nonce: 0,  // To be filled by miner
    },
    transactions: Vec<Transaction>,  // Coinbase first
}
```

**Code**: [miner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/miner.rs#L594-L604)

## Mining Process

### Template Generation

The `getblocktemplate` RPC method generates a block template:

1. Uses formally verified `create_block_template` from `blvm-consensus`
2. Converts to JSON-RPC format (BIP 22/23)
3. Returns template ready for mining

**Code**: [mining.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/mining.rs#L183-L228)

### Proof of Work

Mining involves finding a nonce that satisfies the difficulty target:

1. **Nonce Search**: Iterate through nonce values (0 to 2^32-1)
2. **Hash Calculation**: Compute SHA256(SHA256(block_header))
3. **Target Check**: Verify hash < difficulty target
4. **Success**: Return mined block with valid nonce

**Code**: [miner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/miner.rs#L240-L272)

### Block Submission

Mined blocks are submitted via `submitblock` RPC method:

1. **Validation**: Block validated against consensus rules
2. **Connection**: Block connected to chain
3. **Confirmation**: Block added to blockchain

**Code**: [mining.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/mining.rs#L1-L100)

## Mining Coordinator

The `MiningCoordinator` manages mining operations:

- **Template Generation**: Creates block templates from mempool
- **Mining Loop**: Continuously generates and mines blocks
- **Stratum V2 Integration**: Coordinates with Stratum V2 protocol
- **Merge Mining**: Available via optional `blvm-merge-mining` module (paid plugin)

**Code**: [miner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/miner.rs#L1-L615)

## Stratum V2 Support

Optional Stratum V2 protocol support provides:

- **Binary Protocol**: 50-66% bandwidth savings vs Stratum V1
- **Encrypted Communication**: TLS/QUIC encryption
- **Multiplexed Channels**: QUIC stream multiplexing
- **Merge Mining**: Simultaneous mining of multiple chains

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2/mod.rs#L1-L200)

## Configuration

### Mining Configuration

```toml
[mining]
enabled = false
mining_threads = 1
```

### Stratum V2 Configuration

```toml
[stratum_v2]
enabled = true
listen_addr = "0.0.0.0:3333"
```

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs#L1-L100)

## See Also

- [Node Operations](operations.md) - Node operation and management
- [RPC API Reference](rpc-api.md) - Mining-related RPC methods (`getblocktemplate`, `submitblock`)
- [Stratum V2 + Merge Mining](mining-stratum-v2.md) - Stratum V2 protocol details
- [Node Configuration](configuration.md) - Mining configuration options
- [Protocol Specifications](../reference/protocol-specifications.md) - Stratum V2 and mining protocols

