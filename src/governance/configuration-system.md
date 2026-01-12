# Configuration System

## Overview

The Bitcoin Commons configuration system provides a unified, type-safe interface for all governance-controlled parameters. The system uses **YAML files as the source of truth** with a database-backed registry for governance-controlled changes and a comprehensive fallback chain.

## Architecture

The configuration system has three core components:

### 1. YAML Files (Source of Truth)

YAML configuration files in the `governance/config/` directory serve as the authoritative source for all configuration defaults. These files are version-controlled and human-readable.

**Key Files:**
- `action-tiers.yml` - Tier definitions and signature requirements
- `repository-layers.yml` - Layer definitions and requirements
- `economic-nodes.yml` - Economic node configuration
- `emergency-tiers.yml` - Emergency tier definitions
- `commons-contributor-thresholds.yml` - Commons contributor thresholds
- `governance-fork.yml` - Governance fork configuration
- `maintainers/*.yml` - Maintainer configurations by layer
- `repos/*.yml` - Repository-specific configurations

### 2. ConfigRegistry (Database-Backed)

The `ConfigRegistry` stores all governance-controlled configuration parameters in a database, enabling governance-approved changes without modifying YAML files directly.

**Features:**
- Stores 87+ forkable governance variables
- Tracks change proposals and approvals
- Requires Tier 5 governance to modify
- Complete audit trail of all changes
- Automatic sync from YAML on startup

**Code**: ```1:100:blvm-commons/src/governance/config_registry.rs```

### 3. ConfigReader (Unified Interface)

The `ConfigReader` provides a type-safe interface for reading configuration values with caching and fallback support.

**Features:**
- Type-safe accessors (`get_i32()`, `get_f64()`, `get_bool()`, `get_string()`)
- In-memory caching (5-minute TTL)
- Automatic cache invalidation on changes
- Fallback chain support

**Code**: ```1:100:blvm-commons/src/governance/config_reader.rs```

## Fallback Chain

The system uses a four-tier fallback chain for configuration values:

```
1. Cache (in-memory, 5-minute TTL)
   ↓ (if not found)
2. Config Registry (database, governance-controlled)
   ↓ (if not found)
3. YAML Config (file-based, source of truth)
   ↓ (if not found)
4. Hardcoded Defaults (safety fallback)
```

**Implementation**: ```76:110:blvm-commons/src/governance/config_reader.rs```

## Sync Mechanisms

### sync_from_yaml()

On startup, the system automatically syncs YAML values into the database:

```rust
config_registry.sync_from_yaml(config_path).await?;
```

This process:
1. Loads all YAML configuration files
2. Extracts configuration values using `YamlConfigLoader`
3. Compares with database values
4. Updates database if no governance history exists (preserves governance-approved changes)

**Code**: ```120:200:blvm-commons/src/governance/config_registry.rs```

### sync_to_yaml()

When governance-approved changes are activated, the system can write changes back to YAML files. Full bidirectional sync is planned.

**Code**: ```250:280:blvm-commons/src/governance/config_registry.rs```

## Configuration Categories

Configuration parameters are organized into categories:

- **FeatureFlags**: Feature toggles (e.g., `feature_governance_enforcement`)
- **Thresholds**: Signature and veto thresholds (e.g., `tier_3_signatures_required`)
- **TimeWindows**: Review periods and time limits (e.g., `tier_3_review_period_days`)
- **Limits**: Size and count limits (e.g., `max_pr_size_bytes`)
- **Network**: Network-related parameters
- **Security**: Security-related parameters
- **Other**: Miscellaneous parameters

## 87+ Forkable Variables

The system manages 87+ governance-controlled configuration variables, organized into categories:

### Complete Configuration Schema

| Category | Variables | Description |
|----------|-----------|-------------|
| **Action Tier Thresholds** | 15 | Signature requirements and review periods for each tier |
| **Economic Node Veto Thresholds** | 7 | Veto thresholds for Tier 3, 4, and Tier 5 signaling |
| **Commons Contributor Thresholds** | 8 | Qualification thresholds and weight calculation |
| **Governance Phase Thresholds** | 11 | Phase boundaries (Early, Growth, Mature) |
| **Repository Layer Thresholds** | 9 | Signature requirements per repository layer |
| **Emergency Tier Thresholds** | 10 | Emergency action thresholds and windows |
| **Governance Review Policy** | 10 | Review period policies and requirements |
| **Feature Flags** | 7 | Feature enable/disable flags |
| **Network & Security** | 3 | Network and security configuration |

**Total**: 87+ variables

**Code**: ```1:1055:blvm-commons/src/governance/config_defaults.rs```

