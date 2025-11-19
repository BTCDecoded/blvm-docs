# Phase 1 Verification Integration Plan

**Focus**: Formal Verification with Cross-Layer Checks & Test Vector Improvements

## Current State Analysis

### 1. Formal Verification Integration

**Existing Components:**
- ✅ `verification_check.rs` - Checks CI workflow status for Kani/Proptest
- ✅ `cross_layer_status.rs` - Has equivalence proof checking (but simulated)
- ✅ CI workflow `.github/workflows/verify.yml` - Runs Kani and Proptest
- ✅ Configuration `consensus-proof.yml` - Defines verification requirements

**Gap Identified:**
- `cross_layer_status.rs::check_equivalence_proofs()` uses simulation methods
- No integration between `verification_check.rs` and `cross_layer_status.rs`
- Equivalence proof status doesn't use actual CI verification results

### 2. Hardcoded Test Vectors

**Current Implementation:**
```rust
// governance-app/src/validation/equivalence_proof.rs:106
pub fn generate_consensus_test_vectors() -> Vec<EquivalenceTestVector> {
    // Hardcoded test vectors
}
```

**Issues:**
- Test vectors are hardcoded in code
- Don't reflect actual Orange Paper sections
- Don't match actual Consensus Proof test suite
- Can't be updated without code changes

## Phase 1 Recommendations

### Recommendation 1: Integrate Formal Verification with Cross-Layer Checks

**Goal**: Use actual CI verification results instead of simulation

**Implementation Plan:**

1. **Modify `check_equivalence_proofs()` to use CI results**
   - Replace simulation with actual `verification_check::check_verification_status()` call
   - Use CI workflow status to determine equivalence proof status
   - Map Kani/Proptest results to equivalence proof status

2. **Integration Points:**
   ```rust
   // In cross_layer_status.rs
   async fn check_equivalence_proofs(
       &mut self,
       owner: &str,
       repo: &str,
       changed_files: &[String],
   ) -> Result<EquivalenceProofStatus, GovernanceError> {
       // Check if this is a verification-required repo
       if repo == "bllvm-consensus" {
           // Use actual verification check
           let pr = self.github_client.get_pr(owner, repo, pr_number).await?;
           let verification_result = check_verification_status(
               &self.github_client,
               &pr
           ).await?;
           
           // Map verification result to equivalence proof status
           match verification_result {
               ValidationResult::Valid { .. } => {
                   // All tests passed
               }
               ValidationResult::Invalid { .. } => {
                   // Some tests failed
               }
               ValidationResult::Pending { .. } => {
                   // Verification still running
               }
               _ => {}
           }
       } else {
           // For non-verification repos, use existing logic
       }
   }
   ```

3. **Benefits:**
   - Real verification results instead of simulation
   - Consistent with actual CI status
   - No false positives/negatives
   - Phase 1 appropriate (uses existing CI infrastructure)

### Recommendation 2: Load Test Vectors from Configuration

**Goal**: Make test vectors configurable and maintainable

**Implementation Plan:**

1. **Create Test Vector Configuration Format**
   ```yaml
   # governance/config/test-vectors.yml
   test_vectors:
     - test_id: "block_validation_001"
       description: "Block header validation equivalence"
       orange_paper_section: "5.3 Block Validation"
       consensus_proof_test: "tests/block_validation.rs::test_block_header_validation"
       expected_result: "valid"
       proof_type: "BehavioralEquivalence"
       
     - test_id: "tx_validation_001"
       description: "Transaction signature validation equivalence"
       orange_paper_section: "5.1 Transaction Validation"
       consensus_proof_test: "tests/transaction_validation.rs::test_signature_validation"
       expected_result: "valid"
       proof_type: "SecurityEquivalence"
   ```

