# Pre-Release Resolution Plan: High Priority Issues

## Overview

This plan addresses P0 (Critical - Blocks Production) and P1 (High Priority - Needs Implementation) issues identified in `PRE_RELEASE_CLEANUP.md`.

## Phase 1: Critical P0 Issues (Must Fix Before Release)

### 1.1 Genesis Block Implementation ✅ VERIFIED COMPLETE (2025-01-XX)

**Status**: ✅ Complete and Verified
**File**: `bllvm-protocol/src/genesis.rs`
**Action**: No action needed - implementation is complete
**Verification**: Genesis blocks for mainnet, testnet, and regtest are properly implemented with correct hashes, timestamps, and transactions. All three networks have proper genesis blocks. Hashes verified to match Bitcoin Core exactly:
- Mainnet: `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`
- Testnet: `000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943`
- Regtest: `0f9188f13cb7b2c1f22c6712f09f5a324fbaf64c5354cbc65b4aec4a4c94b6ef`

**Note**: Previously listed as placeholder in some documentation, but verified complete.

### 1.2 Emergency Signature Verification

**File**: `governance-app/src/validation/emergency.rs:266`
**Current**: Placeholder with basic validation only
**Required**: Implement cryptographic signature verification using bllvm-sdk

**Implementation Steps**:
1. ✅ `bllvm-sdk` dependency already present in `governance-app/Cargo.toml`
2. Import signature verification from `bllvm_sdk::governance::verification::verify_signature`
3. Replace placeholder in `validate_keyholder_signature()`:
   - Parse `sig.public_key` (hex string) to `bllvm_sdk::governance::PublicKey`
   - Parse `sig.signature` (hex string) to `bllvm_sdk::governance::Signature`
   - Construct message to verify from `activation`:
     - Serialize `EmergencyActivation` (tier, reason, evidence, activated_by)
     - Or use a canonical format: `format!("{}:{}:{}", activation.tier, activation.reason, activation.activated_by)`
   - Call `bllvm_sdk::governance::verification::verify_signature(&signature, message_bytes, &public_key)?`
   - Return `GovernanceAppError::InvalidSignature` if verification fails
4. Add tests for valid/invalid signatures
5. Document signature format and message structure

**Key Details**:
- `KeyholderSignature` has: `keyholder: String`, `public_key: String` (hex), `signature: String` (hex)
- Need to determine canonical message format for emergency activations
- Use `PublicKey::from_hex()` and `Signature::from_bytes()` for parsing

**Dependencies**: `bllvm-sdk` already available
**Estimated Time**: 2-3 hours

### 1.3 Database Query Implementation

**File**: `governance-app/src/database/queries.rs`
**Current**: All 7 functions return empty/None
**Required**: Implement proper SQLite queries

**Functions to Implement**:
1. `get_pull_request()` - Query `pull_requests` table
2. `get_maintainers_for_layer()` - Query `maintainers` table filtered by layer
3. `get_emergency_keyholders()` - Query `emergency_keyholders` table
4. `get_governance_events()` - Query `governance_events` table with limit
5. `create_pull_request()` - INSERT into `pull_requests` table
6. `add_signature()` - INSERT/UPDATE in `signatures` table
7. `log_governance_event()` - INSERT into `governance_events` table

**Implementation Steps**:
1. ✅ Review database schema in `governance-app/migrations/001_initial_schema.sql`
2. Note: Some functions already implemented in `database/mod.rs` (create_pull_request, add_signature, log_governance_event)
3. Implement remaining functions in `queries.rs`:
   - `get_pull_request()`: `SELECT * FROM pull_requests WHERE repo_name = ? AND pr_number = ?`
   - `get_maintainers_for_layer()`: `SELECT * FROM maintainers WHERE layer = ? AND active = true`
   - `get_emergency_keyholders()`: `SELECT * FROM emergency_keyholders WHERE active = true`
   - `get_governance_events()`: `SELECT * FROM governance_events ORDER BY timestamp DESC LIMIT ?`
4. Use `sqlx::query_as!` macro for type-safe queries
5. Map query results to model types from `models.rs`
6. Handle errors appropriately (convert sqlx::Error to return type)
7. Add tests for each query function
8. Consider: Should `queries.rs` functions be removed in favor of `database/mod.rs` methods?

**Key Details**:
- Database supports both SQLite and PostgreSQL (use parameterized queries)
- Models defined in `governance-app/src/database/models.rs`
- Some functions already exist in `database/mod.rs` - may need to consolidate