### Action Tier Thresholds (15 variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `tier_1_signatures_required` | 3 | Tier 1: Required signatures (out of 5) |
| `tier_1_signatures_total` | 5 | Tier 1: Total signatures available |
| `tier_1_review_period_days` | 7 | Tier 1: Review period (days) |
| `tier_2_signatures_required` | 4 | Tier 2: Required signatures (out of 5) |
| `tier_2_signatures_total` | 5 | Tier 2: Total signatures available |
| `tier_2_review_period_days` | 30 | Tier 2: Review period (days) |
| `tier_3_signatures_required` | 5 | Tier 3: Required signatures (unanimous) |
| `tier_3_signatures_total` | 5 | Tier 3: Total signatures available |
| `tier_3_review_period_days` | 90 | Tier 3: Review period (days) |
| `tier_4_signatures_required` | 4 | Tier 4: Required signatures (emergency) |
| `tier_4_signatures_total` | 5 | Tier 4: Total signatures available |
| `tier_4_review_period_days` | 0 | Tier 4: Review period (immediate) |
| `tier_5_signatures_required` | 5 | Tier 5: Required signatures (governance) |
| `tier_5_signatures_total` | 5 | Tier 5: Total signatures available |
| `tier_5_review_period_days` | 180 | Tier 5: Review period (days) |

**Code**: ```216:357:blvm-commons/src/governance/config_defaults.rs```

### Economic Node Veto Thresholds (7 variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `veto_tier_3_mining_percent` | 30.0 | Tier 3: Mining hashpower threshold (%) |
| `veto_tier_3_economic_percent` | 40.0 | Tier 3: Economic activity threshold (%) |
| `veto_tier_4_mining_percent` | 25.0 | Tier 4: Mining hashpower threshold (%) |
| `veto_tier_4_economic_percent` | 35.0 | Tier 4: Economic activity threshold (%) |
| `veto_tier_4_window_hours` | 24 | Tier 4: Veto window (hours) |
| `signaling_tier_5_mining_percent` | 50.0 | Tier 5: Mining hashpower for support (%) |
| `signaling_tier_5_economic_percent` | 60.0 | Tier 5: Economic activity for support (%) |

**Code**: ```360:399:blvm-commons/src/governance/config_defaults.rs```

### Commons Contributor Thresholds (8 variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `commons_contributor_min_merge_mining_btc` | 0.01 | Minimum merge mining contribution (BTC) |
| `commons_contributor_min_fee_forwarding_btc` | 0.1 | Minimum fee forwarding contribution (BTC) |
| `commons_contributor_min_zaps_btc` | 0.01 | Minimum zap contribution (BTC) |
| `commons_contributor_min_marketplace_btc` | 0.01 | Minimum marketplace contribution (BTC) |
| `commons_contributor_measurement_period_days` | 90 | Measurement period (days) |
| `commons_contributor_qualification_logic` | "OR" | Qualification logic (OR/AND) |
| `commons_contributor_weight_formula` | "linear" | Weight calculation formula |
| `commons_contributor_weight_cap` | 0.10 | Maximum weight per contributor (10%) |

**Code**: ```400:500:blvm-commons/src/governance/config_defaults.rs```

### Governance Phase Thresholds (11 variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `phase_early_max_blocks` | 50000 | Early phase: Maximum blocks |
| `phase_early_max_nodes` | 10 | Early phase: Maximum economic nodes |
| `phase_early_max_contributors` | 10 | Early phase: Maximum contributors |
| `phase_growth_min_blocks` | 50000 | Growth phase: Minimum blocks |
| `phase_growth_max_blocks` | 200000 | Growth phase: Maximum blocks |
| `phase_growth_min_nodes` | 10 | Growth phase: Minimum economic nodes |
| `phase_growth_max_nodes` | 30 | Growth phase: Maximum economic nodes |
| `phase_growth_min_contributors` | 10 | Growth phase: Minimum contributors |
| `phase_growth_max_contributors` | 100 | Growth phase: Maximum contributors |
| `phase_mature_min_blocks` | 200000 | Mature phase: Minimum blocks |
| `phase_mature_min_nodes` | 30 | Mature phase: Minimum economic nodes |
| `phase_mature_min_contributors` | 100 | Mature phase: Minimum contributors |

**Code**: ```500:600:blvm-commons/src/governance/config_defaults.rs```

### Repository Layer Thresholds (9 variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `layer_1_2_signatures_required` | 3 | Layer 1-2: Required signatures |
| `layer_1_2_signatures_total` | 5 | Layer 1-2: Total signatures |
| `layer_1_2_review_period_days` | 7 | Layer 1-2: Review period (days) |
| `layer_3_signatures_required` | 4 | Layer 3: Required signatures |
| `layer_3_signatures_total` | 5 | Layer 3: Total signatures |
| `layer_3_review_period_days` | 30 | Layer 3: Review period (days) |
| `layer_4_signatures_required` | 5 | Layer 4: Required signatures |
| `layer_4_signatures_total` | 5 | Layer 4: Total signatures |
| `layer_4_review_period_days` | 90 | Layer 4: Review period (days) |
| `layer_5_signatures_required` | 5 | Layer 5: Required signatures |
| `layer_5_signatures_total` | 5 | Layer 5: Total signatures |
| `layer_5_review_period_days` | 180 | Layer 5: Review period (days) |

