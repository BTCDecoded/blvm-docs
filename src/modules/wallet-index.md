# Wallet index (`blvm-wallet-index`)

Script history for outputs created on chain, and for spends of those outputs. The module process owns the database. It does not open the node chain store, and it does not hold keys.

## What it stores

On `NewBlock` the module calls `get_block` and writes one row per transaction output: txid, vout, value, `script_pubkey`, and height. If an input spends an output already in this database, it also records that spending transaction against the spent script. On `BlockDisconnected` it deletes every row at that height and above. `ChainReorg` is subscribed and does not delete rows. Disconnect events do.

The script key is SHA256(`scriptPubKey`), byte-reversed. That is the scripthash an Electrum client sends.

## Node RPC

`getscripthistory` takes one argument, the script in hex, and returns the outputs that created that script, oldest height first. `txid` is reversed hex, the same display order as other node hash fields. `getaddressinfo` stays on the node.

## Electrum

The module binds a TCP port only when `listen` is set in its `config.toml`:

```toml
listen = "127.0.0.1:50001"
```

Each line is one JSON-RPC object, or a batch array. The methods are `server.version`, `server.ping`, `server.banner`, `blockchain.scripthash.get_history`, `blockchain.scripthash.subscribe`, `blockchain.headers.subscribe`, and `blockchain.scripthash.get_mempool`. `get_history` returns `{tx_hash, height}` for the transaction that created the script and the transaction that spent it. A disconnect of the spend’s height removes that spend from the next reply. Subscribe returns null when there are no rows, and otherwise the SHA256 hex of `tx_hash:height:` in that same order. When a later block or disconnect changes that script, the server pushes a `blockchain.scripthash.subscribe` notification with the new status.

`blockchain.headers.subscribe` returns null until a block has been indexed, and otherwise `{hex, height}` for the highest stored header. `hex` is the 80-byte header. A later block or disconnect pushes `blockchain.headers.subscribe` with the new tip, or null when no header remains.

`blockchain.scripthash.get_mempool` lists unconfirmed transactions that create or spend that script. Each row is `{tx_hash, height: 0, fee}`. `fee` is input value minus output value when every input is a known UTXO, and `0` when one is not. A mempool removal drops the row. Indexing the same transaction in a block moves it to `get_history`. Subscribe status appends those unconfirmed rows after the confirmed ones, with height `0`. A disconnect does not put the block’s transactions back into this mempool list. The node’s Core RPC port is a different protocol.

## Esplora

Set `esplora` in the same `config.toml` to bind an HTTP port, for example `127.0.0.1:3000`. `GET /blocks/tip/height` returns the highest stored header. `GET /address/<address>` returns confirmed output counts and satoshi totals for that script. `spent_txo_sum` is present when nothing is spent or when every output is spent, and null when only some outputs are spent. `mempool_stats` reports the unconfirmed transaction count only. Transaction hex and `/address/<address>/txs` are not served. `signet_invalidate_disconnects_the_index` disconnects a signet tip through the node and clears this database at that height, including the Esplora tip.

## Loading

Run the `blvm-wallet-index` binary as a node module (`loadmodule`, or a `[modules]` pin once the binary is published). The module manifest asks for `read_blockchain`, `read_utxo`, `read_chain_state`, `subscribe_events`, `read_storage`, `write_storage`, and `register_rpc_endpoint`.