2. **Load Test Vectors from Config**
   ```rust
   // In equivalence_proof.rs
   impl EquivalenceProofValidator {
       pub fn load_test_vectors_from_config(
           config_path: &str
       ) -> Result<Vec<EquivalenceTestVector>, GovernanceError> {
           // Load YAML config
           // Parse into EquivalenceTestVector structs
           // Validate structure
       }
       
       // Keep generate_consensus_test_vectors() as fallback
       pub fn generate_consensus_test_vectors() -> Vec<EquivalenceTestVector> {
           // Fallback to hardcoded if config not available
       }
   }
   ```

3. **Generate Test Vectors from Actual Tests** (Future Enhancement)
   - Parse Consensus Proof test files to extract test cases
   - Map to Orange Paper sections automatically
   - Generate test vectors dynamically

4. **Benefits:**
   - Test vectors can be updated without code changes
   - Can be versioned and reviewed separately
   - Easier to maintain and extend
   - Phase 1 appropriate (configuration-based, not cryptographic)

### Recommendation 3: Enhanced Status Reporting

**Goal**: Provide detailed verification status in cross-layer checks

**Implementation Plan:**

1. **Enhance EquivalenceProofStatus with CI Details**
   ```rust
   pub struct EquivalenceProofStatus {
       pub status: StatusState,
       pub message: String,
       pub tests_run: usize,
       pub tests_passed: usize,
       pub tests_failed: Vec<String>,
       pub proof_verification: Option<String>,
       // NEW: Add CI verification details
       pub kani_status: Option<VerificationToolStatus>,
       pub proptest_status: Option<VerificationToolStatus>,
       pub workflow_url: Option<String>,
   }
   
   pub struct VerificationToolStatus {
       pub tool_name: String,
       pub status: StatusState,
       pub conclusion: Option<String>,
       pub check_run_url: Option<String>,
   }
   ```

2. **Populate from CI Results**
   - Extract Kani check run status
   - Extract Proptest check run status
   - Include workflow URL for detailed logs
   - Show which specific proofs/tests passed/failed

3. **Benefits:**
   - More informative status checks
   - Easier debugging when verification fails
   - Better visibility into verification process

## Implementation Steps

### Step 1: Integrate Verification Check (Priority: High)

**Files to Modify:**
- `governance-app/src/github/cross_layer_status.rs`
  - Replace `check_equivalence_proofs()` simulation with real CI check
  - Import `verification_check` module
  - Use `check_verification_status()` function

**Changes:**
```rust
// Add import
use crate::validation::verification_check::check_verification_status;
use crate::validation::verification_check::ValidationResult;

// Modify check_equivalence_proofs()
async fn check_equivalence_proofs(
    &mut self,
    owner: &str,
    repo: &str,
    changed_files: &[String],
) -> Result<EquivalenceProofStatus, GovernanceError> {
    // Check if verification is required for this repo
    if requires_verification(repo)? {
        // Get PR number from context (need to pass it in)
        // For now, we'll need to modify the function signature
        
        // Get actual verification status
        let pr = self.github_client.get_pr(owner, repo, pr_number).await?;
        let verification_result = check_verification_status(
            &self.github_client,
            &pr
        ).await?;
        
        // Map to EquivalenceProofStatus
        match verification_result {
            ValidationResult::Valid { message } => {
                Ok(EquivalenceProofStatus {
                    status: StatusState::Success,
                    message: format!("✅ Equivalence Proof: {}", message),
                    tests_run: 0, // TODO: Extract from CI
                    tests_passed: 0, // TODO: Extract from CI
                    tests_failed: vec![],
                    proof_verification: Some("CI verification passed".to_string()),
                })
            }
            ValidationResult::Invalid { message, blocking } => {
                Ok(EquivalenceProofStatus {
                    status: StatusState::Failure,
                    message: format!("❌ Equivalence Proof: {}", message),
                    tests_run: 0,
                    tests_passed: 0,
                    tests_failed: vec![message],
                    proof_verification: Some("CI verification failed".to_string()),
                })
            }
            ValidationResult::Pending { message } => {
                Ok(EquivalenceProofStatus {
                    status: StatusState::Pending,
                    message: format!("⏳ Equivalence Proof: {}", message),
                    tests_run: 0,
                    tests_passed: 0,
                    tests_failed: vec![],
                    proof_verification: None,
                })
            }
            _ => {
                // Not applicable
                Ok(EquivalenceProofStatus {
                    status: StatusState::Success,
                    message: "Equivalence proof not required for this repository".to_string(),
                    tests_run: 0,
                    tests_passed: 0,
                    tests_failed: vec![],
                    proof_verification: None,
                })
            }
        }
    } else {
        // Not a verification-required repo
        Ok(EquivalenceProofStatus {
            status: StatusState::Success,
            message: "Equivalence proof not required".to_string(),
            tests_run: 0,
            tests_passed: 0,
            tests_failed: vec![],
            proof_verification: None,
        })
    }
}
```