**Dependencies**: Database schema defined in migrations
**Estimated Time**: 3-4 hours (some work already done)

### 1.4 Cross-layer File Verification

**File**: `governance-app/src/validation/cross_layer.rs:108`
**Current**: Placeholder warning, always returns success
**Required**: Implement actual file correspondence verification

**Implementation Steps**:
1. Determine what "file correspondence" means:
   - Check if files referenced in source repo exist in target repo?
   - Verify file contents match?
   - Verify file paths match patterns?
2. Use GitHub API client (already in `governance-app/src/github/client.rs`)
3. Implement `verify_file_correspondence()`:
   - Parse source and target patterns
   - Query GitHub API for files matching patterns
   - Compare file existence/content as needed
   - Return error if correspondence fails
4. Remove placeholder warning
5. Add tests

**Dependencies**: GitHub API client, clear specification of correspondence rules
**Estimated Time**: 3-4 hours

### 1.5 Maintainer Key Management

**Files**: `governance/config/maintainers/*.yml`
**Current**: All keys are `0x02[PLACEHOLDER_64_CHAR_HEX]`
**Required**: Document as test-only OR replace with real keys

**Options**:
- **Option A (Recommended for Pre-Release)**: Document that placeholder keys are for testing only, add clear warnings
- **Option B (Production)**: Generate real keys and store securely

**Implementation Steps (Option A)**:
1. Add clear documentation in each YAML file: `# WARNING: Placeholder keys for testing only. DO NOT USE IN PRODUCTION.`
2. Add validation in governance-app to reject placeholder keys in production mode
3. Create key generation guide for production deployment
4. Update security documentation

**Implementation Steps (Option B)**:
1. Generate real cryptographic keys for each maintainer
2. Store keys securely (encrypted, not in repo)
3. Update config files with key references (not actual keys)
4. Document key management procedures

**Recommended**: Option A for pre-release, Option B for production
**Estimated Time**: 1-2 hours (Option A) or 4-8 hours (Option B)

## Phase 2: High Priority P1 Issues (Before Production)

### 2.1 Protocol Message Processing Integration

**File**: `bllvm-node/src/network/message_bridge.rs:90`
**Current**: Only converts messages, doesn't process them
**Required**: Integrate with `bllvm_protocol::network::process_network_message()`

**Implementation Steps**:
1. Update `process_incoming_message()` signature to accept:
   - `&BitcoinProtocolEngine`
   - `&mut PeerState` (per-peer state management)
   - `Option<&dyn ChainStateAccess>` (use `NodeChainAccess` from `chain_access.rs`)
   - `Option<&UtxoSet>`
   - `Option<u64>` (current height)
2. Call `bllvm_protocol::network::process_network_message()`
3. Convert `NetworkResponse` to wire format using existing `extract_send_messages()`
4. Update callers in network layer to provide required parameters
5. Add tests

**Dependencies**: `NodeChainAccess` implementation (already done)
**Estimated Time**: 3-4 hours

### 2.2 Mining RPC Implementation

**File**: `bllvm-node/src/rpc/mining.rs`
**Current**: Many placeholder implementations
**Required**: Implement actual mining RPC methods

**Functions to Implement**:
1. `get_mining_info()` - Query actual mining state from `node::miner`
2. `get_block_template()` - Get prioritized transactions from mempool
3. `submit_block()` - Deserialize, validate, and accept blocks
4. `estimate_fee()` - Calculate fee from mempool state
5. `get_network_hash_ps()` - Calculate network hashrate
6. Parameter extraction for various methods

**Implementation Steps**:
1. Add `MempoolManager::get_prioritized_transactions()` method
2. Connect RPC methods to actual node components:
   - `Node::miner()` for mining state
   - `Node::mempool()` for transaction queries
   - `Node::storage()` for chain state
3. Implement fee estimation algorithm
4. Implement sigop counting (may already exist in consensus layer)
5. Add comprehensive tests

**Dependencies**: MempoolManager enhancements, node component access
**Estimated Time**: 6-8 hours

### 2.3 Module System TODOs

**Files**: Multiple in `bllvm-node/src/module/`
**Current**: Various placeholders and incomplete implementations

**Priority Order**:
1. **Process Monitoring Heartbeat** (`process/monitor.rs:87`)
   - Add IPC heartbeat check
   - Implement timeout detection
   - Estimated: 2-3 hours

2. **Module Manager Process Sharing** (`manager.rs:182`)
   - Refactor to properly share process handles
   - Fix lifecycle management
   - Estimated: 3-4 hours

