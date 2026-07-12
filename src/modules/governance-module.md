# Governance module (`blvm-governance`)

On-chain proposal tracking and optional webhook notifications for **`blvm-node`**. Distinct from the **Bitcoin Commons governance framework** documented under [Governance](../governance/overview.md): this page covers the **loadable module** only.

## Overview

**blvm-governance** subscribes to chain events and can forward governance-related signals to an operator webhook (module-specific config). It does **not** replace tier signatures or repository governance rules.

**Repository:** [BTCDecoded/blvm-governance](https://github.com/BTCDecoded/blvm-governance)

## Requirements

- `blvm-node` with the module system enabled.
- **`governance`** compile-time feature on the **`blvm`** build (on by default in **`blvm` default features** / Linux x86_64 release artifacts) for registry bootstrap of pinned modules.
- Module pinned in **`registry/modules.json`** or built locally.

## Loading

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-governance = "0.1.*"
```

Optional node override:

```toml
[modules.blvm-governance]
webhook_url = "https://example.com/governance-hook"
```

Module data dir config: `<modules.data_dir>/blvm-governance/config.toml` (same keys).

## See also

- [Governance overview](../governance/overview.md): tiers, layers, signatures (not this module)
- [Module catalog](overview.md)
- [Installing modules](overview.md#installing-modules)