**Note**: Need to pass `pr_number` to `check_equivalence_proofs()` - modify function signature.

### Step 2: Load Test Vectors from Config (Priority: Medium)

**Files to Create:**
- `governance/config/test-vectors.yml` - Test vector configuration

**Files to Modify:**
- `governance-app/src/validation/equivalence_proof.rs`
  - Add `load_test_vectors_from_config()` function
  - Modify `load_test_vectors()` to try config first, fallback to hardcoded

**Changes:**
```rust
impl EquivalenceProofValidator {
    pub fn load_test_vectors_from_config(
        config_path: &str
    ) -> Result<Vec<EquivalenceTestVector>, GovernanceError> {
        use std::fs;
        use serde_yaml;
        
        let content = fs::read_to_string(config_path)
            .map_err(|e| GovernanceError::ValidationError(
                format!("Failed to read test vector config: {}", e)
            ))?;
        
        #[derive(Deserialize)]
        struct TestVectorConfig {
            test_vectors: Vec<TestVectorConfigEntry>,
        }
        
        #[derive(Deserialize)]
        struct TestVectorConfigEntry {
            test_id: String,
            description: String,
            orange_paper_section: String,
            consensus_proof_test: Option<String>,
            expected_result: String,
            proof_type: String,
        }
        
        let config: TestVectorConfig = serde_yaml::from_str(&content)
            .map_err(|e| GovernanceError::ValidationError(
                format!("Failed to parse test vector config: {}", e)
            ))?;
        
        let mut vectors = Vec::new();
        for entry in config.test_vectors {
            vectors.push(EquivalenceTestVector {
                test_id: entry.test_id,
                description: entry.description,
                orange_paper_spec: entry.orange_paper_section,
                consensus_proof_impl: entry.consensus_proof_test
                    .unwrap_or_else(|| "N/A".to_string()),
                expected_result: entry.expected_result,
                test_data: HashMap::new(), // Can be populated from config if needed
                proof_metadata: ProofMetadata {
                    proof_type: match entry.proof_type.as_str() {
                        "BehavioralEquivalence" => ProofType::BehavioralEquivalence,
                        "SecurityEquivalence" => ProofType::SecurityEquivalence,
                        "PerformanceEquivalence" => ProofType::PerformanceEquivalence,
                        _ => ProofType::DirectEquivalence,
                    },
                    created_at: chrono::Utc::now(),
                    maintainer_signatures: vec![],
                    proof_hash: "".to_string(), // Will be computed
                    verification_status: VerificationStatus::Pending,
                },
            });
        }
        
        // Compute proof hashes
        for vector in &mut vectors {
            vector.proof_metadata.proof_hash = Self::compute_proof_hash(vector);
        }
        
        Ok(vectors)
    }
    
    pub fn load_test_vectors_with_fallback(&mut self) -> Result<(), GovernanceError> {
        // Try to load from config first
        let config_path = "governance/config/test-vectors.yml";
        match Self::load_test_vectors_from_config(config_path) {
            Ok(vectors) => {
                self.load_test_vectors(vectors);
                info!("Loaded {} test vectors from config", self.test_vectors.len());
                Ok(())
            }
            Err(e) => {
                warn!("Failed to load test vectors from config: {}. Using hardcoded fallback.", e);
                let vectors = Self::generate_consensus_test_vectors();
                self.load_test_vectors(vectors);
                Ok(())
            }
        }
    }
}
```

