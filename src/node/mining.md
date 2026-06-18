# Mining Integration

The reference node includes mining coordination functionality as part of the Bitcoin protocol. The system provides block template generation, mining coordination, and optional Stratum V2 protocol support.

## Mining RPC and admin auth

These JSON-RPC methods require **admin** credentials ([admin-only methods](../reference/rpc-errors.md#admin-only-methods)):

| Method | Use |
|--------|-----|
| `getblocktemplate` | Pool / solo template (ckpool, Stratum module via NodeAPI) |
| `submitblock` | Submit mined block |
| `generatetoaddress` | Regtest/test lab block generation |
| `prioritisetransaction` | Adjust effective mempool fee priority |
| `savemempool` | Persist mempool snapshot to disk |

Configure **`[rpc_auth].admin_tokens`**, list tokens in **`admin_tokens`**, or set HTTP Basic **`password`** (auto-admin). Non-admin callers get HTTP **403**. Regtest labs: see [Quick Start](../getting-started/quick-start.md) for Bearer + `generatetoaddress`.

## Block Template Generation

Block templates are built from **`blvm-consensus`** helpers (e.g. template construction) aligned with Orange Paper Section 12.4, with tests and spec-lock proofs on the relevant consensus paths.

### Algorithm Overview

1. **Get Chain State**: Retrieve current chain tip, height, and difficulty
2. **Get Mempool Transactions**: Fetch transactions from mempool
3. **Get UTXO Set**: Load UTXO set for fee calculation
4. **Select Transactions**: Choose transactions based on fee priority
5. **Create Coinbase**: Generate coinbase transaction with subsidy + fees
6. **Calculate Merkle Root**: Compute merkle root from transaction list
7. **Build Template**: Construct block header with all components


### Transaction Selection

Transactions are selected using a fee-based priority algorithm:

1. **Prioritize by Fee Rate**: Transactions sorted by fee rate (satoshis per byte)
2. **Size Limits**: Respect maximum block size (1MB) and weight (4M weight units)
3. **Minimum Fee**: Filter transactions below minimum fee rate (1 sat/vB default)
4. **UTXO Validation**: Verify all transaction inputs exist in UTXO set


### Fee Calculation

Transaction fees are calculated using the UTXO set:

```rust
fee = sum(input_values) - sum(output_values)
fee_rate = fee / transaction_size
```

The coinbase transaction includes:
- **Block Subsidy**: Calculated based on halving schedule
- **Transaction Fees**: Sum of all fees from selected transactions


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


## Mining Process

### Template Generation

The `getblocktemplate` RPC method generates a block template:

1. Uses `create_block_template` (or equivalent) from **`blvm-consensus`**, covered by tests and upstream verification policy
2. Converts to JSON-RPC format (BIP 22/23)
3. Returns template ready for mining


### Proof of Work

Mining involves finding a nonce that satisfies the difficulty target:

1. **Nonce Search**: Iterate through nonce values (0 to 2^32-1)
2. **Hash Calculation**: Compute SHA256(SHA256(block_header))
3. **Target Check**: Verify hash < difficulty target
4. **Success**: Return mined block with valid nonce


### Block Submission

Mined blocks are submitted via `submitblock` RPC method:

1. **Validation**: Block validated against consensus rules
2. **Connection**: Block connected to chain
3. **Confirmation**: Block added to blockchain


## Mining Coordinator

The `MiningCoordinator` manages mining operations:

- **Template Generation**: Creates block templates from mempool
- **Mining Loop**: Continuously generates and mines blocks
- **Stratum V2**: Pool/miner TCP and protocol server live in the **`blvm-stratum-v2`** module; the node exposes P2P demux and `NodeAPI` hooks
- **Merge Mining**: Available via optional `blvm-merge-mining` module (paid plugin)


## Stratum V2 Support

Optional Stratum V2 protocol support provides:

- **Binary Protocol**: 50-66% bandwidth savings vs Stratum V1
- **Encrypted Communication**: TLS/QUIC encryption
- **Multiplexed Channels**: QUIC stream multiplexing
- **Merge Mining**: Simultaneous mining of multiple chains


## Configuration

There is **no** `[mining]` table on `NodeConfig`. Mining uses RPC (`getblocktemplate`, `submitblock`), optional **`blvm-stratum-v2`** for Stratum traffic, and optional **`blvm-merge-mining`**.

### ckpool solo (Bitaxe / Stratum V1)

Stack: synced **`blvm`** node → **ckpool** (`-B` solo) → miners on `:3333`.

```toml
[rpc_auth]
required = true
username = "ckpool"
password = "change-me-to-a-strong-secret"
```

```bash
blvm --network mainnet --rpc-addr 127.0.0.1:8332
```

HTTP Basic password is auto-granted **admin** (required for `getblocktemplate` / `submitblock`). Point ckpool `btcd.url` at the RPC port with matching `auth` / `pass`. Regtest lab: seed chain height with `generatetoaddress` (**admin** Bearer or Basic — see [Quick Start](../getting-started/quick-start.md)) before GBT. Smoke test: `blvm-node/examples/ckpool-solo/smoke-rpc.sh`. See the [blvm-node Integration Guide — ckpool](https://github.com/BTCDecoded/blvm-node/blob/main/docs/INTEGRATION_GUIDE.md#ckpool-solo-mining--bitaxe--stratum-v1).

### Stratum V2 (node + module)

See [Stratum V2 + Merge Mining](mining-stratum-v2.md) for split **node** vs **module** `config.toml` examples and **`p2p_stratum_demux`**.


## Source

- [mining.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/rpc/mining.rs)
- [miner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/node/miner.rs)
- [blvm-stratum-v2](https://github.com/BTCDecoded/blvm-stratum-v2) (module — dedicated miner TCP); node: P2P demux in [network_manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_manager.rs), `NodeAPI::send_peer_transport_payload`
- [config/mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs), [StratumV2Config](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/rpc.rs)
## See Also

- [Node Operations](operations.md) - Node operation and management
- [RPC API Reference](rpc-api.md) - Mining RPC (`getblocktemplate`, `submitblock`, `generatetoaddress`) and admin auth
- [Stratum V2 + Merge Mining](mining-stratum-v2.md) - Stratum V2 protocol details
- [Node Configuration](configuration.md) - Mining configuration options
- [Protocol Specifications](../reference/protocol-specifications.md) - Stratum V2 and mining protocols
