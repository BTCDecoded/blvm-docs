# RPC Methods

<!-- Auto-generated from source code -->
<!-- Regenerate: cd bllvm-docs && python3 tools/extract-rpc-methods.py -->

Complete list of available JSON-RPC 2.0 methods in `bllvm-node`.

For detailed method documentation, see [RPC Reference](../bllvm-node/docs/RPC_REFERENCE.md).

## Blockchain (12 methods)

| Method |
|--------|
| `getblock` |
| `getblockchaininfo` |
| `getblockcount` |
| `getblockhash` |
| `getblockheader` |
| `getblocktemplate` |
| `getdifficulty` |
| `gettxout` |
| `gettxoutproof` |
| `gettxoutsetinfo` |
| `verifychain` |
| `verifytxoutproof` |

## Mempool & Transactions (6 methods)

| Method |
|--------|
| `decoderawtransaction` |
| `getmempoolinfo` |
| `getrawmempool` |
| `getrawtransaction` |
| `sendrawtransaction` |
| `testmempoolaccept` |

## Network (10 methods)

| Method |
|--------|
| `addnode` |
| `clearbanned` |
| `disconnectnode` |
| `getconnectioncount` |
| `getnettotals` |
| `getnetworkinfo` |
| `getpeerinfo` |
| `listbanned` |
| `ping` |
| `setban` |

## Mining (3 methods)

| Method |
|--------|
| `estimatesmartfee` |
| `getmininginfo` |
| `submitblock` |

## Control (6 methods)

| Method |
|--------|
| `getmemoryinfo` |
| `getrpcinfo` |
| `help` |
| `logging` |
| `stop` |
| `uptime` |

## Other (2 methods)

| Method |
|--------|
| `getbestblockhash` |
| `savemempool` |

**Total: 39 methods**

[Source: bllvm-node/src/rpc/control.rs](../../bllvm-node/src/rpc/control.rs)

[Full RPC Reference](../bllvm-node/docs/RPC_REFERENCE.md)
