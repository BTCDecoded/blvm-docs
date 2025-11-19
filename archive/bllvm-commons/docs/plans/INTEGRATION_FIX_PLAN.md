# Integration Fix Plan

## Goal
Fix all remaining integration issues without backwards compatibility concerns.

## Plan

### 1. Update MiningCoordinator to Accept Real MempoolManager
- Change `MiningCoordinator` to accept `Arc<MempoolManager>` instead of `MockMempoolProvider`
- Update constructor to take `Arc<MempoolManager>`
- Remove `MockMempoolProvider` from production code (keep only for tests)

### 2. Add UTXO Set Access to MiningCoordinator
- Add `storage: Option<Arc<Storage>>` field to `MiningCoordinator`
- Update `generate_block_template()` to get UTXO set from storage
- Pass UTXO set to `select_transactions()`

### 3. Remove Deprecated Methods
- Remove `MiningCoordinator::get_prioritized_transactions()` (deprecated, no UTXO set)
- Update all call sites to use mempool directly with UTXO set

### 4. Fix Test Code
- Update all tests to provide empty UTXO set where needed
- Fix `select_transactions()` calls in tests

### 5. Update Node Integration
- Update `Node::new()` to pass real `MempoolManager` to `MiningCoordinator`
- Pass `Storage` to `MiningCoordinator` for UTXO access

## Validation

### Benefits
- ✅ Real mempool integration in production
- ✅ Accurate fee calculation everywhere
- ✅ No duplicate code paths
- ✅ Cleaner API surface

### Risks
- ⚠️ Breaking changes to `MiningCoordinator` API
- ⚠️ Test code needs updates
- ⚠️ Need to ensure Storage is accessible

### Mitigation
- Tests can use `MockMempoolProvider` still (separate from production)
- Storage access is already available in Node
- Changes are internal to node module

## Implementation Order
1. Update `MiningCoordinator` struct and constructor
2. Add Storage field and UTXO access
3. Update `generate_block_template()` to use UTXO set
4. Remove deprecated methods
5. Update `Node::new()` integration
6. Fix test code

