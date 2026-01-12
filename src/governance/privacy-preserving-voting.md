# Privacy-Preserving Voting

## Overview

Bitcoin Commons implements privacy-preserving voting through contribution-based voting and zap-to-vote mechanisms. The system uses quadratic voting (square root of contribution amount) to prevent vote buying while allowing contributors to express preferences.

## Voting Mechanisms

### Contribution-Based Voting

Contributors receive voting weight based on their contributions:

- **Merge Mining**: Revenue contributions from merge mining
- **Fee Forwarding**: Transaction fee contributions
- **Zaps**: Lightning Network zap contributions
- **BIP70 Payments**: Payment protocol contributions

**Code**: ```1:200:blvm-commons/src/governance/contributions.rs```

### Zap-to-Vote

Zaps to governance events are converted into votes:

- **Proposal Zaps**: Zaps to governance event IDs
- **Vote Types**: Support, Veto, Abstain
- **Quadratic Weight**: Vote weight = sqrt(zap_amount_btc)
- **Message Parsing**: Vote type extracted from zap message

**Code**: ```1:293:blvm-commons/src/nostr/zap_voting.rs```

## Vote Weight Calculation

### Quadratic Formula

Vote weight uses quadratic formula to prevent vote buying:

```rust
vote_weight = sqrt(zap_amount_btc)
```

**Code**: ```60:63:blvm-commons/src/governance/weight_calculator.rs```

### Participation Weight

Base participation weight from contributions:

- **90-Day Window**: Contributions within 90 days
- **Contribution Types**: Merge mining, fee forwarding, zaps, BIP70
- **Cooling-Off Period**: New contributions have reduced weight

**Code**: ```65:90:blvm-commons/src/governance/weight_calculator.rs```

### Combined Weight

Proposal vote weight uses higher of zap or participation:

```rust
base_weight = max(zap_weight, participation_weight * 0.1)
final_weight = apply_weight_cap(base_weight, total_system_weight)
```

**Code**: ```65:90:blvm-commons/src/governance/weight_calculator.rs```

## Vote Types

### Support

Default vote type for proposal zaps:

- **Default**: If no message, vote is support
- **Message Keywords**: "support", "yes", "approve"
- **Weight**: Calculated from zap amount

### Veto

Opposition vote:

- **Message Keywords**: "veto", "oppose", "against"
- **Threshold**: 40% of zap votes blocks proposal
- **Independent**: Zap veto independent of participation votes

**Code**: ```67:73:blvm-commons/src/governance/vote_aggregator.rs```

### Abstain

Neutral vote:

- **Message Keywords**: "abstain", "neutral"
- **Weight**: Counted but doesn't affect threshold
- **Purpose**: Express neutrality without blocking

**Code**: ```25:49:blvm-commons/src/nostr/zap_voting.rs```

## Vote Processing

### Zap Vote Processing

1. **Receive Zap**: Zap contribution received via Nostr
2. **Check Proposal Zap**: Verify zap is for governance event
3. **Calculate Weight**: Weight = sqrt(amount_btc)
4. **Parse Vote Type**: Extract from zap message
5. **Check Duplicate**: Prevent duplicate votes
6. **Record Vote**: Store in database

**Code**: ```62:154:blvm-commons/src/nostr/zap_voting.rs```

### Vote Aggregation

Votes are aggregated for proposals:

1. **Get Zap Votes**: All zap votes for proposal
2. **Get Participation Votes**: Participation-based votes
3. **Combine Totals**: Sum support, veto, abstain weights
4. **Check Threshold**: Verify threshold met
5. **Check Veto**: Verify no veto blocking

**Code**: ```32:95:blvm-commons/src/governance/vote_aggregator.rs```

## Privacy Features

### Pseudonymous Voting

Votes are linked to Nostr pubkeys, not real identities:

- **Pubkey-Based**: Votes tracked by sender pubkey
- **No KYC**: No identity verification required
- **Privacy**: Real identity not revealed

### Quadratic Voting

Quadratic formula prevents vote buying:

- **Square Root**: Vote weight = sqrt(contribution)
- **Diminishing Returns**: Large contributions have proportionally less weight
- **Fairness**: Prevents wealthy contributors from dominating

