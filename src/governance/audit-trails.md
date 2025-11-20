# Audit Trails

Bitcoin Commons maintains immutable audit trails of all governance decisions using cryptographic hash chains and Bitcoin blockchain anchoring.

## Audit Log System

The governance system maintains tamper-evident audit logs that record:

- **All Governance Decisions**: Every PR merge, signature, and veto
- **Maintainer Actions**: Key generation, rotation, and usage
- **Emergency Activations**: Emergency mode activations and deactivations
- **Economic Node Signals**: Veto signals and economic activity

## Cryptographic Properties

- **Hash Chains**: Each log entry includes hash of previous entry
- **Bitcoin Anchoring**: Monthly registry anchoring via OpenTimestamps
- **Immutable**: Logs cannot be modified without detection
- **Verifiable**: Anyone can verify log integrity

## Audit Log Verification

Audit logs can be verified using:

```bash
bllvm-commons verify-audit-log --log-path audit.log
```

## Three-Layer Verification Architecture

The governance system implements three complementary verification layers:

![Three-Layer Verification](../images/three-layer-verification-arch.png)
*Figure: Three-layer verification: GitHub merge control, real-time Nostr transparency, and OpenTimestamps historical proof.*

## Audit Trail Completeness

![Audit Trail Completeness](../images/audit-trail-completeness.png)
*Figure: Audit-trail completeness across governance layers.*

## OpenTimestamps Integration

The system uses OpenTimestamps to anchor audit logs to the Bitcoin blockchain:

- **Monthly Anchoring**: Registry state anchored monthly
- **Immutable Proof**: Proof of existence at specific time
- **Public Verification**: Anyone can verify timestamps

For detailed audit log documentation, see [AUDIT_LOG_SYSTEM.md](../../modules/bllvm-commons/docs/AUDIT_LOG_SYSTEM.md).

