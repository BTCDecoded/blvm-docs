# Package Relay (BIP331)

## Overview

Package Relay (BIP331) enables nodes to relay and validate groups of transactions together as atomic units. This is particularly useful for fee-bumping (RBF) transactions, CPFP (Child Pays For Parent) scenarios, and atomic transaction sets.

**Specification**: [BIP 331](https://github.com/bitcoin/bips/blob/master/bip-0331.mediawiki)

## Architecture

### Package Structure

A transaction package contains:

```rust
pub struct TransactionPackage {
    pub transactions: Vec<Transaction>,  // Ordered: parents first
    pub package_id: PackageId,
    pub combined_fee: u64,
    pub combined_weight: usize,
}
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L34-L45)

### Package ID

Package ID is calculated as double SHA256 of all transaction IDs:

```rust
pub fn from_transactions(transactions: &[Transaction]) -> PackageId {
    let mut hasher = Sha256::new();
    for tx in transactions {
        let txid = calculate_txid(tx);
        hasher.update(txid);
    }
    let first = hasher.finalize();
    let mut hasher2 = Sha256::new();
    hasher2.update(first);
    PackageId(final_hash)
}
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L107-L134)

## Validation Rules

### Size Limits

- **Maximum Transactions**: 25 (BIP331 limit)
- **Maximum Weight**: 404,000 WU (~101,000 vB)
- **Minimum Fee Rate**: Configurable (default: 1 sat/vB)

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L86-L105)

### Ordering Requirements

Transactions must be ordered with parents before children:

- Each transaction's inputs that reference in-package parents must reference earlier transactions
- Invalid ordering results in `InvalidOrder` rejection

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L206-L250)

### Fee Calculation

Package fee is calculated as sum of all transaction fees:

```rust
combined_fee = sum(inputs) - sum(outputs) for all transactions
```

Fee rate is calculated as:

```rust
fee_rate = combined_fee / combined_weight
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L142-L204)

## Use Cases

### Fee-Bumping (RBF)

Parent transaction + child transaction that increases fee:

```
Package:
  - Parent TX (low fee)
  - Child TX (bumps parent fee)
```

### CPFP (Child Pays For Parent)

Child transaction pays for parent's fees:

```
Package:
  - Parent TX (insufficient fee)
  - Child TX (pays for parent)
```

### Atomic Transaction Sets

Multiple transactions that must be accepted together:

```
Package:
  - TX1 (depends on TX2)
  - TX2 (depends on TX1)
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L1-L15)

## Package Manager

### PackageRelay

The `PackageRelay` manager handles:

- Package validation
- Package state tracking
- Package acceptance/rejection
- Package relay to peers

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L22-L28)

### Package States

```rust
pub enum PackageStatus {
    Pending,      // Awaiting validation
    Accepted,     // Validated and accepted
    Rejected { reason: PackageRejectReason },
}
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L58-L67)

### Rejection Reasons

```rust
pub enum PackageRejectReason {
    TooManyTransactions,
    WeightExceedsLimit,
    FeeRateTooLow,
    InvalidOrder,
    DuplicateTransactions,
    InvalidStructure,
}
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L69-L84)

## Validation Process

1. **Size Check**: Verify transaction count ≤ 25
2. **Weight Check**: Verify combined weight ≤ 404,000 WU
3. **Ordering Check**: Verify parents before children
4. **Duplicate Check**: Verify no duplicate transactions
5. **Fee Calculation**: Calculate combined fee and fee rate
6. **Fee Rate Check**: Verify fee rate ≥ minimum
7. **Structure Check**: Verify valid package structure

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L250-L400)

## Network Integration

### Package Messages

- `PackageRelay`: Relay package to peers
- `PackageAccept`: Package accepted by peer
- `PackageReject`: Package rejected with reason

**Code**: [package_relay_handler.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay_handler.rs#L1-L200)

### Handler Integration

The `PackageRelayHandler` processes incoming package messages:

- Receives package relay requests
- Validates packages
- Accepts or rejects packages
- Relays accepted packages to other peers

**Code**: [package_relay_handler.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay_handler.rs#L1-L200)

## Configuration

```toml
[network.package_relay]
enabled = true
max_package_size = 25
max_package_weight = 404000  # 404k WU
min_fee_rate = 1000  # 1 sat/vB
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L86-L105)

## Benefits

1. **Efficient Fee-Bumping**: Better fee rate calculation for packages
2. **Reduced Orphans**: Reduces orphan transactions in mempool
3. **Atomic Validation**: Package validated as unit
4. **DoS Resistance**: Size and weight limits prevent abuse
5. **CPFP Support**: Enables child-pays-for-parent scenarios

## Components

The Package Relay system includes:
- Package structure and validation
- Package ID calculation
- Fee and weight calculation
- Ordering validation
- Package manager
- Network message handling

**Location**: `blvm-node/src/network/package_relay.rs`, `blvm-node/src/network/package_relay_handler.rs`

