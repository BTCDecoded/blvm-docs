# Miniscript module (`blvm-miniscript`)

Descriptor and PSBT helpers for **`blvm-node`**. Overrides two core JSON-RPC methods via the module RPC extender when loaded.

## Overview

**blvm-miniscript** registers handlers for:

| RPC method | Purpose |
|------------|---------|
| `getdescriptorinfo` | Descriptor metadata (checksum, canonical form, witness/version hints) |
| `analyzepsbt` | PSBT analysis (inputs, outputs, fee, feasibility) |

Without the module loaded, core stubs return JSON-RPC **-32001** with a message to `loadmodule "blvm-miniscript"`. See [JSON-RPC error reference](../reference/rpc-errors.md#module-not-loaded).

**Repository:** [BTCDecoded/blvm-miniscript](https://github.com/BTCDecoded/blvm-miniscript)

## Requirements

- `blvm-node` with the module system enabled.
- Module pinned in **`registry/modules.json`** or installed on the module search path.
- Manifest declares **`rpc_overrides`** for `getdescriptorinfo` and `analyzepsbt` (validated against `OVERRIDABLE_CORE_RPC_METHODS` at load time).

## Loading

Pin in `blvm.toml` (merge into your full file — include `transport_preference` and network keys):

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-miniscript = "0.1.*"
```

Runtime load (admin RPC):

```bash
curl -s -X POST http://127.0.0.1:18332 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin-token>" \
  -d '{"jsonrpc":"2.0","method":"loadmodule","params":["blvm-miniscript"],"id":1}'
```

Or use **`blvm load blvm-miniscript`** / **`blvm module load blvm-miniscript`** when the node is running (admin RPC auth required).

## Configuration

Optional module config: `<modules.data_dir>/blvm-miniscript/config.toml`

```toml
log_level = "info"   # trace | debug | info | warn | error
```

Node spawn overrides: `[modules.blvm-miniscript]` in `blvm.toml` (same keys; table name must match manifest **`name`**).

## See also

- [RPC API — Available Methods](../node/rpc-api.md#raw-transaction-methods) (`getdescriptorinfo`, `analyzepsbt`)
- [Module catalog](overview.md)
- [Installing modules](overview.md#installing-modules)
