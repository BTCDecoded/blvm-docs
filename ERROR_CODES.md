# Error Codes

<!-- Auto-generated from source code -->
<!-- Regenerate: cd bllvm-docs && python3 tools/extract-errors.py -->

Error codes used across BLLVM components.

## RPC Error Codes

JSON-RPC 2.0 compatible error codes used by `bllvm-node`.

| Code | Variant | Message | Description |
|------|---------|---------|-------------|
| -32700 | `ParseError` | "Parse error" | Invalid JSON was received |
| -32600 | `InvalidRequest` | "Invalid Request" | The JSON sent is not a valid Request object |
| -32601 | `MethodNotFound` | "Method not found" | The method does not exist |
| -32602 | `InvalidParams` | "Invalid params" | Invalid method parameter(s) |
| -32603 | `InternalError` | "Internal error" | Internal JSON-RPC error |
| -1 | `TxAlreadyInChain` | "Transaction already in block chain" | Transaction is already in the blockchain |
| -25 | `TxRejected` | "Transaction rejected" | Transaction was rejected |
| -1 | `TxMissingInputs` | "Missing inputs" | Transaction references non-existent inputs |
| -27 | `TxAlreadyInMempool` | "Transaction already in mempool" | Transaction is already in the mempool |
| -5 | `BlockNotFound` | "Block not found" | Block hash not found |
| -5 | `TxNotFound` | "Transaction not found" | Transaction hash not found |
| -5 | `UtxoNotFound` | "No such UTXO" | UTXO not found |

[Source: bllvm-node/src/rpc/errors.rs](../../bllvm-node/src/rpc/errors.rs)
