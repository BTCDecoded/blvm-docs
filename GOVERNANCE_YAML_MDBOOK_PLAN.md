# Plan: Governance YAML to mdBook (narrow specification)

**Purpose:** Make [governance](https://github.com/BTCDecoded/governance) `config/*.yml` the **authoritative policy numbers** for **published** governance tables in [blvm-docs](https://github.com/BTCDecoded/blvm-docs), resolved at **`mdbook build`** so prose cannot drift from YAML.

**Non-goals (this epic):** Orange Paper templating; auto-editing `GOVERNANCE.md` / `README.md` bodies; replacing hardcoded logic in [blvm-commons](https://github.com/BTCDecoded/blvm-commons) (see §5—that is a **follow-up** unless explicitly scoped).

---

## 1. Frozen implementation choices (defaults)

Change these only with a deliberate ADR; otherwise implementation proceeds as below.

| Decision | Default |
|----------|---------|
| **Render mechanism** | **mdBook preprocessor (Rust)** in `blvm-docs`, crate path **`mdbook-governance-vars/`** (or `tools/mdbook-governance-vars/`). No pre-build generated `src/*.md` in MVP. |
| **mdBook ordering** | `[preprocessor.governance-vars]` with **`after = ["links"]`** so `{{#include}}` runs first (verify against pinned mdBook version). |
| **Placeholder syntax** | **`[[gov:KEY]]`** only: `KEY` is a **flat allowlist** entry (e.g. `tier_1_review_days`), not arbitrary dotted YAML paths in prose—mapping from key to YAML lives **only** in preprocessor code or a single `allowed_keys.toml` next to the crate. |
| **YAML read roots** | **`modules/governance/config/`** at build time. Files in MVP: **`action-tiers.yml`**, **`repository-layers.yml`**, **`emergency-tiers.yml`** (paths already verified in `deploy.yml`). |
| **Emergency policy source** | **Canonical for templating:** `config/emergency-tiers.yml`. **Do not** read the duplicate **`emergency_tiers`** block inside `config/action-tiers.yml` for the book until governance removes or syncs it (Phase 0 governance PR). |
| **CI mdBook** | Pin **`mdbook-version`** in `.github/workflows/deploy.yml` when the preprocessor merges (replace `latest`). |

---

## 2. Bespoke: this workspace

| Item | Detail |
|------|--------|
| **First book files** | `src/development/pr-process.md` only for **MVP**; then `src/governance/layer-tier-model.md`, `multisig-configuration.md`, `configuration-system.md`. |
| **Includes (unchanged in MVP)** | `src/governance/overview.md` to `modules/governance/README.md`; `src/governance/governance-model.md` to `modules/governance/GOVERNANCE.md`; Orange Paper include stays out of scope. |
| **CI today** | `blvm-docs/.github/workflows/deploy.yml`: **Fetch mdBook include sources**, **Verify book inputs** (three YAML files + Orange Paper + governance markdown). Extend verify with **`modules/governance/docs/templates/README.md`** when that path is required. |
| **PR CI** | Add **`pull_request`** job: same fetch + verify + `mdbook build` as deploy (no Pages). **Required before** merging wide template use. |

---

## 3. Current state (validated)

- **Governance:** `config/action-tiers.yml` (PR tiers plus embedded `emergency_tiers` duplicate), `config/repository-layers.yml`, `config/emergency-tiers.yml`, plus classification and per-repo YAML.
- **blvm-docs:** Most content in `src/`; three `{{#include}}` sites; deploy ensures governance clone and YAML files exist.
- **blvm-commons:** `src/validation/threshold.rs` implements `get_tier_threshold`, `get_threshold_for_layer`, `get_combined_requirements` with **hardcoded** integers that match YAML today—it does **not** load `action-tiers.yml` for those functions. Tests reference YAML on disk as fixtures. **Therefore:** templating the book from YAML improves **docs accuracy** but does **not** automatically fix Rust or YAML drift; track separately (§5).

---

## 4. Target layout (governance repo)

**Create (does not exist yet):**

```text
governance/docs/
  README.md                 # editors: what to change in YAML vs here
  templates/                # optional after MVP
```

**MVP path A (minimal):** placeholders live in **`blvm-docs/src/development/pr-process.md`** only; preprocessor loads YAML from `modules/governance/config/`; **no** `governance/docs/templates/` until a second PR.

**Path B (after MVP):** move repeated fragments into **`governance/docs/templates/*.md`** and `{{#include}}` them from blvm-docs; preprocessor still expands `[[gov:…]]` after include.

---

## 5. Third source of truth (code)—backlog

| Source | Role today |
|--------|------------|
| `governance/config/*.yml` | Human-edited policy; some tests load files. |
| `blvm-docs` | Narrative; risk of hand-copied numbers. |
| `blvm-commons` `validation/threshold.rs` | **Enforced** merge thresholds and review periods in code paths. |

**MVP:** book must match **YAML** only.

**Follow-up (separate issue):** (a) CI job diffing YAML-derived numbers against `threshold.rs`, or (b) loading YAML at runtime in commons, or (c) generating `threshold.rs` from YAML. Until then, any governance YAML change that should affect merges **must** still get a **blvm-commons** PR.

---

## 6. Placeholder contract (narrow)

1. **Pattern:** `[[gov:KEY]]` where `KEY` is in an allowlist (for example `tier_1_review_days`, `tier_4_signatures_required`, `layer_3_review_days`).
2. **Resolution:** preprocessor replaces with a string from merged YAML load (the three MVP files); missing key or unknown `KEY` → **stderr and exit 1**.
3. **Registry:** table `KEY` to YAML path lives in **`mdbook-governance-vars`** (`keys.rs` or `allowed_keys.toml`); optional duplicate list in `governance/docs/README.md` for non-Rust editors (Phase 2).
4. **Forbidden:** placeholders inside included Orange Paper (optional CI grep).
5. **Whitespace:** replace only the exact token; preserve surrounding Markdown newlines.
6. **Composite formatting:** allowlist values may be **derived** in code (for example format `tiers.tier_1_routine.signatures.{required,total}` as `3-of-5`)—still one `KEY` per insertion site.

---

## 7. CI and local (exact steps)

**Deploy and PR (same build block):**

1. `actions/checkout` plus submodules as today.
2. **Fetch mdBook include sources** (existing): ensure `modules/governance` with the three YAML files.
3. **Verify book inputs** (existing): extend when new required paths exist.
4. **Rust:** `actions/checkout` for `blvm-docs` should run **`dtolnay/rust-toolchain@stable`** (or repo MSRV) before `cargo install` so the preprocessor crate always builds.
5. **Install:** pinned **`mdbook-version`** (see §1); `cargo install --path mdbook-governance-vars` from repo root (or `cargo install --locked --path …` if the crate ships a lockfile).
6. **`mdbook build`** with `[preprocessor.governance-vars]` and `command = "mdbook-governance-vars"` (binary on `PATH` after install).
7. Existing HTML, CSS, and Mermaid post-steps unchanged.

**Caching (optional):** cache `~/.cargo/bin` and registry dir keyed on `Cargo.lock` hash for the preprocessor crate to keep CI fast.

**Local:** README: clone or symlink `modules/governance`, install mdBook + preprocessor, run `mdbook build`; preprocessor errors reference `KEY` and file path.

---

## 8. Phases (reduced)

| Phase | Deliverable | Done when |
|-------|-------------|-----------|
| **0** | Governance PR: treat **`emergency-tiers.yml`** as canonical for emergency tables; add comment or remove or sync duplicate `emergency_tiers` inside `action-tiers.yml`. Inventory **`[[gov:`** keys for MVP rows in `pr-process.md` only. | Merged in governance; key list agreed. |
| **1** | `blvm-docs`: crate `mdbook-governance-vars`, `book.toml` wiring, **one** working `[[gov:…]]` in `pr-process.md`, deploy plus **new PR workflow** green. | PR merged; site builds. |
| **2** | Replace all numeric policy fragments in **`pr-process.md`** that are covered by the three YAML files. | No hand-maintained duplicates for in-scope policy in that file. |
| **3** | Same for `layer-tier-model.md`, `multisig-configuration.md`, `configuration-system.md` (keys or includes). | Same criterion per file. |
| **4** | Optional: `governance/docs/templates/`; governance YAML lint; diff job vs `threshold.rs`. | Drift: `cargo test` in `mdbook-governance-vars`; templates still optional. |

---

## 9. Risks (short)

| Risk | Mitigation |
|------|------------|
| YAML versus Rust drift | §5 backlog plus release checklist until automated. |
| Unknown placeholder | Hard fail at build (§6). |
| mdBook upgrade | Pin version (§1). |

---

## 10. Exit criteria (epic close)

1. **PR CI** on blvm-docs runs full book build with preprocessor.
2. **`pr-process.md`** in-scope policy numbers come only from YAML via `[[gov:…]]` (Phase 2 complete for that file).
3. **Governance** duplicate emergency block resolved or single-sourced (Phase 0).
4. **Contributor docs** (README and appendices) state: do not hand-edit migrated numbers in blvm-docs.

---

## 11. Validated data gaps and edge cases

These were checked against **`blvm-docs/src/development/pr-process.md`** and **`governance/config/*.yml`** (workspace tree, 2026).

| Topic | Finding | Plan |
|-------|---------|------|
| **Tier 5 signatures in prose** | Book says *Special process (5-of-7 maintainers + 2-of-3 emergency keyholders)*. **`action-tiers.yml`** `tier_5_governance` has **`signatures: 5/5`** and **180 days** only—no 7-pool or 2-of-3 fields. | Phase 0 or governance follow-up: **extend YAML** (or a small `tier_5_special_process.md` include) **or** keep that **one sentence** hand-authored until policy is encoded. Do **not** invent `[[gov:…]]` keys for prose that has no YAML field. |
| **`action-tiers.yml` embedded `emergency_tiers`** | Uses keys `critical` / `urgent` / `elevated` with **numeric** `activation_threshold` / `activation_total` and **no** `4-of-7` maintainer string. **`emergency-tiers.yml`** uses `tiers.tier_1_critical` etc. with **`signature_threshold: 4-of-7`** strings under `requirements`. | Preprocessor reads **`emergency-tiers.yml` only** for emergency-class maintainer bullets; Phase 0 governance work dedupes or documents why both exist. |
| **Security-specific tiers** | `action-tiers.yml` includes `security_critical`, `cryptographic`, `security_enhancement` with their own thresholds—**not** summarized in `pr-process.md` today. | **Out of MVP** unless a doc page lists those numbers; add keys later if documented. |
| **Layer–tier combination matrix** | `layer-tier-model.md` matrix is **`max(layer, tier)`** logic—same as **`blvm-commons`** `get_combined_requirements`. Not a single flat YAML row per cell. | **Phase 3:** implement the same max rule **inside the preprocessor** (small pure-Rust module) **with unit tests** whose expected cells match `threshold.rs` today; optional Phase 4 CI compares output to `blvm-commons` test vectors. |
| **Consensus 365-day note** | Book: Layer 1–2 consensus changes → **365 days**. **`repository-layers.yml`** exposes `consensus_review_period_days: 365` on layers 1–2. | Add allowlist keys or one derived sentence key when that line is templated (Phase 3). |

---

## 12. Initial allowlist sketch (Phase 0 → Phase 2)

**Convention:** `tier_N_*` from `action-tiers.yml` `tiers.tier_N_*` (PR tiers **1–5** only for MVP). `layer_N_*` from `repository-layers.yml` `layers.layer_N_*`. `emergency_*` from `emergency-tiers.yml` `tiers.tier_*`.

| `KEY` (example) | Source path (logical) | Typical rendered output |
|-----------------|----------------------|---------------------------|
| `tier_1_review_days` | `tiers.tier_1_routine.review_period_days` | `7` |
| `tier_1_signatures` | format from `signatures.required` / `total` | `3-of-5` |
| `tier_2_review_days` | `tiers.tier_2_features.review_period_days` | `30` |
| `tier_2_signatures` | … | `4-of-5` |
| `tier_3_review_days` | `tiers.tier_3_consensus_adjacent.review_period_days` | `90` |
| `tier_3_signatures` | … | `5-of-5` |
| `tier_4_review_days` | `tiers.tier_4_emergency.review_period_days` | `0` |
| `tier_4_signatures` | … | `4-of-5` |
| `tier_5_review_days` | `tiers.tier_5_governance.review_period_days` | `180` |
| `tier_5_signatures` | … | `5-of-5` |
| `lifecycle_tier1_days` … `lifecycle_tier5_days` | same as tier review bullets at top of PR lifecycle | duplicates OK if clearer for editors |
| `emergency_critical_review_days` | `tiers.tier_1_critical.requirements.review_period_days` | `0` |
| `emergency_critical_signature` | `tiers.tier_1_critical.requirements.signature_threshold` | `4-of-7` |
| `emergency_critical_activation` | format `activation_threshold` / implied total **7** | `5-of-7` |
| `emergency_critical_max_days` | `requirements.max_duration_days` | `7` |
| (parallel keys for **urgent** / **elevated**) | `tier_2_urgent`, `tier_3_elevated` | … |

**Phase 0 deliverable:** freeze the exact **KEY** names and row coverage for `pr-process.md` in a short table in the governance PR or in `mdbook-governance-vars` README.

---

## 13. `mdbook-governance-vars` implementation contract

| Requirement | Detail |
|-------------|--------|
| **Crate type** | Rust binary named **`mdbook-governance-vars`**; depends on **`mdbook`** (matching CI pin), **`serde`**, **`serde_yaml`**, **`anyhow`** (or `thiserror`). |
| **Entry** | Implement mdBook’s **`Preprocessor`** trait; `run()` loads the three YAML files from **`context.root` / `modules/governance/config/`** (path join; fail if missing). |
| **Algorithm** | Walk every `BookItem::Chapter`; replace `[[gov:KEY]]` in `chapter.content` via allowlist map; second pass or assert **no** unreplaced `[[gov:`** substring remains** (catch typos). |
| **Errors** | `eprintln!` with chapter **path**, **`KEY`**, and reason; **`std::process::exit(1)`** on any failure (mdBook surfaces non-zero). |
| **Tests** | **`tests/fixtures/`** copy minimal YAML + sample `chapter.md`; assert expanded strings; golden tests for **tier 1–5** and **three emergency** rows. |
| **Repo layout** | Either **workspace member** under `blvm-docs` (if you convert to workspace `Cargo.toml`) or **standalone crate** in `mdbook-governance-vars/` with its own `Cargo.lock` committed for **`cargo install --locked`**. |

---

## 14. `book.toml` and workflow checklist

- [ ] Add **`[preprocessor.governance-vars]`** with `command = "mdbook-governance-vars"` and **`after = ["links"]`** (confirm key name against pinned mdBook release notes).
- [ ] Pin **`mdbook-version`** in **`peaceiris/actions-mdbook`** to the same major.minor used locally.
- [ ] After **Install mdBook**, add **Rust toolchain** + **`cargo install --path mdbook-governance-vars`** (or `--locked`).
- [ ] Ensure **`PATH`** includes `$HOME/.cargo/bin` before **`mdbook build`**.
- [ ] New **`.github/workflows/docs.yml`** (or extend **`deploy.yml`**) with **`on: pull_request`** for `paths: ['src/**', 'book.toml', 'mdbook-governance-vars/**', '.github/workflows/**']`—same fetch, verify, build, **no** Pages / deploy.
- [ ] Extend **Verify book inputs** when new committed paths are required.

---

## 15. PR workflow sketch (`pull_request`)

```yaml
jobs:
  build-book:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { submodules: recursive, fetch-depth: 0 }
      - uses: peaceiris/actions-mdbook@v1
        with: { mdbook-version: '0.4.x' }  # pin explicitly
      - uses: dtolnay/rust-toolchain@stable
      - name: Fetch include sources + verify inputs
        run: |  # paste or reuse same script block as deploy.yml
          …
      - name: Install governance-vars preprocessor
        run: cargo install --locked --path mdbook-governance-vars
      - name: mdbook build
        run: mdbook build
```

Adjust versions and path to match the chosen crate layout.

---

## 16. Rollback and flags

- **Rollback:** revert the `blvm-docs` PR that adds the preprocessor; remove `[preprocessor.*]` from `book.toml`; site builds without YAML expansion.
- **Feature flag:** optional env **`MDBOOK_GOVERNANCE_VARS=0`** handled inside the preprocessor to no-op (only if you need gradual rollout); default **on** in CI.

---

## 17. Definition of ready (start Phase 1 coding)

All must be true:

1. Phase **0** merged in **governance** (or explicit written decision to defer duplicate `emergency_tiers` removal with owner + date).
2. **Allowlist table** for `pr-process.md` agreed (§12).
3. **mdBook version** integer chosen and recorded in plan or ADR.
4. **Crate layout** chosen: workspace member vs standalone with lockfile.
5. **PR CI** workflow file name and `paths` filter agreed so unrelated edits do not always rebuild the book.

---

## 18. References

- [blvm-docs](https://github.com/BTCDecoded/blvm-docs) — `book.toml`, `.github/workflows/deploy.yml`
- [governance](https://github.com/BTCDecoded/governance) — `config/`
- [mdBook preprocessors](https://rust-lang.github.io/mdBook/for_developers/preprocessors.html)
- [blvm-commons threshold.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/threshold.rs) — hardcoded merge rules (§5)

---

## 19. Prioritized implementation order

Work **top to bottom**. Later rows assume earlier ones are done (or explicitly waived in writing per §17).

| Order | Item | Repo | Blocks |
|-------|------|------|--------|
| **1** | **Tier 5 prose decision** (extend `action-tiers.yml`, keep one hand sentence, or defer with owner+date) — §11 | governance (policy) + note in plan/ADR | **Waived:** special process in `GOVERNANCE.md` + `docs/ACTION_TIERS.md`; YAML row for review days only |
| **2** | **Emergency single-source:** comment + doc pointer, or remove/sync **`emergency_tiers`** inside `action-tiers.yml` vs **`emergency-tiers.yml`** — §11, Phase 0 | governance | **Done** (2026-05-18): duplicate block removed from `action-tiers.yml` |
| **3** | **Freeze MVP allowlist** (exact `KEY` names for `pr-process.md` only) — §12 | governance PR or `mdbook-governance-vars` README | **Done** in `mdbook-governance-vars/README.md` |
| **4** | **Pick mdBook version** + record in `deploy.yml` / ADR — §1, §17 | blvm-docs | Reproducible preprocessor |
| **5** | **Pick crate layout** (standalone `mdbook-governance-vars/` + committed `Cargo.lock` **recommended** for `cargo install --locked`) — §13, §17 | blvm-docs | CI install |
| **6** | **Scaffold preprocessor:** `Preprocessor` impl, load three YAMLs from `modules/governance/config/`, allowlist map, replace `[[gov:KEY]]`, fail on unknown or leftover `[[gov:` — §13 | blvm-docs | Everything below |
| **7** | **Unit tests** with fixture YAML + golden expanded markdown — §13 | blvm-docs | Safe refactors |
| **8** | **`book.toml`:** `[preprocessor.governance-vars]` + `after = ["links"]` — §14 | blvm-docs | Local + CI build |
| **9** | **One placeholder** in `src/development/pr-process.md` (smoke) — Phase 1 | blvm-docs | Proves end-to-end |
| **10** | **`deploy.yml`:** Rust toolchain + `cargo install --locked --path mdbook-governance-vars` + pin `mdbook-version` — §7, §14 | blvm-docs | Pages deploy |
| **11** | **`pull_request` workflow** (same fetch/verify/build, `paths` filter) — §15 | blvm-docs | Merge safety |
| **12** | **Phase 2:** replace remaining in-scope literals in **`pr-process.md`** with `[[gov:…]]` — §8 | blvm-docs | **Done** (incl. Pass 2: layer bullets, matrix example table) |
| **13** | **Contributor docs:** README + appendices — do not edit migrated numbers in blvm-docs — §10 | blvm-docs | **Done** (2026-05-18): README, CONTRIBUTING, contributing-docs |
| **14** | **Phase 3:** `layer-tier-model.md` (combine matrix: port max-rule + tests vs `threshold.rs`) — §8, §11 | blvm-docs | **Done** (2026-05-18): `combine.rs`, matrix table + layer/tier keys |
| **15** | **Phase 3:** `multisig-configuration.md`, `configuration-system.md` — §8 | blvm-docs | **Done** (2026-05-18): placeholders + ACTION_TIERS pointer |
| **16** | **Phase 4 optional:** `governance/docs/templates/`, YAML lint, drift CI vs `threshold.rs` — §4, §5 | governance / blvm-docs | **Partial:** `threshold_ref` + `drift_check` tests in CI; `scripts/verify-book-inputs.sh`; ADR `docs/GOVERNANCE_MDBOOK.md` |
| **17** | **Pass 3 / book-wide:** SDK, security, fork, `*_sig_*`, `security_critical_*` keys; `scripts/check-governance-literals.sh` in CI — §8 | blvm-docs | **Done** (2026-05-18): wired chapters templated; only Tier 5 special line exempt |

**Parallelism:** **1–3** (governance) can run in parallel with **4–7** (blvm-docs crate) once **Tier 5** and **emergency** decisions do not block allowlist naming—if they do, finish **1–2** before **3**.

**Fast path (minimum to “it works”):** **4 → 6 → 7 → 8 → 9 → 10** with **Tier 5** line left static and **emergency** reading only `emergency-tiers.yml`; defer **1–2** only with written waiver (§17).

---

*Copy §1, §5, §10–§17, §12, and §19 into a remote ADR (`governance` or `blvm-docs`) when execution starts.*
