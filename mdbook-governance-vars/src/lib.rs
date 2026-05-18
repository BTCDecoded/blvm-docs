use std::collections::HashMap;
use std::fs;
use std::path::Path;

use anyhow::{bail, Context, Result};
use mdbook::book::{Book, BookItem};
use mdbook::errors::Error as MdError;
use mdbook::preprocess::{Preprocessor, PreprocessorContext};
use regex::{Captures, Regex};
use serde_yaml::Value;
use std::sync::OnceLock;

mod combine;
mod drift_check;
mod threshold_ref;

const ACTION_TIERS: &str = "action-tiers.yml";
const REPOSITORY_LAYERS: &str = "repository-layers.yml";
const EMERGENCY_TIERS: &str = "emergency-tiers.yml";

fn placeholder_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\[\[gov:([a-z0-9_]+)\]\]").expect("placeholder regex"))
}

/// mdBook preprocessor name — must match `[preprocessor.governance-vars]` in `book.toml`.
pub struct GovVarsPreprocessor;

impl Preprocessor for GovVarsPreprocessor {
    fn name(&self) -> &str {
        "governance-vars"
    }

    fn run(&self, ctx: &PreprocessorContext, mut book: Book) -> Result<Book, MdError> {
        if std::env::var("MDBOOK_GOVERNANCE_VARS")
            .ok()
            .is_some_and(|v| v == "0" || v.eq_ignore_ascii_case("false"))
        {
            return Ok(book);
        }

        let config_dir = ctx.root.join("modules/governance/config");
        let replacements = build_replacements(&config_dir)
            .map_err(|e| MdError::msg(format!("governance-vars: {e:#}")))?;

        apply_to_chapters(&mut book.sections, &replacements)?;

        Ok(book)
    }
}

/// Load the three YAML files and build the allowlisted replacement map.
pub fn build_replacements(config_dir: &Path) -> Result<HashMap<String, String>> {
    let action = load_yaml(config_dir, ACTION_TIERS)?;
    let layers = load_yaml(config_dir, REPOSITORY_LAYERS)?;
    let emergency = load_yaml(config_dir, EMERGENCY_TIERS)?;

    let mut map = HashMap::new();

    const PR_TIERS: [(u8, &str); 5] = [
        (1, "tier_1_routine"),
        (2, "tier_2_features"),
        (3, "tier_3_consensus_adjacent"),
        (4, "tier_4_emergency"),
        (5, "tier_5_governance"),
    ];

    for (n, yaml_key) in PR_TIERS {
        let tier = action
            .get("tiers")
            .and_then(|t| t.get(yaml_key))
            .with_context(|| format!("action-tiers.yml missing tiers.{yaml_key}"))?;
        let review_days = scalar_to_string(
            tier.get("review_period_days")
                .with_context(|| format!("{yaml_key}.review_period_days"))?,
        )?;
        let signatures = format_signatures(tier)?;

        let prefix = format!("tier_{n}");
        map.insert(format!("{prefix}_review_days"), review_days.clone());
        map.insert(format!("{prefix}_signatures"), signatures);
        map.insert(format!("lifecycle_tier{n}_days"), review_days);
    }

    if let Some(tier) = action.get("tiers").and_then(|t| t.get("security_critical")) {
        map.insert(
            "security_critical_signatures".to_string(),
            format_signatures(tier)?,
        );
        map.insert(
            "security_critical_review_days".to_string(),
            scalar_to_string(
                tier.get("review_period_days")
                    .context("security_critical.review_period_days")?,
            )?,
        );
    }

    const EMERGENCY: [(&str, &str); 3] = [
        ("critical", "tier_1_critical"),
        ("urgent", "tier_2_urgent"),
        ("elevated", "tier_3_elevated"),
    ];

    for (slug, yaml_key) in EMERGENCY {
        let tier = emergency
            .get("tiers")
            .and_then(|t| t.get(yaml_key))
            .with_context(|| format!("emergency-tiers.yml missing tiers.{yaml_key}"))?;
        let req = tier
            .get("requirements")
            .with_context(|| format!("{yaml_key}.requirements"))?;

        let prefix = format!("emergency_{slug}");
        map.insert(
            format!("{prefix}_review_days"),
            scalar_to_string(
                req.get("review_period_days")
                    .with_context(|| format!("{yaml_key}.requirements.review_period_days"))?,
            )?,
        );
        map.insert(
            format!("{prefix}_signature"),
            scalar_to_string(
                req.get("signature_threshold")
                    .with_context(|| format!("{yaml_key}.requirements.signature_threshold"))?,
            )?,
        );
        map.insert(
            format!("{prefix}_activation"),
            scalar_to_string(
                req.get("activation_threshold")
                    .with_context(|| format!("{yaml_key}.requirements.activation_threshold"))?,
            )?,
        );
        map.insert(
            format!("{prefix}_max_days"),
            scalar_to_string(
                req.get("max_duration_days")
                    .with_context(|| format!("{yaml_key}.requirements.max_duration_days"))?,
            )?,
        );
    }

    combine::insert_layer_tier_keys(&mut map, &action, &layers)?;

    Ok(map)
}

