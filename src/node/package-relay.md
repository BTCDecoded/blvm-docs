# Package Relay (BIP331)

## Overview

Package Relay (BIP331) enables nodes to relay and validate groups of transactions together as atomic units. This is particularly useful for fee-bumping (RBF) transactions, CPFP (Child Pays For Parent) scenarios, and atomic transaction sets.

**Specification**: [BIP 331](https://github.com/bitcoin/bips/blob/master/bip-0331.mediawiki)

## Architecture

### Package Structure

A transaction package contains:

`TransactionPackage` in `blvm-node/src/network/package_relay.rs` carries the transactions in parent-first order, the package id, the combined fee, the combined weight, and `fee_known`.

### Package ID

`PackageId::from_transactions` sorts the package wtxids lexicographically and hashes that byte string once with SHA256. With no witness, the wtxid is the txid.


## Validation Rules

### Size Limits

- **Maximum Transactions**: 25 (BIP331 limit)
- **Maximum Weight**: 404,000 WU (~101,000 vB)
- **Minimum Fee Rate**: 100 satoshis per 1,000 virtual bytes (0.1 sat/vB)


### Ordering Requirements

Transactions must be ordered with parents before children:

- Each transaction's inputs that reference in-package parents must reference earlier transactions
- Invalid ordering results in `InvalidOrder` rejection


### Fee Calculation

The package fee is the sum of the transaction fees. When `fee_known` is set, the package pays at least `min_fee_rate` satoshis per 1,000 virtual bytes, rounded up. Virtual size is `combined_weight` divided by 4, rounded up.


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


## Package Manager

### PackageRelay

The `PackageRelay` manager handles:

- Package validation
- Package state tracking
- Package acceptance/rejection
- Package relay to peers


### Package States

```rust
pub enum PackageStatus {
    Pending,      // Awaiting validation
    Accepted,     // Validated and accepted
    Rejected { reason: PackageRejectReason },
}
```


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


## Validation Process

1. **Size Check**: Verify transaction count ≤ 25
2. **Weight Check**: Verify combined weight ≤ 404,000 WU
3. **Ordering Check**: Verify parents before children
4. **Duplicate Check**: Verify no duplicate transactions
5. **Fee Calculation**: Calculate combined fee and fee rate
6. **Fee Rate Check**: Verify fee rate ≥ minimum
7. **Structure Check**: Verify valid package structure


## Network Integration

### Package Messages

- `PackageRelay`: Relay package to peers
- `PackageAccept`: Package accepted by peer
- `PackageReject`: Package rejected with reason


### Handler Integration

The `PackageRelayHandler` processes incoming package messages:

- Receives package relay requests
- Validates packages
- Accepts or rejects packages
- Relays accepted packages to other peers


## Defaults

`PackageValidator` in `blvm-node/src/network/package_relay.rs` uses the three limits above. There is no `[network.package_relay]` table.


## Source

- [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs)
- [package_relay_handler.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay_handler.rs)

