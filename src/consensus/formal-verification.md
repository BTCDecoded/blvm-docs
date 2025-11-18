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

