# First Node Setup

The operator binary is `blvm`. It does not hold keys. Wallet RPCs are absent. `getdescriptorinfo` and `analyzepsbt` are the miniscript override. Signing stays out.

`blvm-node` is pre-production for mainnet. A release checksum is a SHA256 file, not a signature.

## Default modules

A fresh install enables `blvm-miniscript`, `blvm-zmq`, and `blvm-index`, each at `0.1.*`. `blvm-payment` is not in that set. Payment, vault, pool, and congestion methods return method-not-found until that module is loaded.

`blvm-index` replaces `blvm-wallet-index`. The node binds Electrum and Esplora. An unset `[services]` `listen` does not open a port.

ZMQ's default binds are loopback:

| Topic | Bind |
|-------|------|
| `hashblock` | `tcp://127.0.0.1:28332` |
| `hashtx` | `tcp://127.0.0.1:28333` |
| `rawblock` | `tcp://127.0.0.1:28334` |
| `rawtx` | `tcp://127.0.0.1:28335` |
| `sequence` | `tcp://127.0.0.1:28336` |

The `sequence` body is 33 bytes: `0x01` for a mempool entry and `0x02` for a removal. It is not Bitcoin Core's `C`/`D`/`R`/`A` frame. The socket is not authenticated.

## Regtest

[Quick Start](quick-start.md) is the five-minute regtest path. Name the data directory and the RPC bind in that command.

With no RPC password, the process writes `{datadir}/.cookie` as `__cookie__:<hex>`, mode `0600`, and deletes that file on stop. A configured password leaves the directory untouched.

Regtest RPC listens on `127.0.0.1:18443`. Mainnet RPC is `8332`. Testnet RPC is `18332`.

## Startup checks

- The release default storage feature is heed3.
- A second process cannot open the same data directory. Startup rejects a store that fails the block check.
- Compact filters stay off unless configured.
- A named config file that is missing is refused.
- Stratum flags are refused when the binary was built without the stratum feature.
- `blvm-fibre` is not in the module registry until its `module.toml` has a `[downloads]` table.
- The release binary on `origin/main` compiles CUDA kernels and does not link `libcudart`.

REST is compiled into the default binary. It does not listen until `rest_api.enabled` is set. Routes are under `/api/v1`. They are not Bitcoin Core `/rest/*`. Payment REST routes are not served. Fee estimates from `blvm-index` are the node's own paths (`GET /fee-estimates` and `GET /api/fee-estimates`).

## Mempool

`RbfConfig::default` sets `allow_package_replacements` to `true` and `mode` to standard. `min_relay_fee_rate` defaults to `100`, in satoshis per 1,000 virtual bytes. A 67-virtual-byte transaction at that floor pays 7 satoshis. That is 0.1 sat/vB. Replacement still requires BIP125 signaling (sequence below `0xffffffff`).

## Assume-valid

These seeds are this binary's. They are not Bitcoin Core's `defaultAssumeValid`. The Core checkout `f0de87f040` comments mainnet `defaultAssumeValid` as height `966143`. Do not copy that hash onto height `912683`.

| Network | Seeded height | Header hash |
|---------|---------------|-------------|
| mainnet | 912683 | `00000000000000000000611fd22f2df7c8fbd0688745c3a6c3bb5109cc2a12cb` |
| testnet | 4550000 | unset |
| signet | 267665 | unset |
| testnet4 | 0 | no assume-valid section |
| regtest | 0 | no assume-valid section |

When the hash is unset, script checks still run. A CLI disable sets the height to 0 and clears the hash. Fork choice states no maximum reorg depth. Do not copy another node's 1024 or 288.

Mainnet AssumeUTXO data in this tree is an empty list. The node does not publish a mainnet snapshot. Regtest has a test entry at height 100. A matching MuHash is not a snapshot load.

## Mainnet initial sync {#mainnet-initial-sync}

1. Use a data directory with room for the chain you intend to keep. This page does not publish a disk figure.
2. Leave assume-valid at the mainnet seed above, or disable it. Do not paste Core's anchor hash onto `912683`.
3. Confirm RPC with the cookie file, not a shared password copied from a Core example.
4. ZMQ, if you use it, is the loopback binds above.
5. Electrum and Esplora stay closed until `[services]` sets `listen`.
6. Keep mainnet Lightning channel funds off this module until a restart and a reorg deeper than the LDK tip are in the test record.

Chain import from a Bitcoin Core datadir is [Node operations](../node/operations.md). Deployment limits are [Deployment posture](../security/deployment-posture.md).
