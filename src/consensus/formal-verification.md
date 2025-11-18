# Formal Verification

The consensus layer implements formal verification for Bitcoin consensus rules using a multi-layered approach.

{{#include ../../../modules/bllvm-consensus/docs/VERIFICATION.md}}

## Consensus Coverage Comparison

![Consensus Coverage Comparison](../images/Consensus-Coverage-Comparison.png)
*Figure: Consensus coverage comparison: Bitcoin Core achieves coverage through testing alone. Bitcoin Commons achieves formal verification coverage (Kani proofs) plus comprehensive test coverage. Commons uses consensus-focused test files with extensive test functions compared to Core's total files. The mathematical specification enables both formal verification and comprehensive testing.*

## Proof Maintenance Cost

![Proof Maintenance Cost](../images/proof-maintenance-cost.png)
*Figure: Proof maintenance cost: proofs updated per change by area; highlights refactor hotspots; Commons aims for lower proof churn than Core.*

## Spec Drift vs Test Coverage

![Spec Drift vs Test Coverage](../images/spec-drift-vs-test-coverage.png)
*Figure: Spec drift decreases as test coverage increases. Higher test coverage reduces the likelihood of specification drift over time.*

## Network Protocol Verification

The network protocol message parsing, serialization, and processing are formally verified using Kani model checking, extending formal verification beyond consensus to the network layer.

### Verified Properties

1. **Message Header Parsing**: Magic number, command string, payload length, checksum extraction
2. **Checksum Validation**: Invalid checksums are rejected, checksum calculation correctness
3. **Size Limit Enforcement**: Oversized messages are rejected, payload size limits enforced
4. **Round-Trip Properties**: All message types verify `parse(serialize(msg)) == msg`

### Verified Message Types

**Phase 1: Core Messages** (8 proofs):
- Version, VerAck, Ping, Pong messages

**Phase 2: Consensus-Critical Messages** (8 proofs):
- Transaction, Block, Headers, Inv, GetData, GetHeaders messages

### Mathematical Specifications

**Round-Trip Property:**
```
∀ msg ∈ ProtocolMessage: parse(serialize(msg)) = msg
```

**Checksum Validation:**
```
∀ payload, checksum: checksum ≠ calculate_checksum(payload) ⟹
  parse_message(payload, checksum) = error
```

**Size Limit Enforcement:**
```
∀ message: |message| > MAX_PROTOCOL_MESSAGE_LENGTH ⟹
  parse_message(message) = error
```

### Running Network Verification

```bash
# Install Kani
cargo install kani-verifier --version 0.41.0

# Run all network protocol proofs
cd bllvm-node
cargo kani --features verify
```

Network protocol verification runs automatically in CI. All proofs must pass, and verification code is excluded from release builds via the `verify` feature.

