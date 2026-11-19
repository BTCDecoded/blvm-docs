# Governance configuration

> On current `blvm-commons` `main`, YAML loads through **`src/config/loader.rs`** (`GovernanceConfigFiles` and related types). Older doc links to `src/governance/config_registry.rs`, `config_reader.rs`, `yaml_loader.rs`, and similar files **do not exist** in that form; use **loader.rs** and the **[governance](https://github.com/BTCDecoded/governance) repo** `config/` tree as the live references.

## Overview

The Bitcoin Commons configuration system exposes governance-controlled parameters through typed YAML. **YAML files are the source of truth**, with a database-backed registry for governed changes and a fallback chain when files are missing.

Published policy tables in this book (for example [PR Process](../development/pr-process.md), [Layer-Tier Model](layer-tier-model.md)) use **`[[gov:KEY]]`** placeholders expanded at **`mdbook build`** from `modules/governance/config/*.yml` via **`mdbook-governance-vars`**. That keeps narrative docs aligned with YAML; **merge enforcement** in `blvm-commons` may still use hardcoded thresholds until runtime YAML loading is implemented.

## Architecture

The configuration system has three core components:

### 1. YAML Files (Source of Truth)

YAML configuration files in the `governance/config/` directory serve as the authoritative source for all configuration defaults. These files are version-controlled and human-readable.

**Key Files:**
- `action-tiers.yml` - PR action tier definitions (see [action tiers](https://github.com/BTCDecoded/governance/blob/main/docs/ACTION_TIERS.md))
- `repository-layers.yml` - Layer definitions and requirements
- `emergency-tiers.yml` - Emergency response classes (**separate** from action tiers)
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


### 3. ConfigReader (Unified Interface)

The `ConfigReader` provides a type-safe interface for reading configuration values with caching and fallback support.

**Features:**
- Type-safe accessors (`get_i32()`, `get_f64()`, `get_bool()`, `get_string()`)
- In-memory caching (5-minute TTL)
- Automatic cache invalidation on changes
- Fallback chain support


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

**Implementation**: See `src/config/loader.rs` in **blvm-commons**

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


### sync_to_yaml()

When governance-approved changes are activated, the system can write changes back to YAML files. Full bidirectional sync is planned.


## Configuration Categories

Configuration parameters are organized into categories:

- **FeatureFlags**: Feature toggles (e.g., `feature_governance_enforcement`)
- **Thresholds**: Maintainer signature thresholds (e.g., `tier_3_signatures_required`)
- **TimeWindows**: Review periods and time limits (e.g., `tier_3_review_period_days`)
- **Limits**: Size and count limits (e.g., `max_pr_size_bytes`)
- **Network**: Network-related parameters
- **Security**: Security-related parameters
- **Other**: Miscellaneous parameters

## Forkable variables

The values live in the governance repository under `config/` (YAML) and `ruleset-export-template*.y`. This page does not copy them. `repository-layers.yml` is [[gov:layer_1_signatures]] and [[gov:layer_1_review_days]] days. The schedules the book draws are on [Governance model](governance-model.md). Emergency classes are on [PR process](../development/pr-process.md#emergency-procedures). What the process loads is `blvm-commons/src/config/loader.rs`.

## Governance Change Workflow

Changing a configuration parameter requires Tier 5 governance approval:

1. **Proposal**: Create a configuration change proposal via PR
2. **Review**: [[gov:tier_5_signatures]] maintainer signatures required
3. **Review Period**: [[gov:tier_5_review_days]] days review period
4. **Activation**: Change activated in database via `activate_change()`
5. **Sync**: Change optionally synced back to YAML files


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
let enabled = config.get_bool("feature_governance_enforcement", false).await?;
```

### Convenience Methods

```rust
// Get tier signatures
let (required, total) = config.get_tier_signatures(3).await?;

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


## YAML Structure

YAML files use a structured format. Example from `action-tiers.yml`:

```yaml
tiers:
 - tier: 1
 name: "Routine Maintenance"
 signatures_required: 3
 signatures_total: 5
 review_period_days: 7
 - tier: 3
 name: "Consensus-Adjacent"
 signatures_required: 5
 signatures_total: 5
 review_period_days: 90
```

The `YamlConfigLoader` extracts values from these files into a flat key-value structure for the registry.


## Initialization

On system startup:

1. **Load YAML Files**: System loads YAML configuration files
2. **Sync to Database**: `sync_from_yaml()` populates database from YAML
3. **Initialize Defaults**: `initialize_governance_defaults()` registers any missing configs
4. **Create ConfigReader**: ConfigReader created with YAML loader for fallback access


## Configuration Key Reference

All configuration keys follow a naming convention:

- Tier configs: `tier_{n}_{property}`
- Layer configs: `layer_{n}_{property}`

See the governance repo `config/` tree for the live key set.

## Source

- [config/loader.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/config/loader.rs)
- [main.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/main.rs)

