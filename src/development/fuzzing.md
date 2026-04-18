# Fuzzing

Coverage-guided fuzzing uses **libFuzzer** via **cargo-fuzz** on unstructured byte inputs. It complements spec-lock, unit tests, and property tests; it does not replace them.

## Source of truth

Harness names and crate wiring live in each repo’s **`fuzz/Cargo.toml`** (`[[bin]]` entries). Implementation sources are under **`fuzz/fuzz_targets/`**. Do not treat prose (here or in READMEs) as an inventory—it goes stale.

| Crate | Location |
|-------|----------|
| blvm-consensus | [`blvm-consensus/fuzz`](https://github.com/BTCDecoded/blvm-consensus/tree/main/fuzz) |
| blvm-node | [`blvm-node/fuzz`](https://github.com/BTCDecoded/blvm-node/tree/main/fuzz) |

## Quick start (consensus)

```bash
cd blvm-consensus/fuzz
./init_corpus.sh    # optional: seed corpora
cargo +nightly fuzz run <target_name>
```

Pick `<target_name>` from `fuzz/Cargo.toml`. The `fuzz/` directory also contains scripts (e.g. campaign runners, corpus helpers, sanitizer build helpers)—use what matches your workflow.

## CI

Fuzz jobs are defined in the relevant repository’s GitHub Actions. Matrix steps and timeouts may not exercise every harness on every run; read the workflow for actual behavior.

## See also

- [Testing](testing.md) — how techniques fit together  
- [Differential testing](differential-testing.md) — cross-implementation checks  
- [Formal verification](../consensus/formal-verification.md) — spec-lock scope  
