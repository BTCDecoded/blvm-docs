# System Overview

{{#include ../../../DESIGN.md}}

## BLLVM Stack Architecture

![BLLVM Stack Architecture](../images/stack.png)
*Figure: BLLVM architecture showing bllvm-spec (Orange Paper) as the foundation, bllvm-consensus as the core implementation with verification paths (Kani proofs, spec drift detection, hash verification), and dependent components (bllvm-protocol, bllvm-node, bllvm-sdk) building on the verified consensus layer.*

## Complete Bitcoin Commons Architecture

![Bitcoin Commons Architecture](../images/architecture-trans.png)
*Figure: The complete seven-repository architecture showing how mathematical specification, formal verification, modular design, and cryptographic governance work together.*

## Tiered Architecture

![Tiered Architecture](../images/tier-architecture.png)
*Figure: Tiered architecture: Tier 1 = Orange Paper + Consensus Proof (mathematical foundation); Tier 2 = Protocol Engine (protocol abstraction); Tier 3 = Reference Node (complete implementation); Tier 4 = Developer SDK + Governance (developer toolkit + governance enforcement).*

