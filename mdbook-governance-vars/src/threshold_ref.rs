//! Hardcoded thresholds from `blvm-commons` `validation/threshold.rs` (merge enforcement).
//! Used only to detect **drift** between YAML-driven book output and runtime code until commons loads YAML.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SigThreshold {
    pub required: u64,
    pub total: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CombinedRef {
    pub signatures: SigThreshold,
    pub review_days: u64,
    pub source: &'static str,
}

pub fn layer_threshold(layer: u8) -> SigThreshold {
    match layer {
        1 | 2 => SigThreshold {
            required: 6,
            total: 7,
        },
        3 => SigThreshold {
            required: 4,
            total: 5,
        },
        4 => SigThreshold {
            required: 3,
            total: 5,
        },
        5 => SigThreshold {
            required: 2,
            total: 3,
        },
        _ => SigThreshold {
            required: 1,
            total: 1,
        },
    }
}

pub fn layer_review_days(layer: u8) -> u64 {
    match layer {
        1 | 2 => 180,
        3 => 90,
        4 => 60,
        5 => 14,
        _ => 30,
    }
}

pub fn tier_threshold(tier: u8) -> SigThreshold {
    match tier {
        1 => SigThreshold {
            required: 3,
            total: 5,
        },
        2 => SigThreshold {
            required: 4,
            total: 5,
        },
        3 | 5 => SigThreshold {
            required: 5,
            total: 5,
        },
        4 => SigThreshold {
            required: 4,
            total: 5,
        },
        _ => SigThreshold {
            required: 1,
            total: 1,
        },
    }
}

pub fn tier_review_days(tier: u8) -> u64 {
    match tier {
        1 => 7,
        2 => 30,
        3 => 90,
        4 => 0,
        5 => 180,
        _ => 30,
    }
}

fn requirement_source(
    layer_sigs_req: u64,
    layer_review: u64,
    tier_sigs_req: u64,
    tier_review: u64,
    layer: u8,
    tier: u8,
) -> &'static str {
    if layer_sigs_req >= tier_sigs_req && layer_review >= tier_review {
        match layer {
            1 => "Layer 1",
            2 => "Layer 2",
            3 => "Layer 3",
            4 => "Layer 4",
            5 => "Layer 5",
            _ => "Layer",
        }
    } else if tier_sigs_req >= layer_sigs_req && tier_review >= layer_review {
        match tier {
            1 => "Tier 1",
            2 => "Tier 2",
            3 => "Tier 3",
            4 => "Tier 4",
            5 => "Tier 5",
            _ => "Tier",
        }
    } else {
        "Combined"
    }
}

pub fn combined_ref(layer: u8, tier: u8) -> CombinedRef {
    let layer_sig = layer_threshold(layer);
    let tier_sig = tier_threshold(tier);
    let layer_review = layer_review_days(layer);
    let tier_review = tier_review_days(tier);

    let sig_req = layer_sig.required.max(tier_sig.required);
    let sig_total = layer_sig.total.max(tier_sig.total);
    let review = layer_review.max(tier_review);

    let source_tag = requirement_source(
        layer_sig.required,
        layer_review,
        tier_sig.required,
        tier_review,
        layer,
        tier,
    );

    CombinedRef {
        signatures: SigThreshold {
            required: sig_req,
            total: sig_total,
        },
        review_days: review,
        source: source_tag,
    }
}

pub fn combined_source_string(layer: u8, tier: u8) -> String {
    let layer_sig = layer_threshold(layer);
    let tier_sig = tier_threshold(tier);
    let layer_review = layer_review_days(layer);
    let tier_review = tier_review_days(tier);

    if layer_sig.required >= tier_sig.required && layer_review >= tier_review {
        format!("Layer {layer}")
    } else if tier_sig.required >= layer_sig.required && tier_review >= layer_review {
        format!("Tier {tier}")
    } else {
        format!("Combined Layer {layer} + Tier {tier}")
    }
}