### Step 3: Extract Detailed CI Status (Priority: Low)

**Files to Modify:**
- `governance-app/src/validation/verification_check.rs`
  - Enhance `check_tool_status()` to return detailed status
  - Extract check run URLs and conclusions

**Changes:**
```rust
pub struct VerificationToolStatus {
    pub tool_name: String,
    pub status: StatusState,
    pub conclusion: Option<String>,
    pub check_run_url: Option<String>,
}

async fn check_tool_status_detailed(
    client: &GitHubClient,
    pr: &PullRequest,
    tool_name: &str,
) -> Result<VerificationToolStatus, GovernanceError> {
    let checks = client.get_check_runs(&pr.repository, &pr.head_sha).await?;
    
    for check in checks {
        if check.name == tool_name {
            return Ok(VerificationToolStatus {
                tool_name: tool_name.to_string(),
                status: match check.conclusion.as_deref() {
                    Some("success") => StatusState::Success,
                    Some("failure") | Some("cancelled") => StatusState::Failure,
                    _ => StatusState::Pending,
                },
                conclusion: check.conclusion.clone(),
                check_run_url: check.html_url.clone(),
            });
        }
    }
    
    Ok(VerificationToolStatus {
        tool_name: tool_name.to_string(),
        status: StatusState::Pending,
        conclusion: None,
        check_run_url: None,
    })
}
```

## Validation Plan

### Test Cases

1. **Verification Integration Test**
   - Mock GitHub client with successful verification
   - Verify equivalence proof status shows success
   - Mock GitHub client with failed verification
   - Verify equivalence proof status shows failure

2. **Test Vector Loading Test**
   - Create test config file
   - Load test vectors from config
   - Verify vectors are loaded correctly
   - Test fallback to hardcoded when config missing

3. **End-to-End Test**
   - Create PR to bllvm-consensus
   - Run cross-layer status check
   - Verify it uses actual CI results
   - Verify status check is posted correctly

### Success Criteria

1. ✅ Equivalence proof status uses actual CI verification results
2. ✅ Test vectors can be loaded from configuration
3. ✅ Fallback to hardcoded vectors if config unavailable
4. ✅ Status checks show detailed verification information
5. ✅ All existing tests pass
6. ✅ No breaking changes to existing functionality

## Phase 1 Scope Boundaries

**What This Plan Includes:**
- ✅ Integration of existing CI verification with cross-layer checks
- ✅ Configuration-based test vectors (no cryptographic enforcement)
- ✅ Enhanced status reporting

**What This Plan Excludes (Phase 2):**
- ❌ Cryptographic signature verification
- ❌ Version manifest loading from repository
- ❌ Semantic content validation
- ❌ Real equivalence proof execution (uses CI results instead)

## Timeline Estimate

- **Step 1 (Verification Integration)**: 2-3 days
- **Step 2 (Test Vector Config)**: 1-2 days
- **Step 3 (Detailed Status)**: 1 day
- **Testing & Validation**: 1-2 days

**Total**: ~1 week

## Dependencies

- GitHub API client must support:
  - `get_pr()` - Get PR details
  - `get_check_runs()` - Get check run status
  - `get_workflow_status()` - Get workflow status (already exists)

- Configuration system must support:
  - YAML file loading
  - Error handling for missing files

## Risks & Mitigation

**Risk 1**: GitHub API rate limits
- **Mitigation**: Cache results, use conditional requests

**Risk 2**: CI workflow not running when status check runs
- **Mitigation**: Handle pending state gracefully, retry logic

**Risk 3**: Test vector config format changes
- **Mitigation**: Version config format, validate on load, fallback to hardcoded

## Next Steps

1. Review and validate this plan
2. Implement Step 1 (Verification Integration)
3. Test with actual PRs
4. Implement Step 2 (Test Vector Config)
5. Update documentation

