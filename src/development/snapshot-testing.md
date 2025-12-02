# Snapshot Testing

## Overview

Bitcoin Commons uses snapshot testing to verify that complex data structures and outputs don't change unexpectedly. Snapshot tests capture the output of functions and compare them against stored snapshots, making it easy to detect unintended changes.

## Purpose

Snapshot testing serves to:

- **Detect Regressions**: Catch unexpected changes in output
- **Verify Complex Outputs**: Test complex data structures without writing detailed assertions
- **Document Behavior**: Snapshots serve as documentation of expected behavior
- **Review Changes**: Interactive review of snapshot changes

**Code**: ```1:5:bllvm-commons/tests/snapshot/mod.rs```

## Architecture

### Snapshot Testing Library

Bitcoin Commons uses `insta` for snapshot testing:

- **Snapshot Storage**: Snapshots stored in `.snap` files
- **Version Control**: Snapshots committed to git
- **Interactive Review**: Review changes before accepting
- **Format Support**: Text, JSON, YAML, and custom formats

**Code**: ```98:129:bllvm-commons/docs/testing/TESTING_SETUP.md```

## Usage

### Creating Snapshots

```rust
use insta::assert_snapshot;

#[test]
fn test_example() {
    let result = compute_something();
    assert_snapshot!("snapshot_name", result);
}
```

**Code**: ```100:110:bllvm-commons/docs/testing/TESTING_SETUP.md```

### Snapshot Examples

#### Content Hash Snapshot

```rust
#[test]
fn test_content_hash_snapshot() {
    let validator = ContentHashValidator::new();
    let content = b"test content for snapshot";
    let hash = validator.compute_file_hash(content);
    
    assert_snapshot!("content_hash", hash);
}
```

**Code**: ```10:18:bllvm-commons/tests/snapshot/validation_snapshot_tests.rs```

#### Directory Hash Snapshot

```rust
#[test]
fn test_directory_hash_snapshot() {
    let validator = ContentHashValidator::new();
    let files = vec![
        ("file1.txt".to_string(), b"content1".to_vec()),
        ("file2.txt".to_string(), b"content2".to_vec()),
        ("file3.txt".to_string(), b"content3".to_vec()),
    ];
    
    let result = validator.compute_directory_hash(&files);
    
    assert_snapshot!("directory_hash", format!(
        "file_count: {}\ntotal_size: {}\nmerkle_root: {}",
        result.file_count,
        result.total_size,
        result.merkle_root
    ));
}
```

**Code**: ```19:37:bllvm-commons/tests/snapshot/validation_snapshot_tests.rs```

#### Version Format Snapshot

```rust
#[test]
fn test_version_format_snapshot() {
    let validator = VersionPinningValidator::default();
    let format = validator.generate_reference_format(
        "v1.2.3",
        "abc123def456",
        "sha256:fedcba9876543210"
    );
    
    assert_snapshot!("version_format", format);
}
```

**Code**: ```39:49:bllvm-commons/tests/snapshot/validation_snapshot_tests.rs```

## Running Snapshot Tests

### Run Tests

```bash
cargo test --test snapshot_tests
```

Or using Makefile:

```bash
make test-snapshot
```

**Code**: ```44:48:bllvm-commons/docs/testing/TESTING_SETUP.md```

## Updating Snapshots

### Interactive Review

When snapshots change (expected changes):

```bash
cargo insta review
```

This opens an interactive review where you can:
- Accept changes
- Reject changes
- See diffs

**Code**: ```112:123:bllvm-commons/docs/testing/TESTING_SETUP.md```

### Update Command

```bash
make update-snapshots
```

**Code**: ```47:47:bllvm-commons/docs/testing/TESTING_SETUP.md```

## Snapshot Files

### File Location

- **Location**: `tests/snapshots/`
- **Format**: `.snap` files
- **Version Controlled**: Yes

**Code**: ```124:129:bllvm-commons/docs/testing/TESTING_SETUP.md```

### File Structure

Snapshot files are organized by test module:

```
tests/snapshots/
├── validation_snapshot_tests/
│   ├── content_hash.snap
│   ├── directory_hash.snap
│   └── version_format.snap
└── github_snapshot_tests/
    └── ...
```

## Best Practices

### 1. Commit Snapshots

- Commit `.snap` files to version control
- Review snapshot changes in PRs
- Don't ignore snapshot files

**Code**: ```203:206:bllvm-commons/docs/testing/TESTING_SETUP.md```

### 2. Review Changes

- Always review snapshot changes before accepting
- Understand why snapshots changed
- Verify changes are expected

**Code**: ```159:165:bllvm-commons/docs/testing/TESTING_SETUP.md```

### 3. Use Descriptive Names

- Use clear snapshot names
- Include context in snapshot names
- Group related snapshots

### 4. Test Complex Outputs

- Use snapshots for complex data structures
- Test formatted output
- Test serialized data

## Troubleshooting

### Snapshots Failing

If snapshots fail unexpectedly:

1. Review changes: `cargo insta review`
2. If changes are expected, accept them
3. If changes are unexpected, investigate

**Code**: ```159:165:bllvm-commons/docs/testing/TESTING_SETUP.md```

### Snapshot Not Found

If snapshot file is missing:

1. Run test to generate snapshot
2. Review generated snapshot
3. Accept if correct

## CI Integration

### GitHub Actions

Snapshot tests run in CI:

- **On PRs**: Run snapshot tests
- **On Push**: Run snapshot tests
- **Fail on Mismatch**: Tests fail if snapshots don't match

### Local CI Simulation

```bash
# Run snapshot tests (like CI)
make test-snapshot
```

**Code**: ```144:155:bllvm-commons/docs/testing/TESTING_SETUP.md```

## Configuration

### Insta Configuration

Configuration file: `.insta.yml`

```yaml
# Insta configuration
snapshot_path: tests/snapshots
```

**Code**: ```1:15:bllvm-commons/.insta.yml```

## Test Suites

### Validation Snapshots

Tests for validation functions:

- Content hash computation
- Directory hash computation
- Version format generation
- Version parsing

**Code**: ```1:53:bllvm-commons/tests/snapshot/validation_snapshot_tests.rs```

### GitHub Snapshots

Tests for GitHub integration:

- PR comment formatting
- Status check formatting
- Webhook processing

**Code**: ```1:51:bllvm-commons/tests/snapshot/github_snapshot_tests.rs```

## See Also

- [Testing Infrastructure](testing.md) - Overview of all testing techniques
- [Property-Based Testing](property-based-testing.md) - Verify invariants with random inputs
- [Fuzzing Infrastructure](fuzzing.md) - Automated bug discovery
- [Contributing](contributing.md) - Testing requirements for contributions

## Benefits

1. **Easy Regression Detection**: Catch unexpected changes easily
2. **Complex Output Testing**: Test complex structures without detailed assertions
3. **Documentation**: Snapshots document expected behavior
4. **Interactive Review**: Review changes before accepting
5. **Version Control**: Track changes over time

## Components

The snapshot testing system includes:
- Insta snapshot testing library
- Snapshot test suites
- Snapshot file management
- Interactive review tools
- CI integration

**Location**: `bllvm-commons/tests/snapshot/`, `bllvm-commons/docs/testing/TESTING_SETUP.md`

