# Assurance

Consensus coverage runs from an Orange Paper sentence to a mainnet block. The figures are the locks. The rows say what a pass means.

![What locks the implementation](../images/charts/assurance-counts.svg)

Z3 checks the `#[spec_locked]` functions on the figure, including witness fixtures. The other rows are the body proofs, the mutation checks, the test functions, and the Lean proofs. Theorem 6.1.2, the subsidy rule, is proved in Lean for every natural number and in Rust for the heights the tool checks.

## Where the attributes sit

![Spec-lock attributes by area](../images/charts/consensus-coverage.svg)

The bars are the production `#[spec_locked]` attributes in `blvm-consensus`. Witness fixtures are included in the figure's total.

## Where the tests sit

![Consensus test functions](../images/charts/consensus-tests.svg)

Counted from `#[test]` and `#[tokio::test]`. The property tests include the Orange Paper property file, which compares results with the Orange Paper formulas. The fuzz harnesses on the first figure run beside this count.

## Specification

<div class="locks">
<section>
<p class="lock-name">Orange Paper</p>
<p>The sentence is the rule the other rows refer to.</p>
<p class="lock-where"><a href="https://github.com/BTCDecoded/blvm-spec-lock/blob/main/docs/sentence-inventory.tsv">sentence-inventory.tsv</a>.</p>
</section>
</div>

## Formal verification of the Rust

<div class="locks">
<section>
<p class="lock-name"><code>#[spec_locked]</code></p>
<p>The function carries an Orange Paper contract.</p>
<p class="lock-where"><code>cargo spec-lock coverage --format json</code>, field <code>by_section</code>. Section map: <a href="https://github.com/BTCDecoded/blvm-spec-lock/blob/main/SPEC_LOCK_COVERAGE.md">SPEC_LOCK_COVERAGE.md</a>.</p>
</section>
<section>
<p class="lock-name"><code>check-drift</code></p>
<p>Those contracts still parse against the spec.</p>
<p class="lock-where">The drift report from the command in <a href="formal-verification.html">Formal verification</a>.</p>
</section>
<section>
<p class="lock-name">Spec lock, Z3</p>
<p>Z3 discharged the contract. A <strong>Passed</strong> row is formal verification of that function.</p>
<p class="lock-where"><code>cargo spec-lock verify</code> JSON, one row per function.</p>
</section>
<section>
<p class="lock-name">Body proofs</p>
<p>The proof is tied to the function body. The functions are named in <a href="https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/VERIFICATION.md">VERIFICATION.md</a>.</p>
<ul class="lock-names">
<li><code>sigop_count_push_opcode</code></li>
<li><code>is_pay_to_script_hash</code></li>
<li><code>validate_supply_limit</code></li>
<li><code>is_witness_empty</code></li>
<li><code>is_witness_version_opcode</code></li>
<li><code>validate_taproot_script</code></li>
<li><code>validate_segwit_witness_structure</code></li>
<li><code>tx_has_nonempty_input_witness</code></li>
<li><code>script_bool_bytes</code></li>
<li><code>is_version_zero_witness_program</code></li>
<li><code>validate_taproot_script_path_with_leaf_version</code></li>
<li><code>locktime_types_match</code></li>
<li><code>tx_requires_witness_script_flags</code></li>
</ul>
</section>
<section>
<p class="lock-name">Mutation gate</p>
<p>A semantic edit makes Z3 report that the obligation no longer holds.</p>
<p class="lock-where">The functions in that same guide, and the tool's list in <a href="https://github.com/BTCDecoded/blvm-spec-lock/blob/main/docs/MUTATION_COVERAGE.md">MUTATION_COVERAGE.md</a>.</p>
</section>
</div>

## Formal verification of the spec model

<div class="locks">
<section>
<p class="lock-name">Lean</p>
<p>The theorems of the model in <code>blvm-spec/lean/</code> are marked in the sentence inventory. The subsidy theorem (6.1.2) is proved in Lean for every natural number, and in Rust for the heights the tool checks.</p>
<p class="lock-where"><a href="https://github.com/BTCDecoded/blvm-spec-lock/blob/main/docs/sentence-inventory.tsv">sentence-inventory.tsv</a>.</p>
</section>
</div>

## Tests in the crate

