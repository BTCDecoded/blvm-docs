# RBF Configuration Example

Complete example of configuring RBF (Replace-By-Fee) for different use cases.

## Exchange Node Configuration

For exchanges that need to protect users from unexpected transaction replacements:

```toml
[rbf]
mode = "conservative"
min_fee_rate_multiplier = 2.0
min_fee_bump_satoshis = 5000
min_confirmations = 1
max_replacements_per_tx = 3
cooldown_seconds = 300

[mempool]
max_mempool_mb = 500
max_mempool_txs = 200000
min_relay_fee_rate = 2
eviction_strategy = "lowest_fee_rate"
max_ancestor_count = 25
max_descendant_count = 25
persist_mempool = true
```

**Why This Configuration:**
- **Conservative RBF**: Requires 2x fee increase, preventing low-fee replacements
- **1 Confirmation Required**: Additional safety check before allowing replacement
- **Higher Fee Threshold**: 2 sat/vB minimum relay fee filters low-priority transactions
- **Mempool Persistence**: Survives restarts for better reliability

## Mining Pool Configuration

For mining pools that want to maximize fee revenue:

```toml
[rbf]
mode = "aggressive"
min_fee_rate_multiplier = 1.05
min_fee_bump_satoshis = 500
allow_package_replacements = true
max_replacements_per_tx = 10
cooldown_seconds = 60

[mempool]
max_mempool_mb = 1000
max_mempool_txs = 500000
min_relay_fee_rate = 1
eviction_strategy = "lowest_fee_rate"
max_ancestor_count = 50
max_descendant_count = 50
```

**Why This Configuration:**
- **Aggressive RBF**: Only 5% fee increase required, maximizing fee opportunities
- **Package Replacements**: Allows parent+child transaction replacements
- **Larger Mempool**: 1GB capacity for more transaction opportunities
- **Relaxed Ancestor Limits**: 50 transactions for larger packages

## Standard Node Configuration

For general-purpose nodes with Bitcoin Core compatibility:

```toml
[rbf]
mode = "standard"
min_fee_rate_multiplier = 1.1
min_fee_bump_satoshis = 1000

[mempool]
max_mempool_mb = 300
max_mempool_txs = 100000
min_relay_fee_rate = 1
eviction_strategy = "lowest_fee_rate"
max_ancestor_count = 25
max_descendant_count = 25
mempool_expiry_hours = 336
```

**Why This Configuration:**
- **Standard RBF**: BIP125-compliant with 10% fee increase
- **Bitcoin Core Defaults**: Matches Bitcoin Core mempool settings
- **Balanced**: Good for most use cases

## Testing RBF Configuration

### Test Transaction Replacement

1. **Create initial transaction:**
```bash
# Send transaction with RBF signaling (sequence < 0xffffffff)
bitcoin-cli sendtoaddress <address> 0.001 "" "" true
```

2. **Replace with higher fee:**
```bash
# Create replacement with higher fee
bitcoin-cli bumpfee <txid> --fee_rate 20
```

3. **Verify replacement:**
```bash
# Check mempool
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getmempoolentry", "params": ["<new_txid>"], "id": 1}'
```

### Monitor RBF Activity

```bash
# Get mempool info
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "getmempoolinfo", "params": [], "id": 1}'
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "size": 1234,
    "bytes": 567890,
    "usage": 1234567,
    "maxmempool": 314572800,
    "mempoolminfee": 0.00001,
    "minrelaytxfee": 0.00001
  },
  "id": 1
}
```

## See Also

- [RBF and Mempool Policies](../node/rbf-mempool-policies.md) - Complete configuration guide
- [Node Configuration](../node/configuration.md) - All configuration options
- [Node Operations](../node/operations.md) - Managing your node





