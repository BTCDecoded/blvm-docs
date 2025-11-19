# Archived Documentation Versions

This directory contains archived documentation for previous major versions.

## Current Version

The current documentation is in the root of `bllvm-docs/`. Check the [VERSION](../VERSION) file for the current version number.

## Archived Versions

Archived versions are organized by major version (e.g., `v1.0/`, `v2.0/`).

### Accessing Archived Versions

To view archived documentation:

1. Navigate to the version directory: `archive/versions/vX.Y/`
2. Open the `INDEX.md` or `README.md` file in that directory

### When Versions Are Archived

Documentation is archived when:
- A new major version is released (e.g., 1.0.0 → 2.0.0)
- The documentation structure changes significantly
- Breaking changes require separate documentation

### Archiving Process

To archive the current version:

```bash
cd bllvm-docs
./tools/archive-version.sh
```

This will:
1. Read the current version from `VERSION`
2. Extract the major version (X.Y)
3. Copy all documentation to `archive/versions/vX.Y/`
4. Preserve the exact state of documentation at that version

## Version History

- No archived versions yet

