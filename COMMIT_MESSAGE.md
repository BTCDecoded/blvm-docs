# Intended commits

## `blvm-node` (and related crates touching IPC)

Single commit for **unpushed** work: original getdata / selective-withhold behavior **plus** the module IPC / `NodeAPI` extensions.

**Title:**

```
feat(node): P2P getdata, selective withhold, and module IPC serve policy
```

**Body:**

```
- getdata_serve: MSG_BLOCK/MSG_TX from storage; notfound for gaps; segwit witness check;
  serve after IBD bandwidth gate (serve_getdata_request).
- selective_sync_withheld: optional selective_sync/withheld_blocks.json — listed block
  hashes never sent as full block messages (notfound) even if partial data exists.
- IPC / NodeAPI: Merge/Get/Clear/Replace block and tx serve denylists; snapshots;
  GetSyncStatus; BanPeer; SetBlockServeMaintenanceMode (MessageType / RequestPayload /
  server wiring); getdata_serve applies denylists and maintenance mode for MSG_BLOCK /
  MSG_TX.
- NetworkManager: denylist maintenance, snapshots, sync coordinator exposure for IPC
  handlers.
```

## `blvm-selective-sync`

**Title:**

```
feat: forward withheld hashes into node block/tx serve denylists
```

**Body:**

```
- Use NodeAPI merge_*_serve_denylist (and related helpers) so selective-sync policy can
  align local withholding with P2P getdata behavior via the node.
```

## `blvm-docs`

**Title:**

```
docs: module IPC, NodeAPI hooks, and selective-sync P2P policy
```

**Body:**

```
- module-development: document P2P serve policy & sync NodeAPI methods; clarify events
  vs writes; mesh send_mesh_packet_to_peer vs send_mesh_packet_to_module (IPC).
- module-ipc-protocol: request table for denylist, sync, ban, maintenance.
- module-system: events vs targeted node control.
- selective-sync: link policy to merge_*_serve_denylist and IPC docs.
```