/// Replace `[[gov:KEY]]` using `map`. Fails on unknown keys or leftover placeholders.
pub fn replace_content(content: &str, map: &HashMap<String, String>) -> Result<String> {
    let mut unknown = Vec::new();
    for caps in placeholder_re().captures_iter(content) {
        let key = caps.get(1).expect("capture group 1").as_str();
        if !map.contains_key(key) {
            unknown.push(key.to_string());
        }
    }
    if !unknown.is_empty() {
        unknown.sort();
        unknown.dedup();
        bail!("unknown [[gov:KEY]] placeholder(s): {}", unknown.join(", "));
    }

    let expanded = placeholder_re()
        .replace_all(content, |caps: &Captures| map[&caps[1]].as_str())
        .into_owned();

    if placeholder_re().is_match(&expanded) {
        bail!("unreplaced [[gov:…]] placeholder(s) remain after expansion");
    }

    Ok(expanded)
}

fn apply_to_chapters(items: &mut [BookItem], map: &HashMap<String, String>) -> Result<(), MdError> {
    for item in items {
        let BookItem::Chapter(chapter) = item else {
            continue;
        };
        let path = chapter
            .path
            .as_deref()
            .map(|p| p.display().to_string())
            .unwrap_or_else(|| "<unknown>".to_string());
        chapter.content = replace_content(&chapter.content, map).map_err(|e| {
            MdError::msg(format!("governance-vars in chapter {path}: {e:#}"))
        })?;
        apply_to_chapters(&mut chapter.sub_items, map)?;
    }
    Ok(())
}

pub(crate) fn load_yaml(config_dir: &Path, file: &str) -> Result<Value> {
    let path = config_dir.join(file);
    let raw = fs::read_to_string(&path)
        .with_context(|| format!("read {}", path.display()))?;
    serde_yaml::from_str(&raw).with_context(|| format!("parse {}", path.display()))
}

pub(crate) fn scalar_to_string(value: &Value) -> Result<String> {
    match value {
        Value::Number(n) => Ok(n.to_string()),
        Value::String(s) => Ok(s.clone()),
        Value::Bool(b) => Ok(b.to_string()),
        other => bail!("expected scalar, got {other:?}"),
    }
}

pub(crate) fn format_signatures(tier: &Value) -> Result<String> {
    let sigs = tier
        .get("signatures")
        .context("missing signatures block")?;
    let required = sigs
        .get("required")
        .context("signatures.required")?;
    let total = sigs.get("total").context("signatures.total")?;
    Ok(format!(
        "{}-of-{}",
        scalar_to_string(required)?,
        scalar_to_string(total)?
    ))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    fn fixture_config() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/config")
    }

    #[test]
    fn replacements_match_golden_tier1() {
        let map = build_replacements(&fixture_config()).unwrap();
        assert_eq!(map.get("tier_1_review_days").map(String::as_str), Some("7"));
        assert_eq!(map.get("tier_1_signatures").map(String::as_str), Some("3-of-5"));
        assert_eq!(map.get("lifecycle_tier1_days").map(String::as_str), Some("7"));
    }

    #[test]
    fn expand_chapter_snippet() {
        let map = build_replacements(&fixture_config()).unwrap();
        let input = "- **Tier 1**: [[gov:tier_1_review_days]] days\n";
        let out = replace_content(input, &map).unwrap();
        assert_eq!(out, "- **Tier 1**: 7 days\n");
    }

    #[test]
    fn emergency_replacements_from_fixtures() {
        let map = build_replacements(&fixture_config()).unwrap();
        assert_eq!(
            map.get("emergency_critical_signature").map(String::as_str),
            Some("4-of-7")
        );
        assert_eq!(
            map.get("emergency_urgent_max_days").map(String::as_str),
            Some("30")
        );
        assert_eq!(
            map.get("emergency_elevated_review_days").map(String::as_str),
            Some("30")
        );
    }

    #[test]
    fn expand_tier4_and_emergency_snippets() {
        let map = build_replacements(&fixture_config()).unwrap();
        let input = "\
**Governance Tier 4** remains **[[gov:tier_4_signatures]]** and **[[gov:tier_4_review_days]]-day** review.\n\
- **Activation**: [[gov:emergency_critical_activation]] emergency keyholders\n";
        let out = replace_content(input, &map).unwrap();
        assert!(out.contains("4-of-5"));
        assert!(out.contains("0-day"));
        assert!(out.contains("5-of-7 emergency keyholders"));
    }

    #[test]
    fn unknown_key_fails() {
        let map = HashMap::from([("tier_1_review_days".to_string(), "7".to_string())]);
        let err = replace_content("[[gov:not_a_real_key]]", &map).unwrap_err();
        assert!(
            err.to_string().contains("not_a_real_key"),
            "{err}"
        );
    }
}