**Code**: ```61:63:blvm-commons/src/governance/weight_calculator.rs```

### Cooling-Off Period

New contributions have reduced weight:

- **Age Check**: Contributions must be old enough
- **Reduced Weight**: New contributions use participation weight only
- **Prevents Gaming**: Prevents last-minute contribution manipulation

**Code**: ```73:80:blvm-commons/src/governance/weight_calculator.rs```

## Vote Aggregation

### Vote Totals

```rust
pub struct VoteTotals {
    pub support_weight: f64,
    pub veto_weight: f64,
    pub abstain_weight: f64,
    pub total_weight: f64,
    pub support_count: u32,
    pub veto_count: u32,
    pub abstain_count: u32,
    pub total_count: u32,
}
```

**Code**: ```281:292:blvm-commons/src/nostr/zap_voting.rs```

### Proposal Vote Result

```rust
pub struct ProposalVoteResult {
    pub pr_id: i32,
    pub tier: u8,
    pub threshold: u32,
    pub total_votes: f64,
    pub support_votes: f64,
    pub veto_votes: f64,
    pub abstain_votes: f64,
    pub zap_vote_count: u32,
    pub participation_vote_count: u32,
    pub threshold_met: bool,
    pub veto_blocks: bool,
}
```

**Code**: ```32:95:blvm-commons/src/governance/vote_aggregator.rs```

## Veto Mechanisms

### Zap Veto

Zap votes can veto proposals:

- **Threshold**: 40% of zap votes must be veto
- **Independent**: Independent of participation votes
- **Blocking**: Veto blocks proposal approval

**Code**: ```67:73:blvm-commons/src/governance/vote_aggregator.rs```

### Economic Node Veto

Economic nodes can also veto (separate mechanism):

- **Threshold**: 30% hashpower OR 40% economic activity
- **Tier 3+**: Only for Tier 3+ proposals
- **Combined**: Works alongside zap veto

**Code**: ```57:75:blvm-commons/src/governance/vote_aggregator.rs```

## Database Schema

### Proposal Zap Votes Table

```sql
CREATE TABLE proposal_zap_votes (
    id INTEGER PRIMARY KEY,
    pr_id INTEGER NOT NULL,
    governance_event_id TEXT NOT NULL,
    sender_pubkey TEXT NOT NULL,
    amount_msat INTEGER NOT NULL,
    amount_btc REAL NOT NULL,
    vote_weight REAL NOT NULL,  -- sqrt(amount_btc)
    vote_type TEXT NOT NULL,    -- 'support', 'veto', 'abstain'
    timestamp DATETIME NOT NULL,
    verified BOOLEAN DEFAULT FALSE
);
```

**Code**: ```77:93:blvm-commons/src/database/migrations/005_governance_contributions.sql```

## Integration with Nostr

### Zap Tracking

Zaps are tracked via Nostr integration:

- **Zap Tracker**: Monitors Nostr zaps
- **Event Filtering**: Filters zaps to governance events
- **Vote Conversion**: Converts zaps to votes

**Code**: ```1:281:blvm-commons/src/nostr/zap_tracker.rs```

### Governance Events

Governance events on Nostr:

- **Event IDs**: Unique identifiers for proposals
- **Zap Targets**: Zaps to event IDs become votes
- **Real-Time**: Votes processed in real-time

## Benefits

1. **Privacy**: Pseudonymous voting via Nostr pubkeys
2. **Fairness**: Quadratic voting prevents vote buying
3. **Accessibility**: Anyone can vote via Lightning zaps
4. **Transparency**: All votes recorded on-chain/off-chain
5. **Resilience**: No single point of failure

## Components

The privacy-preserving voting system includes:
- Zap-to-vote processor
- Vote weight calculator (quadratic formula)
- Vote aggregator
- Participation weight calculation
- Cooling-off period enforcement
- Veto mechanisms (zap and economic node)

**Location**: `blvm-commons/src/nostr/zap_voting.rs`, `blvm-commons/src/governance/weight_calculator.rs`, `blvm-commons/src/governance/vote_aggregator.rs`

