use std::path::Path;

use anyhow::{Context, Result};

use crate::combine::{combine, parse_layer_tier_policy};
use crate::load_yaml;
use crate::threshold_ref::{combined_ref, combined_source_string};

const ACTION_TIERS: &str = "action-tiers.yml";
const REPOSITORY_LAYERS: &str = "repository-layers.yml";

/// Returns a list of human-readable drift messages (empty = OK).
pub fn check_yaml_vs_threshold_rs(config_dir: &Path) -> Result<Vec<String>> {
    let action = load_yaml(config_dir, ACTION_TIERS)?;
    let layers = load_yaml(config_dir, REPOSITORY_LAYERS)?;
    let policy = parse_layer_tier_policy(&action, &layers)?;

    let mut drifts = Vec::new();

    for layer in 1..=5u8 {
        for tier in 1..=5u8 {
            let yaml_cell = combine(layer, tier, &policy)?;
            let rust_ref = combined_ref(layer, tier);
            let expected_source = combined_source_string(layer, tier);

            let yaml_sig = parse_sig_pair(&yaml_cell.signatures)?;
            if yaml_sig != rust_ref.signatures {
                drifts.push(format!(
                    "L{layer} T{tier} signatures: YAML {} vs threshold.rs {}-of-{}",
                    yaml_cell.signatures, rust_ref.signatures.required, rust_ref.signatures.total
                ));
            }
            if yaml_cell.review_days != rust_ref.review_days {
                drifts.push(format!(
                    "L{layer} T{tier} review_days: YAML {} vs threshold.rs {}",
                    yaml_cell.review_days, rust_ref.review_days
                ));
            }
            if yaml_cell.source != expected_source {
                drifts.push(format!(
                    "L{layer} T{tier} source: YAML {:?} vs threshold.rs {:?}",
                    yaml_cell.source, expected_source
                ));
            }
        }
    }

    Ok(drifts)
}

fn parse_sig_pair(s: &str) -> Result<crate::threshold_ref::SigThreshold> {
    let (req, total) = s
        .split_once("-of-")
        .with_context(|| format!("invalid signature format: {s}"))?;
    Ok(crate::threshold_ref::SigThreshold {
        required: req.parse()?,
        total: total.parse()?,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    #[test]
    fn fixtures_align_with_threshold_rs() {
        let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/config");
        let drifts = check_yaml_vs_threshold_rs(&dir).unwrap();
        assert!(
            drifts.is_empty(),
            "YAML/threshold.rs drift:\n{}",
            drifts.join("\n")
        );
    }

    #[test]
    fn workspace_governance_aligns_with_threshold_rs_if_present() {
        let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../modules/governance/config");
        if !dir.join("action-tiers.yml").exists() {
            let alt = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../../governance/config");
            if alt.join("action-tiers.yml").exists() {
                let drifts = check_yaml_vs_threshold_rs(&alt).unwrap();
                assert!(drifts.is_empty(), "{}", drifts.join("\n"));
            }
            return;
        }
        let drifts = check_yaml_vs_threshold_rs(&dir).unwrap();
        assert!(drifts.is_empty(), "{}", drifts.join("\n"));
    }
}
