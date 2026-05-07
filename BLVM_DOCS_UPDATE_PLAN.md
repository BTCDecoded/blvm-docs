# BLVM documentation update plan

**Status (2026-05-07):** Book updates for **P0–P2** (§3–§5) are **landed** in [`src/`](src/); `mdbook build` succeeded. Submodule rename (**§6**) and infra backlog (**§9**) remain.

**Location:** Repository root: [`BLVM_DOCS_UPDATE_PLAN.md`](BLVM_DOCS_UPDATE_PLAN.md) (this file)  
**Primary target:** published book sources in [`src/`](src/)  
**Secondary:** [`modules/blvm/`](modules/blvm/) (meta-repo submodule; naming drift)  
**Last revised:** 2026-05-07 (rationale precision + fact-check + implementation).

---

## 1. Goals

- Align **`blvm-docs/src/`** prose with **`blvm-consensus`**, **`blvm-protocol`**, **`blvm-node`**, and **`blvm-sdk`** as-implemented — described **timelessly** (no “recently”, “now ships”, changelog tone).
- Remove or qualify statements that contradict **`Cargo.toml`**, workflows, or code (P2P / transport narrative, lockfile policy, dependency posture, Stratum V2 integration story).
- Extend reference coverage where the stack has behavior the book omits (fuzz crate inventory, BIP155 addrv2, IBD resource pressure, nested multisig pointer).
- Track **meta-repo rename debt** (`bllvm` → `blvm` under `modules/blvm`) without blocking book-source fixes.

---

## 2. Validation performed (how this plan was checked)

| Check | Result |
|--------|--------|
| Grep `blvm-docs/src` for `Cargo.lock`, `V2 (planned)`, `BIP324`, `bllvm` | Targets map to §3 rows; **`bllvm`** absent from `src/`. |
| `rust-version` / `Cargo.toml` in **node** vs **consensus** | Snapshot: **consensus `rust-version`** and **node `rust-version`** differ — **book must not freeze one global MSRV**; send readers to **`rust-version` in the crate they edit** (**P2-2**, **§11**). |
| **`modules/blvm`** / `bllvm` | Heavy stale **`bllvm-*`** naming in submodule docs/scripts — §6 only. |
| **`mining-stratum-v2.md`** vs **`modules/stratum-v2.md`** | Tone mismatch on transport (TCP listener path vs generic QUIC/TLS benefits) — **P2-1**. |
| **`contributing-docs.md`** style vs **`utxo-commitments.md`** | Numbers (98%, ~500 GB) vs “no unsubstantiated numbers” — **P2-4**. |

**Re-run after book edits:**

```bash
rg -n 'Cargo\.lock|V2 \(planned\)|BIP324|bllvm' blvm-docs/src
rg -n 'bllvm' blvm-docs/modules/blvm --glob '*.md' | head
```

### 2.1 Assertion checklist (targets still present until fixed)

| ID | Predicate |
|----|-----------|
| P0-1 | `protocol/architecture.md` contains **Bitcoin V1, V2 (planned)**. |
| P0-2 | `development/ci-cd-workflows.md` advises committing **`Cargo.lock`** universally; cache-key text references **`Cargo.lock` hash**. |
| P0-3 | `development/fuzzing.md` lists only **consensus** + **node** fuzz crates. |

---

## 3. Priority P0 — incorrect or misleading (fix first)