<div class="locks">
<section>
<p class="lock-name">Unit tests</p>
<p>The asserted case holds.</p>
<p class="lock-where"><code>cargo test</code> in <code>blvm-consensus</code>.</p>
</section>
<section>
<p class="lock-name">Property tests</p>
<p>The invariant holds on the generated inputs.</p>
<p class="lock-where"><a href="../development/property-based-testing.html">Property-based testing</a>, <code>tests/consensus_property_tests.rs</code>.</p>
</section>
<section>
<p class="lock-name">Fuzz</p>
<p>The harness accepts the corpus and the generated inputs it has run.</p>
<p class="lock-where"><code>[[bin]]</code> names in <a href="https://github.com/BTCDecoded/blvm-consensus/blob/main/fuzz/Cargo.toml">blvm-consensus/fuzz/Cargo.toml</a>: transaction and block validation, script, proof of work, subsidy, serialization, sighash, ECDSA and Schnorr, locktime, sigops, witness, taproot, BIP 34, 54, 66, 90, 113, 119, and 147, plus <code>offchain_class</code>.</p>
</section>
<section>
<p class="lock-name">MIRI</p>
<p>The selected tests run without undefined behavior.</p>
<p class="lock-where"><a href="../development/testing.html#miri-integration">Testing</a>.</p>
</section>
<section>
<p class="lock-name">Internal differential fuzz</p>
<p>A serialize/deserialize round-trip inside this crate agrees with itself.</p>
<p class="lock-where"><code>differential_fuzzing</code> in the same <code>fuzz/Cargo.toml</code>.</p>
</section>
</div>

## Tests against Bitcoin Core

<div class="locks">
<section>
<p class="lock-name">Core transaction vectors</p>
<p>BLVM accepts <code>tx_valid.json</code> and rejects <code>tx_invalid.json</code>.</p>
<p class="lock-where"><a href="https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/core_test_vectors/README.md">core_test_vectors/README.md</a>, run from <code>transaction_tests.rs</code>.</p>
</section>
<section>
<p class="lock-name">Activation-height scripts</p>
<p>The script verdict matches <code>libbitcoinconsensus</code> at the height before, on, and after each activation.</p>
<p class="lock-where"><a href="https://github.com/BTCDecoded/blvm-consensus/blob/main/tests/height_script_differential.rs">height_script_differential.rs</a>.</p>
</section>
<section>
<p class="lock-name">Per-input script bench</p>
<p>The script verdict matches <code>libbitcoinconsensus</code> when the prevout is known.</p>
<p class="lock-where"><code>blvm-bench</code> <code>script_validation.rs</code>.</p>
</section>
<section>
<p class="lock-name">Regtest BIP comparison</p>
<p>Accept and reject match a Core node over RPC for BIP30, BIP34, BIP90, and a valid block.</p>
<p class="lock-where"><a href="../development/differential-testing.html">Differential testing</a>, <code>blvm-bench</code> <code>tests/integration.rs</code>.</p>
</section>
<section>
<p class="lock-name">Historical replay</p>
<p>BLVM's result matches Core on the mainnet blocks in the chosen height range.</p>
<p class="lock-where"><code>test_historical_blocks_differential</code>.</p>
</section>
<section>
<p class="lock-name">Full-chain phase 1</p>
<p>BLVM accepts every non-coinbase script on the canonical mainnet chain Core already accepted.</p>
<p class="lock-where"><a href="https://github.com/BTCDecoded/blvm-bench/blob/main/docs/FULL_CHAIN_DIFFERENTIAL.md">FULL_CHAIN_DIFFERENTIAL.md</a>, <code>sort_merge_test</code> step 6.</p>
</section>
<section>
<p class="lock-name">Full-chain phase 2</p>
<p><code>connect_block</code> matches <code>libbitcoinkernel</code> <code>process_block</code> on block connection.</p>
<p class="lock-where">The same note, <code>block_kernel_diff</code>.</p>
</section>
</div>

Phase 1 is the script comparison. Phase 2 is the block-connection comparison. The records are on the [differential testing](../development/differential-testing.md) page.

## What runs them

Consensus CI runs `cargo test --all-features`, then `check-drift`, then `verify`. The workflow is [blvm-consensus CI](https://github.com/BTCDecoded/blvm-consensus/blob/main/.github/workflows/ci.yml). Commands and the Z3 timeout are on [Formal verification](formal-verification.md).
