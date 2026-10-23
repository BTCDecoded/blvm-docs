# Deployment posture

How to expose a BLVM node without handing out the RPC credential. Day-to-day commands are in the [Operator guide](../getting-started/operator-guide.md).

## RPC stays on loopback

Default RPC binds are loopback: mainnet `127.0.0.1:8332`, testnet `127.0.0.1:18332`, signet `127.0.0.1:38332`, testnet4 `127.0.0.1:48332`, regtest `127.0.0.1:18443`. Leave `--rpc-addr` unset unless a local client on another interface must reach the port.

HTTP Basic, including the cookie, is cleartext. A non-loopback bind means anyone who can open the port can try that password. Prefer a Bearer token over a tunnel, or terminate TLS in a proxy you run. The transport matrix is [RPC transport × authentication](rpc-transport-auth-matrix.md).

## Cookie file

`{data_dir}/.cookie` is the admin Basic password when `[rpc_auth].password` is unset. The file mode is `0600`. Do not copy the data directory into a backup that other users can read, and do not serve that directory over the network. Shutdown removes the file this process created. A crash leaves it until the next start overwrites it.

Setting `[rpc_auth].username` and `[rpc_auth].password` skips the cookie. Treat that password like the cookie: it is admin, and it is not a Bearer token.

## Bearer tokens

`[rpc_auth].tokens` and `RPC_AUTH_TOKENS` are read-only. Put a token in `admin_tokens` as well before using it for `getblocktemplate`, `submitblock`, or `stop`. Do not commit the token. A `token_file` should be mode `0600`, same as the cookie.

Omitting `required` in the table deserializes as false. Startup still forces authentication on when it writes the cookie, including a node with no `[rpc_auth]` table. After that, a loopback client with no header is rejected. A configured `password` does not force `required`. Set `required = true` in that table if every caller must authenticate.

## What is still absent

There is no Electrum or Esplora listener in the node process. Point wallets that speak Bitcoin Core RPC at this port. Script history is `blvm-wallet-index`, a separate process. Its Electrum port binds only when that module’s `listen` address is set. It answers `blockchain.scripthash.get_history`, `blockchain.headers.subscribe`, and `blockchain.scripthash.get_mempool`. Its Esplora port binds only when `esplora` is set, and that port serves tip height and address stats. It does not serve transaction hex.
