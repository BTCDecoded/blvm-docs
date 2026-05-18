use std::collections::HashMap;

use anyhow::{bail, Context, Result};
use serde_yaml::Value;

use crate::scalar_to_string;

const LAYER_YAML_KEYS: [&str; 5] = [
    "layer_1_constitutional",
    "layer_2_constitutional",
    "layer_3_implementation",
    "layer_4_application",
    "layer_5_extension",
];

const TIER_YAML_KEYS: [&str; 5] = [
    "tier_1_routine",
    "tier_2_features",
    "tier_3_consensus_adjacent",
    "tier_4_emergency",
    "tier_5_governance",
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SigThreshold {
    pub required: u64,
    pub total: u64,
}

#[derive(Debug, Clone)]
pub struct CombinedCell {
    pub signatures: String,
    pub review_days: u64,
    pub source: String,
}

#[derive(Debug, Clone)]
pub struct LayerTierPolicy {
    pub layers: [SigThreshold; 5],
    pub layer_review_days: [u64; 5],
    pub layer_consensus_review_days: [Option<u64>; 5],
    pub tiers: [SigThreshold; 5],
    pub tier_review_days: [u64; 5],
}

pub fn parse_layer_tier_policy(action: &Value, layers: &Value) -> Result<LayerTierPolicy> {
    let tiers_root = action
        .get("tiers")
        .context("action-tiers.yml missing tiers")?;
    let layers_root = layers
        .get("layers")
        .context("repository-layers.yml missing layers")?;

    let mut tier_sigs = [SigThreshold {
        required: 0,
        total: 0,
    }; 5];
    let mut tier_review_days = [0u64; 5];
    for (i, key) in TIER_YAML_KEYS.iter().enumerate() {
        let tier = tiers_root
            .get(*key)
            .with_context(|| format!("action-tiers.yml missing tiers.{key}"))?;
        tier_sigs[i] = parse_signatures(tier)?;
        tier_review_days[i] = parse_review_days(tier)?;
    }

    let mut layer_sigs = [SigThreshold {
        required: 0,
        total: 0,
    }; 5];
    let mut layer_review_days = [0u64; 5];
    let mut layer_consensus_review_days = [None; 5];
    for (i, key) in LAYER_YAML_KEYS.iter().enumerate() {
        let layer = layers_root
            .get(*key)
            .with_context(|| format!("repository-layers.yml missing layers.{key}"))?;
        layer_sigs[i] = parse_signatures(layer)?;
        layer_review_days[i] = parse_review_days(layer)?;
        layer_consensus_review_days[i] = layer
            .get("consensus_review_period_days")
            .map(|v| {
                scalar_to_string(v)?
                    .parse::<u64>()
                    .context("consensus_review_period_days not a number")
            })
            .transpose()?;
    }

    Ok(LayerTierPolicy {
        layers: layer_sigs,
        layer_review_days,
        layer_consensus_review_days,
        tiers: tier_sigs,
        tier_review_days,
    })
}

fn parse_signatures(node: &Value) -> Result<SigThreshold> {
    let sigs = node
        .get("signatures")
        .context("missing signatures block")?;
    let required = scalar_to_string(sigs.get("required").context("signatures.required")?)?
        .parse::<u64>()
        .context("signatures.required not a number")?;
    let total = scalar_to_string(sigs.get("total").context("signatures.total")?)?
        .parse::<u64>()
        .context("signatures.total not a number")?;
    Ok(SigThreshold { required, total })
}

fn parse_review_days(node: &Value) -> Result<u64> {
    scalar_to_string(
        node.get("review_period_days")
            .context("missing review_period_days")?,
    )?
    .parse::<u64>()
    .context("review_period_days not a number")
}

/// Same max-rule as `blvm-commons` `ThresholdValidator::get_combined_requirements`.
pub fn combine(layer: u8, tier: u8, policy: &LayerTierPolicy) -> Result<CombinedCell> {
    if !(1..=5).contains(&layer) || !(1..=5).contains(&tier) {
        bail!("layer and tier must be 1..=5, got layer={layer} tier={tier}");
    }
    let li = (layer - 1) as usize;
    let ti = (tier - 1) as usize;

    let layer_sig = policy.layers[li];
    let tier_sig = policy.tiers[ti];
    let sig_req = layer_sig.required.max(tier_sig.required);
    let sig_total = layer_sig.total.max(tier_sig.total);
    let review = policy.layer_review_days[li].max(policy.tier_review_days[ti]);

    let source = requirement_source(
        layer_sig.required,
        policy.layer_review_days[li],
        tier_sig.required,
        policy.tier_review_days[ti],
        layer,
        tier,
    );

    Ok(CombinedCell {
        signatures: format!("{sig_req}-of-{sig_total}"),
        review_days: review,
        source,
    })
}

/// Mirrors `ThresholdValidator::get_requirement_source`.
fn requirement_source(
    layer_sigs_req: u64,
    layer_review: u64,
    tier_sigs_req: u64,
    tier_review: u64,
    layer: u8,
    tier: u8,
) -> String {
    if layer_sigs_req >= tier_sigs_req && layer_review >= tier_review {
        format!("Layer {layer}")
    } else if tier_sigs_req >= layer_sigs_req && tier_review >= layer_review {
        format!("Tier {tier}")
    } else {
        format!("Combined Layer {layer} + Tier {tier}")
    }
}

pub fn render_combination_matrix_table(policy: &LayerTierPolicy) -> Result<String> {
    let mut lines = vec![
        "| Layer | Tier | Final Signatures | Final Review | Source |".to_string(),
        "|-------|------|------------------|--------------|---------|".to_string(),
    ];
    for layer in 1..=5u8 {
        for tier in 1..=5u8 {
            let cell = combine(layer, tier, policy)?;
            lines.push(format!(
                "| {layer} | {tier} | {} | {} days | {} |",
                cell.signatures, cell.review_days, cell.source
            ));
        }
    }
    Ok(lines.join("\n"))
}

pub fn insert_layer_tier_keys(
    map: &mut HashMap<String, String>,
    action: &Value,
    layers: &Value,
) -> Result<()> {
    let policy = parse_layer_tier_policy(action, layers)?;

    for n in 1..=5u8 {
        let i = (n - 1) as usize;
        map.insert(
            format!("layer_{n}_signatures"),
            format!(
                "{}-of-{}",
                policy.layers[i].required, policy.layers[i].total
            ),
        );
        map.insert(
            format!("layer_{n}_sig_required"),
            policy.layers[i].required.to_string(),
        );
        map.insert(
            format!("layer_{n}_sig_total"),
            policy.layers[i].total.to_string(),
        );
        map.insert(
            format!("layer_{n}_review_days"),
            policy.layer_review_days[i].to_string(),
        );
        if let Some(days) = policy.layer_consensus_review_days[i] {
            map.insert(format!("layer_{n}_consensus_review_days"), days.to_string());
        }
    }

    for n in 1..=5u8 {
        let i = (n - 1) as usize;
        map.insert(
            format!("tier_{n}_sig_required"),
            policy.tiers[i].required.to_string(),
        );
        map.insert(
            format!("tier_{n}_sig_total"),
            policy.tiers[i].total.to_string(),
        );
    }

    map.insert(
        "combination_matrix_table".to_string(),
        render_combination_matrix_table(&policy)?,
    );

    for layer in 1..=5u8 {
        for tier in 1..=5u8 {
            let cell = combine(layer, tier, &policy)?;
            let prefix = format!("matrix_{layer}_{tier}");
            map.insert(format!("{prefix}_signatures"), cell.signatures);
            map.insert(format!("{prefix}_review_days"), cell.review_days.to_string());
            map.insert(format!("{prefix}_source"), cell.source);
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    fn fixture_policy() -> LayerTierPolicy {
        let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/config");
        let action =
            serde_yaml::from_str(&std::fs::read_to_string(dir.join("action-tiers.yml")).unwrap())
                .unwrap();
        let layers = serde_yaml::from_str(
            &std::fs::read_to_string(dir.join("repository-layers.yml")).unwrap(),
        )
        .unwrap();
        parse_layer_tier_policy(&action, &layers).unwrap()
    }

    #[test]
    fn matrix_matches_threshold_rs_vectors() {
        let p = fixture_policy();
        let cases: [(u8, u8, &str, u64, &str); 8] = [
            (1, 1, "6-of-7", 180, "Layer 1"),
            (3, 1, "4-of-5", 90, "Layer 3"),
            (3, 3, "5-of-5", 90, "Tier 3"),
            (3, 5, "5-of-5", 180, "Tier 5"),
            (4, 2, "4-of-5", 60, "Combined Layer 4 + Tier 2"),
            (5, 1, "3-of-5", 14, "Combined Layer 5 + Tier 1"),
            (5, 2, "4-of-5", 30, "Tier 2"),
            (4, 4, "4-of-5", 60, "Combined Layer 4 + Tier 4"),
        ];
        for (layer, tier, sigs, days, source) in cases {
            let c = combine(layer, tier, &p).unwrap();
            assert_eq!(c.signatures, sigs, "L{layer} T{tier} sigs");
            assert_eq!(c.review_days, days, "L{layer} T{tier} days");
            assert_eq!(c.source, source, "L{layer} T{tier} source");
        }
    }

    #[test]
    fn layer_consensus_review_days_from_fixture() {
        let p = fixture_policy();
        assert_eq!(p.layer_consensus_review_days[0], Some(365));
        assert_eq!(p.layer_consensus_review_days[2], None);
    }
}