**Code**: ```600:700:blvm-commons/src/governance/config_defaults.rs```

### Complete Reference

For the complete list of all 87+ variables with descriptions and default values, see:
- **YAML Source**: `governance/config/FORKABLE_VARIABLES.md`
- **Default Values**: `governance/config/DEFAULT_VALUES_REFERENCE.md`
- **Implementation**: `blvm-commons/src/governance/config_defaults.rs`

## Governance Change Workflow

Changing a configuration parameter requires Tier 5 governance approval:

1. **Proposal**: Create a configuration change proposal via PR
2. **Review**: 5-of-5 maintainer signatures required
3. **Review Period**: 180 days review period
4. **Economic Node Signaling**: 50%+ hashpower, 60%+ economic activity
5. **Activation**: Change activated in database via `activate_change()`
6. **Sync**: Change optionally synced back to YAML files

**Code**: ```400:500:blvm-commons/src/governance/config_registry.rs```

## Usage Examples

### Basic Configuration Access

```rust
use crate::governance::config_reader::ConfigReader;
use crate::governance::config_registry::ConfigRegistry;
use std::sync::Arc;

// Initialize
let registry = Arc::new(ConfigRegistry::new(pool));
let yaml_loader = YamlConfigLoader::new(config_path);
let config = Arc::new(ConfigReader::with_yaml_loader(
    registry.clone(),
    Some(yaml_loader),
));

// Read a value (with fallback)
let review_period = config.get_i32("tier_3_review_period_days", 90).await?;
let veto_threshold = config.get_f64("veto_tier_3_mining_percent", 30.0).await?;
let enabled = config.get_bool("feature_governance_enforcement", false).await?;
```

### Convenience Methods

```rust
// Get tier signatures
let (required, total) = config.get_tier_signatures(3).await?;

// Get veto thresholds
let (mining, economic) = config.get_veto_thresholds(3).await?;

// Get Commons contributor threshold (with YAML fallback)
let threshold = config.get_commons_contributor_threshold("merge_mining").await?;
```

### Integration with Validators

```rust
// ThresholdValidator with config support
let validator = ThresholdValidator::with_config(config.clone());

// All methods use config registry
let (req, total) = validator.get_tier_threshold(3).await?;
```

## Caching Strategy

- **Cache TTL**: 5 minutes (configurable via `cache_ttl`)
- **Cache Invalidation**: 
  - Automatic after config changes are activated
  - Manual via `clear_cache()` or `invalidate_key()`
- **Cache Storage**: In-memory `HashMap<String, serde_json::Value>`

**Code**: ```76:120:blvm-commons/src/governance/config_reader.rs```

## YAML Structure

YAML files use a structured format. Example from `action-tiers.yml`:

```yaml
tiers:
  - tier: 1
    name: "Routine Maintenance"
    signatures_required: 3
    signatures_total: 5
    review_period_days: 7
    economic_veto: false
  - tier: 3
    name: "Consensus-Adjacent"
    signatures_required: 5
    signatures_total: 5
    review_period_days: 90
    economic_veto: true
```

The `YamlConfigLoader` extracts values from these files into a flat key-value structure for the registry.

**Code**: ```1:200:blvm-commons/src/governance/yaml_loader.rs```

## Initialization

On system startup:

1. **Load YAML Files**: System loads YAML configuration files
2. **Sync to Database**: `sync_from_yaml()` populates database from YAML
3. **Initialize Defaults**: `initialize_governance_defaults()` registers any missing configs
4. **Create ConfigReader**: ConfigReader created with YAML loader for fallback access

**Code**: ```365:410:blvm-commons/src/main.rs```

## Configuration Key Reference

All configuration keys follow a naming convention:

- Tier configs: `tier_{n}_{property}`
- Layer configs: `layer_{n}_{property}`
- Veto configs: `veto_tier_{n}_{type}_percent`
- Commons contributor: `commons_contributor_threshold_{type}`
- Economic node: `economic_node_{type}_{property}`

**Complete Reference**: See `governance/config/DEFAULT_VALUES_REFERENCE.md` for all keys and default values.

## Benefits

1. **YAML as Source of Truth**: Human-readable, version-controlled defaults
2. **Governance Control**: Database enables governance-approved changes without YAML edits
3. **Type Safety**: Type-safe accessors prevent configuration errors
4. **Performance**: Caching reduces database queries
5. **Flexibility**: Fallback chain ensures system always has valid configuration
6. **Audit Trail**: Complete history of all configuration changes

