# Repository layout

How the Bitcoin Commons Rust implementation is split across repositories, why, and how local development and CI relate.

## Summary

Bitcoin Commons is a specification-first project. The canonical artifact is the specification, the Orange Paper together with the formal spec, and implementations conform to it. The Rust codebase under the BTCDecoded organization is the first implementation of that specification, not the reference and not a privileged one. The project anticipates multiple independent implementations over time, in other languages, each conforming to the same specification. No implementation is meant to be the one others defer to. That deference is reserved for the spec.

The rest of this document describes how that first implementation is organized: as independent, individually versioned crates across separate repositories rather than a single monorepo, with a local development workflow that recovers workspace ergonomics and a CI workflow that verifies the published dependency graph.

## What the Codebase Contains

The repositories described here make up the Rust implementation, the first implementation of the Bitcoin Commons specification. They fall into a few categories.

The layered core consists of blvm-primitives, blvm-consensus, blvm-protocol, blvm-node, and blvm-sdk. These form the spine of the system, from foundational types up through the node binary and the software development kit.

The standalone cryptographic and infrastructure crates include blvm-secp256k1, blvm-muhash, and blvm-miniscript. These have value entirely independent of Bitcoin Commons. Any Rust project that needs a fast secp256k1 implementation or a MuHash accumulator can consume these directly without adopting anything else from the project.

The modules include blvm-lightning, blvm-stratum-v2, blvm-mesh, blvm-governance, and blvm-selective-sync. Each targets a specific extension point and can be adopted on its own.

The verification layer is blvm-spec-lock, which locks the implementation to the formal specification.

Supporting repositories cover benchmarks, documentation, and continuous integration tooling.

## The Central Principle: Specification-First Coherence

Correctness in Bitcoin Commons is enforced by the formal specification, not by the physical arrangement of any implementation's code. This is what explains nearly every structural decision below.

It holds at two levels. Across implementations, a future implementation in another language is correct because it conforms to the same specification the Rust implementation conforms to. Nothing about the Rust code is authoritative for that other implementation. The spec is. Within the Rust implementation, the consensus-critical layers agree with each other for the same reason: each one independently conforms to the Orange Paper and the formal spec, and the spec-lock proves that conformance.

In a typical layered application the layers agree because they are compiled together and their types line up at the boundaries. Proximity is load-bearing, so a monorepo is natural, because the structure itself is part of what keeps the system correct. Bitcoin Commons holds together differently. The agreement between components, and between entire implementations, is enforced at the level of the specification rather than by any code's physical layout, so the repository structure is not load-bearing for correctness. The specification is.

Because the spec rather than the structure holds the system together, the repositories can be arranged to serve other goals, independent consumption, clear boundaries, and resistance to structural drift, without sacrificing the guarantee that the components remain coherent. The same property that lets a separate C or Go implementation stand as a first-class citizen alongside the Rust one lets the Rust implementation's own crates live in separate repositories without losing coherence.

## Why Separate Repositories

Separate repositories are published rather than a single workspace for three reasons.

Independent consumption. Several crates have value outside the project. A separately published crate with its own version history can be adopted by any project in the ecosystem without taking on a dependency relationship to the node or its release cadence. This is ordinary practice in the Rust ecosystem for infrastructure and cryptographic libraries, where primitives are published as independent crates that unrelated projects consume piecemeal. That is the relevant comparison class, not single-product application monorepos.

Boundary enforcement. The governance model assigns jurisdiction by the public merge record per crate, with a contributor's domain extending one hop along the dependency graph, determined automatically rather than by human adjudication. This stays clean only when crate boundaries are hard and unambiguous. In a workspace, a contributor can introduce a path dependency that quietly couples two crates, and nothing structural prevents it. With separately published, versioned dependencies, crossing a boundary means taking a dependency on a published version, which makes coupling explicit rather than accidental. This applies to the dependency graph the same discipline the project applies through required independent review, removing reliance on human vigilance wherever a structural guarantee can replace it.

Design horizon. Bitcoin Commons is built to outlast its current contributors and to resist the slow concentration of authority that captures informally governed systems over time. Convention-enforced boundaries inside a workspace depend on every future reviewer noticing and rejecting boundary violations, and over a long enough horizon that vigilance cannot be assumed. Explicit, versioned, published boundaries do not depend on anyone noticing, because the cost of crossing them is built into the structure. That property compounds over time rather than decaying, and it maps onto the project's core purpose.

## The Local Development Workflow

Local development uses a `[patch.crates-io]` section in the Cargo configuration that redirects the inter-crate dependencies to local paths. With a contributor's repositories checked out, the implementation compiles and tests as a single unit, the same as it would in a workspace, and changes spanning multiple crates can be developed and tested together without waiting on publication. The workspace ergonomics that make a monorepo pleasant are available during development, so the local friction of separate repositories is handled without collapsing the published structure.

## The Continuous Integration Workflow

Continuous integration removes the `[patch.crates-io]` section. With the patch stripped, the build resolves dependencies against the actually published crates rather than local paths.

A workspace always builds against the in-tree code, so it never verifies that the published crates work together as published. Incompatibilities between published versions can go undetected until a downstream consumer hits them, because nothing in the project's own pipeline exercises the published-dependency path. Stripping the patch on CI closes that gap: the build resolves against the published crates and verifies the real dependency graph the way an external consumer experiences it. Local development exercises the convenient path through the patch, CI exercises the real path by removing it, and the path that ships is the one that gets verified.

## On the Choice of Structure

The conventional default for a multi-crate Rust effort is a workspace monorepo, and for most projects that is the better choice. Bitcoin Commons departs from it because its constraints differ: a specification-first consensus system built for multiple independent implementations, with independently consumable components and a multi-decade horizon. A monorepo would optimize for compile-time convenience, which the local patch already provides, while giving up the independent consumption, boundary enforcement, and capture resistance described above.

## See Also

- [Contributing](contributing.md) — developer workflow from setup to merge
- [Stack overview](../architecture/system-overview.md) — six-layer stack
- [Crate dependencies](../architecture/component-relationships.md) — crate dependency graph
- [Layer-Tier Model](../governance/layer-tier-model.md) — governance layers mapped to repositories
- [CI/CD Workflows](ci-cd-workflows.md) — what runs when you push code
