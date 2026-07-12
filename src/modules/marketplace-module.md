# Marketplace module (`blvm-marketplace`)

Optional **module discovery, registry, and payment** integration for **`blvm-node`**. Most operators use **`[modules].registry_url`** bootstrap (GitHub Releases + `modules.json`) without loading this module.

## Overview

**blvm-marketplace** can:

- Serve or proxy **module registry** metadata (legacy: **`[modules.blvm-marketplace] registry_url`** fallback when top-level **`[modules].registry_url`** is unset)
- Handle **paid module installs** and revenue split logic when payment features are enabled
- Respond to **`fetch_module`** inter-module calls when **`loadmodule`** marketplace auto-fetch is enabled (opt-in, **off by default**)

**Repository:** [BTCDecoded/blvm-marketplace](https://github.com/BTCDecoded/blvm-marketplace)

## Requirements

- `blvm-node` with the module system enabled.
- Payment flows require compile-time **`bip70-http`** / payment processor wiring on the node (**`blvm` default features**; omitted from portable Windows/aarch64 release builds).
- Not required for standard **registry bootstrap** of pinned modules: use [Installing modules](overview.md#installing-modules) instead.

## Loading

Optional pin (only if you use marketplace discovery/payments):

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-marketplace = "0.1.*"
```

Legacy registry URL placement (still supported when `[modules].registry_url` is omitted):

```toml
[modules.blvm-marketplace]
registry_url = "https://example.com/modules.json"
```

Prefer **`[modules].registry_url`** for bootstrap: see [Configuration reference](../reference/configuration-reference.md#modulesregistry_url).

## `loadmodule` and marketplace auto-fetch

By default, **`loadmodule "some-module"`** only loads modules already on disk under **`[modules].modules_dir`**. If the module is missing locally, RPC returns an error: marketplace auto-fetch is **disabled**.

When marketplace auto-fetch is enabled (**`[modules].marketplace_fetch_enabled = true`**, default **false**), the node may call **`blvm-marketplace`** via inter-module IPC (`fetch_module`) before retrying local discovery. Requires **`blvm-marketplace`** loaded.

**Operator default:** pin modules in **`blvm.toml`**, use registry bootstrap at startup, or **`blvm load <name>`** after placing binaries manually: do not rely on remote auto-fetch over RPC unless you explicitly enable and trust it.

## See also

- [Module catalog: Installing modules](overview.md#installing-modules)
- [Module system architecture](../architecture/module-system.md#module-registry)
- [RPC API: Module Methods](../node/rpc-api.md#module-methods)