3. **IPC Server Connection Handling** (`ipc/server.rs:123,372`)
   - Fix temporary ID generation
   - Complete connection handling
   - Estimated: 2-3 hours

4. **Resource Limits** (`security/validator.rs:85`) - Phase 2 feature
5. **Process Sandboxing** (`sandbox/process.rs:88`) - Phase 2 feature
6. **Node API Event System** (`api/node_api.rs:155`) - Future enhancement

**Total Estimated Time**: 7-10 hours for immediate items

### 2.4 BIP70 Payment Protocol

**File**: `bllvm-node/src/bip70.rs`
**Current**: Payment verification and ACK signing not implemented

**Implementation Steps**:
1. Implement transaction verification against PaymentRequest
2. Validate merchant_data matches original request
3. Implement PaymentACK signing with merchant key
4. Add tests

**Estimated Time**: 4-5 hours

### 2.5 BIP158 Compact Block Filters

**File**: `bllvm-node/src/bip158.rs`
**Current**: GCS decoder and matcher are simplified placeholders

**Implementation Steps**:
1. Implement proper Golomb-Rice coding decoder
2. Implement bit-level GCS matching
3. Add tests with real filter data
4. Performance optimization

**Dependencies**: GCS library or implementation
**Estimated Time**: 6-8 hours

## Phase 3: Implementation Order

### Week 1: Critical P0 Issues (Must Complete Before Release)
1. ✅ Genesis blocks (already complete - no action needed)
2. Emergency signature verification (2-3 hours)
3. Database queries (3-4 hours - some already done)
4. Cross-layer file verification (3-4 hours)
5. Maintainer keys documentation (1-2 hours)

**Total**: ~9-13 hours

### Week 2: High Priority P1 Issues
1. Protocol message processing (3-4 hours)
2. Mining RPC core methods (6-8 hours)
3. Module system critical TODOs (7-10 hours)

**Total**: ~16-22 hours

### Week 3: Remaining P1 Issues
1. BIP70 implementation (4-5 hours)
2. BIP158 implementation (6-8 hours)
3. Testing and integration (4-6 hours)

**Total**: ~14-19 hours

## Risk Assessment

### High Risk
- **Database queries**: Schema changes could break implementation
- **Cross-layer verification**: Requires clear specification of rules
- **BIP158**: Complex cryptographic implementation

### Medium Risk
- **Emergency signatures**: Depends on bllvm-sdk API stability
- **Mining RPC**: Requires coordination with node architecture
- **Module system**: Complex state management

### Low Risk
- **Maintainer keys**: Documentation-only change
- **Protocol message processing**: Well-defined API
- **BIP70**: Straightforward implementation

## Testing Strategy

For each implementation:
1. Unit tests for new functions
2. Integration tests with real components
3. Error path testing
4. Performance testing where applicable

## Success Criteria

### P0 Issues (Pre-Release)
- ✅ All placeholders removed or documented
- ✅ All critical functions implemented
- ✅ Tests passing
- ✅ No security warnings
- ✅ Can run governance-app without placeholder errors

### P1 Issues (Before Production)
- ✅ Core functionality implemented
- ✅ Integration with existing systems
- ✅ Tests passing
- ✅ Documentation updated
- ✅ No "for now" or "simplified" comments in critical paths

## Quick Start: Immediate Actions

### Today (Highest Priority)
1. **Emergency Signature Verification** - 2-3 hours
   - Most critical security issue
   - Clear implementation path
   - bllvm-sdk already available

2. **Database Queries** - 3-4 hours
   - 4 functions to implement
   - Schema already defined
   - Some work already done in `database/mod.rs`

### This Week
3. **Cross-layer File Verification** - 3-4 hours
4. **Maintainer Keys Documentation** - 1-2 hours
5. **Protocol Message Processing** - 3-4 hours (P1 but important)

### Next Week
6. **Mining RPC Implementation** - 6-8 hours
7. **Module System TODOs** - 7-10 hours

## Notes

- ✅ Genesis blocks are already correctly implemented - verified complete (2025-01-XX)
- ✅ Integration test failures fixed - proper header chains now provided (2025-01-XX)
- ✅ Panic!/unwrap() in consensus code verified safe - all in test/proof code (2025-01-XX)
- Maintainer keys: Prefer documentation approach for pre-release, real keys for production
- Module system: Some TODOs are Phase 2 features (sandboxing, rate limiting) - defer if appropriate
- BIP implementations: May be lower priority if not critical for initial release