| ID | Facts (precision) | Book action | Files |
|----|-------------------|-------------|--------|
| **P0-1** | **`protocol/architecture.md`** lumps **BitcoinV1-like network variants** with **“V2 (planned)”**, which overlaps confusingly with **Bitcoin P2P v2 / BIP324** (encryption) and internal transport refactors. **BIP324**-related code and **fuzz harnesses** exist in **`blvm-protocol`**; **default node P2P path** must not be asserted from the book without checking **node + protocol wiring**. | Replace with: **variants** (mainnet / testnet / regtest); **message serialization** vs **optional transports** (see [transport](src/node/transport-abstraction.md)); one **conditional** sentence on **encrypted P2P (BIP324)** (e.g. “optional / status in …”) — follow **§12**. Verify links (**`blvm-protocol/src/node_tcp.rs`**, etc.) before ship. | [`protocol/architecture.md`](src/protocol/architecture.md) |
| **P0-2** | **`blvm-consensus`**, **`blvm-protocol`**, **`blvm-sdk`**, **`blvm-node`** **gitignore** root **`Cargo.lock`**. **`blvm-node/CONTRIBUTING.md`** *text* says to keep **`Cargo.lock` committed**, but the file is **ignored and not tracked** in git in a typical clone — **documentation bug in `blvm-node`**, not only the book. Aggregated CI doc must not state one rule for all repos. | **Book:** “Lockfile policy is **per repository**; read that repo’s **`CONTRIBUTING.md`** and **`.github/workflows`**. Do not assume the root **`Cargo.lock`** is committed.” Adjust cache-key bullet: if no lockfile, keys may use **manifest / toolchain** inputs. **Optional upstream:** open **`blvm-node`** issue — align CONTRIBUTING with **`.gitignore`** or **track** `Cargo.lock`. | [`development/ci-cd-workflows.md`](src/development/ci-cd-workflows.md) |
| **P0-3** | **`blvm-protocol/fuzz`** and **`blvm-sdk/fuzz`** exist with **`fuzz/Cargo.toml`**; book table lists only consensus + node. **`blvm-protocol/fuzz/Cargo.toml`** documents **`[patch.crates-io]`** for local monorepo vs CI behavior. | Add two table rows + links; one sentence: local monorepo fuzz may **path-patch** sibling crates; **CI** may resolve **crates.io** only (no jargon “strip” in book body). | [`development/fuzzing.md`](src/development/fuzzing.md) |
| **P0-4** | Book claims **all** consensus deps are exact-pinned. **Reality:** **BLVM → BLVM** deps use **published ranges** in **`Cargo.toml`** (e.g. **`blvm-primitives = { version = ">=0.1, <1" }`**, **`blvm-spec-lock`** with **`>=0.1.3, <1`**). Many **non-BLVM** deps use **`=`** where the manifest says so; **`secp256k1`** is **`version = "0.28"`**, not **`=0.28.2`**. **`consensus/overview.md`** shows a **stale / wrong** TOML fragment (`secp256k1 = "=0.28.2"`). | **Principles for readers:** (1) **Version constraints** = what **`Cargo.toml`** declares (do not paraphrase as “all exact” or “semver within major” for **0.x**). (2) **`--locked`** = use the **lockfile for that build** when the project provides one; it does **not** mean “every repo commits `Cargo.lock`.” (3) **Remove or replace** the bad snippet: link to **[`blvm-consensus/Cargo.toml`](https://github.com/BTCDecoded/blvm-consensus/blob/main/Cargo.toml)** or show **2–3 real `=` lines** with “examples only”. | [`development/contributing.md`](src/development/contributing.md), [`consensus/overview.md`](src/consensus/overview.md), [`architecture/system-overview.md`](src/architecture/system-overview.md), [`architecture/component-relationships.md`](src/architecture/component-relationships.md), [`security/threat-models.md`](src/security/threat-models.md), optionally [`ci-cd-workflows.md`](src/development/ci-cd-workflows.md) |

---

## 4. Priority P1 — gaps and consistency

| ID | Facts (precision) | Book action | Files |
|----|-------------------|-------------|--------|
| **P1-1** | **`addrv2`** / **AddrV2** handling appears in **`blvm-node`** (e.g. **`protocol_adapter.rs`**, **`wire_dispatch.rs`**) and protocol wire; aligns with **BIP155** subject matter — cite BIP only after spot-checking code/spec comments. | Add **BIP155** under **Network Protocol BIPs** with file pointers. | [`reference/protocol-specifications.md`](src/reference/protocol-specifications.md) |
| **P1-2** | **`blvm-protocol/src/node_tcp.rs`** exists today; framing story should be explained without internal codenames (**§12**). | Short neutral subsection: TCP path + message handling; define terms before contrasting framing styles; link to **`src/`** paths (re-verify after refactors). | [`protocol/network-protocol.md`](src/protocol/network-protocol.md), optionally [`protocol/message-formats.md`](src/protocol/message-formats.md) |
| **P1-3** | **`ibd-protection.md`** covers **bandwidth** abuse; **node** development has focused on **queue / memory** pressure during aggressive IBD — internal names (**retire-lag**, **pending-ops**) are **not** stable public API. | Add **conceptual** section: sync can be **memory- and backlog-limited**, not only bandwidth; point to **`blvm-node` docs**, **config**, **RELEASE_NOTES** — not PR URLs. | [`node/ibd-protection.md`](src/node/ibd-protection.md) or new page + **`SUMMARY.md`** |
| **P1-4** | SDK documents **nested multisig**; governance chapter is threshold-only. | Short cross-link + one paragraph on hierarchical / team quorum uses. | [`governance/multisig-configuration.md`](src/governance/multisig-configuration.md) |
| **P1-5** | **`blvm-node/CONTRIBUTING.md`** (**CI parity**) already states **default-feature** CI vs heavier **`--all-features`** — it does **not** give a RAM GiB figure. **Aggregate [`development/contributing.md`](src/development/contributing.md)** lacks that caution for readers who never open the node repo. | Add bullet: **`--all-features`**, broad integration suites, or large **`cargo test`** graphs can be **CPU/RAM-heavy** — follow **each repo’s** **`CONTRIBUTING.md`** (**link `blvm-node` CONTRIBUTING**). **Do not** invent GiB in the book. | [`development/contributing.md`](src/development/contributing.md) |

---

## 5. Priority P2 — polish, style, release hygiene

| ID | Facts (precision) | Book action | Files |
|----|-------------------|-------------|--------|
| **P2-1** | Stratum **spec** mentions modern transports; **node** integrates **TCP TLV** listener + **`blvm-stratum-v2`** module per existing book pages. | Qualify module page: **which transport** depends on deployment; **default** path documented in mining chapter. | [`modules/stratum-v2.md`](src/modules/stratum-v2.md) |
| **P2-2** | MSRV differs by crate (**`rust-version`** field). | Single rule: **read `Cargo.toml` `rust-version` in the repo you build.** | [`development/contributing.md`](src/development/contributing.md) |
| **P2-3** | Install copy references **v0.1.0** artifacts; either still true or drift. | Prefer **generated** install content / **`releases/latest`**; maintain release checklist. | [`getting-started/installation.md`](src/getting-started/installation.md), [`install/install-content.json`](src/install/install-content.json) |
| **P2-4** | Large round numbers conflict with **`contributing-docs.md`** rule. | Rephrase as **order-of-magnitude illustration** or cite **published benchmark** with method. | [`consensus/utxo-commitments.md`](src/consensus/utxo-commitments.md) |
| **P2-5** | **`blvm-protocol`** still ships **`economic`** module (**parameters**); removed items are **specific wire / P2P surfaces**, not “economics” wholesale. README may need **wire inventory** sync only. | Upstream issue/PR: README vs **actual** `NetworkMessage` / extension set. | **External:** `blvm-protocol` repo |

---

## 6. Large separate effort — `blvm-docs/modules/blvm` (`bllvm` → `blvm`)

Submodule mixes **`bllvm-*`** names across docs, scripts, tests. **Out of scope** for mdBook narrative in §3–§5.

1. **Mechanical rename** (scripts + tests + docs) **or**  
2. **Banner** on submodule: “historical names; see `blvm` org for current crate names.”  
3. Avoid **partial** Markdown-only renames without scripts.

Coordinate with **`blvm` meta-repo** default branch if doing (1).

---

## 7. Execution order

1. **P0-1 … P0-4**  
2. **P1-1, P1-2**  
3. **P1-3, P1-4, P1-5**  
4. **P2**  
5. **§6 submodule** — maintainer sign-off

---

## 8. Out of scope

- **commons-website** / whitepaper HTML  
- Renaming fuzz targets in code  
- Full **Orange Paper** text ( **`blvm-spec`** include )

---

## 9. Backlog (not assigned to P0–P2)

- Book text: **economic-node** P2P commands — remove if still named after protocol changes.  
- **BIP324 enabled by default**: do not claim from fuzz targets alone (**`protocol_bip324_*`** in **`blvm-protocol/fuzz`**).  
- **REST / rpc-api** vs **hyper** body types — spot-check when touching API docs.  
- **`modules/blvm/DOCUMENTATION_ORGANIZATION.md`** — umbrella layout accuracy.  
- **`blvm-docs/.github/workflows/deploy.yml`**: **`mdbook-version: latest`** — consider pin for reproducibility.  
- **`blvm-docs/book/`** HTML if committed — stale vs `src/` policy.

---

## 10. Sign-off

- [ ] P0–P1 done; §2 greps clean for resolved items.  
- [ ] `mdbook test` (with **blvm-spec** + **governance** includes per [`appendices/contributing-docs.md`](src/appendices/contributing-docs.md)).  
- [ ] Published links valid.  
- [ ] Optional: **`blvm-node`** issue — **`Cargo.lock`** / **CONTRIBUTING** / **`.gitignore`** alignment.

---

## 11. What belongs in the **official book** vs elsewhere

| Tier | IDs | Rule |
|------|-----|------|
| **Timeless book** | P0-1, P0-4, P1-1, P1-2, P1-4, P2-1, P2-4 | Architecture, BIP reference, dependency **principles**, qualitative claims — no sprint language. |
| **Book, but generic** | P0-2, P0-3, P1-3, P1-5, P2-2 | Per-repo policy, “may be heavy”, “see CONTRIBUTING” — **no** universal lockfile rule, **no** invented GiB, **no** frozen MSRV string. |
| **Other venues** | P2-3 (release automation), P2-5 (upstream README), §6, §9 infra | Not reader-facing mdBook core. |

**Dependency principle (correct wording):** BLVM crates depend on each other via **version ranges declared in `Cargo.toml`** (often **pre-1.0** `>= …, <1`); that is **not** the same as “floating” or “unpinned” — and **not** “all `=` pins.” Third-party pins follow **each manifest**.

---

## 12. Wording guardrails (for implementers)

| Avoid in book | Use instead |
|----------------|-------------|
| “Retired v2 transport” (vague) | Describe **current** default paths; optional **BIP324** as **optional** / **see release notes**. |
| “TCP v1–style / framed” (slash overload) | Separate **TCP compatibility**, **QUIC/Iroh**, then **framing** with definitions. |
| “CI strip” | “CI may build without path patches; crates resolve from **crates.io**.” |
| “Semver within major” for **0.x** | “**As in `Cargo.toml`** for that crate.” |
| “F2”, bare “economic-node” | Neutral **wire** / **message** names or **code links**. |
| “Classic” messages | **Defined** terms (header, command, payload, frame — after reading sources). |
| PR URLs as spec | **RELEASE_NOTES**, **node `docs/`**, stable anchors. |

---

## 13. Workspace fact-check (audit snapshot)

**Workspace:** `/home/user/src/btc-commons` (2026-05-07). Re-run before execution.

| Statement | Verified |
|-----------|----------|
| P0-1 line in `protocol/architecture.md` | Yes |
| P0-2 `ci-cd-workflows.md` + multi-repo **`Cargo.lock` gitignore** | Yes |
| P0-3 **`blvm-protocol/fuzz`**, **`blvm-sdk/fuzz`** exist; book table incomplete | Yes |
| P0-4 **`blvm-primitives`** / **`blvm-spec-lock`** ranges; **`secp256k1`** not `=0.28.2`; overview snippet wrong | Yes |
| P1-1 **AddrV2** in **node** + protocol | Yes |
| P1-2 **`node_tcp.rs`** present | Yes |
| P1-5 **Node CONTRIBUTING** has **CI vs all-features**, **no GiB** | Yes |
| **Node** `Cargo.lock` **untracked**, **ignored**, CONTRIBUTING says “commit” | Yes (upstream inconsistency) |

**Conclusion:** Priority table **Facts** columns are the source of truth; §13 is an **audit trail** only.
