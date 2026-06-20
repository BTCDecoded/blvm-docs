# Governance Overview

Cryptographic governance for Bitcoin Commons repositories: tiers, signatures, and audit trails. **Not required for operating a node.**

**Running a node?** Use the [Operator guide](../getting-started/operator-guide.md) and [Deployment posture](../security/deployment-posture.md). Return here when you contribute code, sign releases, or configure governance tooling.

**Building modules?** See the [Developer guide](../getting-started/developer-guide.md) and [SDK overview](../sdk/overview.md).

## Governance documentation

| Topic | Guide |
|------|--------|
| Constitutional model, tiers, capture resistance | [Governance Model](governance-model.md) |
| Layers × tiers and signature rules | [Layer–tier model](layer-tier-model.md) |
| PR lifecycle, signatures, merge rules | [PR process](../development/pr-process.md) |
| Human review and AI review intelligence | [Review standards](#review-standards) |
| Multisig thresholds | [Multisig configuration](multisig-configuration.md) |
| Maintainer key duties | [Keyholder procedures](keyholder-procedures.md) |
| Audit logging and verification | [Audit trails](audit-trails.md) |
| Governance tooling config | [Governance configuration](configuration-system.md) |
| Governance forks | [Governance fork system](governance-fork.md) |
| P2P governance messages | [P2P governance messages](p2p-governance-messages.md) |
| blvm-commons enforcement | [blvm-commons](blvm-commons.md) |
| OpenTimestamps / Nostr integrations | [OpenTimestamps](opentimestamps-integration.md), [Nostr](nostr-integration.md) |
| Operator FAQ (governance) | [FAQ — governance](../appendices/faq.md#do-i-need-governance-to-run-a-node) |

The governance system enforces development processes cryptographically across Bitcoin Commons repositories. Module README (below) covers day-to-day governance module usage; the [Governance Model](governance-model.md) page includes the full constitutional document.

{{#include ../../modules/governance/README.md}}

## Review standards {#review-standards}

Human maintainer expectations and AI-assisted “review intelligence” for Bitcoin Commons code are **canonical in the [governance](https://github.com/BTCDecoded/governance) repository**—they are not duplicated in this book.

- **[Review expectations](https://github.com/BTCDecoded/governance/blob/main/REVIEW_EXPECTATIONS.md)** — Expected practices for **human** reviewers and maintainers (guidelines, not rigid rules; see challenge mechanism there).
- **[Review intelligence](https://github.com/BTCDecoded/governance/blob/main/guides/REVIEW_INTELLIGENCE.md)** — Operating document for **AI-assisted** review of Bitcoin implementations: true alternative vs Core fork taxonomy, flag structure, and alignment with the [Orange Paper](../reference/orange-paper.md) and the [Bitcoin Commons Compact](https://github.com/BTCDecoded/governance/blob/main/COMPACT.md).

For PR tiers, cryptographic signatures, and merge rules, see [PR process](../development/pr-process.md) and [Layer–tier model](layer-tier-model.md).

## See Also

- [Governance Model](governance-model.md) — Constitutional model and included `GOVERNANCE.md`
- [PR Process](../development/pr-process.md) — How tiers apply to pull requests
- [Multisig Configuration](multisig-configuration.md) — Configuring multisig thresholds
- [Keyholder Procedures](keyholder-procedures.md) — Maintainer responsibilities
- [Audit Trails](audit-trails.md) — Audit logging and verification
- [SDK API Reference](../sdk/api-reference.md) — Governance primitives API

