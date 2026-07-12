# Building your first module

Tutorial: load a minimal read-only module on a regtest node and confirm it receives `NewBlock` events.

**Prerequisites:** [Quick Start](quick-start.md) (regtest node running), Rust toolchain, [Module system](../architecture/module-system.md) overview.

**Time:** ~15 minutes for an experienced Rust developer.

## What you will build

`hello-module`: a process-isolated module that:

- Declares `read_blockchain` and `subscribe_events` in `module.toml`
- Subscribes to `NewBlock` and logs the block hash
- Loads via a **`[modules]`** pin in `blvm.toml`

Full patterns (manifest fields, NodeAPI, publishing events) live in [Building modules](../sdk/module-development.md).

## 1. Scaffold the crate

```bash
mkdir -p modules/hello-module/src
cd modules/hello-module
```

`Cargo.toml` (minimal):

```toml
[package]
name = "hello-module"
version = "0.1.0" # your crate semver (not tied to BLVM releases)
edition = "2024"

[dependencies]
blvm-sdk = "0.1"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
tracing = "0.1"
tracing-subscriber = "0.3"
```

`module.toml`:

```toml
name = "hello-module"
version = "0.1.0" # manifest semver for your module
description = "Tutorial hello module"
entry_point = "hello-module"

capabilities = [
 "read_blockchain",
 "subscribe_events",
]
```

Implement `main.rs` using the `blvm-sdk` module runner: subscribe to `NewBlock`, log `block_hash` from the event payload. Copy the event-loop skeleton from [Building modules: Module lifecycle](../sdk/module-development.md#module-lifecycle) and replace the handler body with a `tracing::info!` on `NewBlock`.

## 2. Build the binary

```bash
cargo build --release
```

Expected: `target/release/hello-module` with no errors.

## 3. Install on the module search path

Either copy into the node modules directory:

```bash
NODE_MODULES=~/.local/share/blvm/modules
mkdir -p "$NODE_MODULES/hello-module/target/release"
cp target/release/hello-module "$NODE_MODULES/hello-module/target/release/"
cp module.toml "$NODE_MODULES/hello-module/"
```

Or pin a published crate via the registry (production path): see [Installing modules](../modules/overview.md#installing-modules).

## 4. Enable in `blvm.toml`

On the regtest node from [Quick Start](quick-start.md), add:

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
hello-module = "0.1.*" # local build: place binary under modules_dir first
modules_dir = "~/.local/share/blvm-quickstart/modules"
```

Restart the node with `--verbose`.

## 5. Verify loading

Expected log lines (wording may vary):

- Module `hello-module` loaded / started
- No capability or manifest errors

Mine a block ([Quick Start](quick-start.md) step 4) or use [First Node Setup](first-node.md). Expected when a block connects:

- `NewBlock` log line with a 32-byte hash from your module

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Module not loaded | Binary path matches `module.toml` `entry_point`; `modules_dir` correct |
| Manifest error | `module.toml` beside binary; capabilities match what the code requests |
| No events | Node actually connected a block; module subscribed to `NewBlock` |
| Build fails on `blvm-sdk` | MSRV and crate version: see [Contributing](../development/contributing.md) |

## Next steps

- [Building modules](../sdk/module-development.md): IPC, NodeAPI, publishing events, inter-module calls
- [Module catalog](../modules/overview.md): production modules (mesh, zmq, stratum-v2, …)
- [SDK overview](../sdk/overview.md)
