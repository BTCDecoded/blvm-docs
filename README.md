# Bitcoin Commons Documentation

**Version:** 1.0.0

Centralized documentation for the Bitcoin Commons system architecture, integration, and deployment.

## Documentation Structure

### System Documentation

- [Architecture](ARCHITECTURE.md) - 6-tier system architecture
- [Integration](INTEGRATION.md) - Cross-repository integration patterns
- [Quick Start](QUICK_START.md) - System-wide quick start guide
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [Performance Tuning](PERFORMANCE_TUNING.md) - Performance optimization guide
- [Best Practices](BEST_PRACTICES.md) - Configuration and usage recommendations
- [Deployment](DEPLOYMENT.md) - Multi-component deployment (coming soon)
- [Configuration](CONFIGURATION.md) - Unified configuration guide
- [Configuration Defaults](CONFIGURATION_DEFAULTS.md) - Auto-generated configuration defaults
- [Protocol Constants](PROTOCOL_CONSTANTS.md) - Bitcoin protocol constants
- [RPC Methods](RPC_METHODS.md) - Available RPC methods
- [Error Codes](ERROR_CODES.md) - Error code reference
- [Monitoring](MONITORING.md) - System-wide monitoring (coming soon)
- [Security](SECURITY.md) - System-wide security model (coming soon)
- [Governance](GOVERNANCE.md) - Governance model (coming soon)
- [Releases](RELEASES.md) - Release documentation (coming soon)

### Component Documentation

Component-specific documentation is in each repository's `docs/` directory:

- **bllvm-consensus**: `bllvm-consensus/docs/` - Consensus layer documentation
- **bllvm-protocol**: `bllvm-protocol/docs/` - Protocol layer documentation
- **bllvm-node**: `bllvm-node/docs/` - Node implementation documentation
- **bllvm-sdk**: `bllvm-sdk/docs/` - SDK documentation
- **bllvm-commons**: `bllvm-commons/docs/` - Governance system documentation

### Historical Documentation

Historical documentation is archived in [archive/](archive/) organized by repository.

## Quick Navigation

**New to the project?** → Start with [Quick Start](QUICK_START.md)

**Want to understand the system?** → Read [Architecture](ARCHITECTURE.md)

**Integrating components?** → See [Integration](INTEGRATION.md)

**Having issues?** → Check [Troubleshooting](TROUBLESHOOTING.md)

**Optimizing performance?** → See [Performance Tuning](PERFORMANCE_TUNING.md)

**Configuring the system?** → See [Configuration](CONFIGURATION.md) and [Best Practices](BEST_PRACTICES.md)

**Deploying to production?** → See [Deployment](DEPLOYMENT.md) (coming soon)

## Documentation Principles

All documentation follows these principles:

- **USEFUL**: Solves real problems, answers real questions
- **CONCISE**: No fluff, get to the point
- **TECHNICALLY ACCURATE**: Correct, precise, verifiable
- **IMPERATIVE**: Present tense, describes what exists
- **TIMELESS**: No dates, no status updates, no "coming soon"
- **PROPER JARGON**: Uses correct technical terms

## Contributing to Documentation

### How to Contribute

1. **Find the right place**: 
   - System-wide docs → `bllvm-docs/`
   - Component-specific docs → `<repo>/docs/`

2. **Edit directly on GitHub**:
   - Click "Edit this page" link at the top of any doc
   - Make your changes
   - Submit a pull request

3. **Follow documentation principles**:
   - Keep it useful, concise, technically accurate
   - Use imperative tense
   - Avoid dates and status updates
   - Use proper technical jargon

4. **Update cross-references**:
   - If you move content, update links
   - If you add new docs, add to README navigation

### Documentation Review Process

1. **Submit PR**: Create pull request with documentation changes
2. **Review**: Maintainers review for accuracy and style
3. **Merge**: Changes merged after approval

### Reporting Documentation Issues

- **Incorrect information**: Create GitHub issue with correction
- **Missing documentation**: Create GitHub issue describing what's missing
- **Unclear documentation**: Create GitHub issue with specific questions
- **Broken links**: Create GitHub issue with link location

## Feedback

We welcome feedback on documentation:

- **GitHub Discussions**: Use [Documentation category](https://github.com/BTCDecoded/.github/discussions/categories/documentation)
- **GitHub Issues**: Create issue for specific problems
- **Pull Requests**: Submit improvements directly

## Edit This Page

Found an issue with this page? [Edit it on GitHub](https://github.com/BTCDecoded/bllvm-docs/edit/main/README.md)

## Related Resources

- [Main Project Repository](https://github.com/BTCDecoded/.github)
- [Governance Documentation](../governance/README.md)
- [Component Repositories](../)

## Auto-Generated Documentation

The following documentation is automatically extracted from source code:

- [Configuration Defaults](CONFIGURATION_DEFAULTS.md) - Configuration defaults
- [Protocol Constants](PROTOCOL_CONSTANTS.md) - Bitcoin protocol constants
- [RPC Methods](RPC_METHODS.md) - Available RPC methods
- [Error Codes](ERROR_CODES.md) - Error code reference

To regenerate:
```bash
cd bllvm-docs
python3 tools/extract-defaults.py
python3 tools/extract-constants.py
python3 tools/extract-rpc-methods.py
python3 tools/extract-errors.py
```

## Releases

Documentation releases provide versioned snapshots. See [Release System](RELEASE_SYSTEM.md) for details.

**Current Version:** 1.0.0

**Creating a Release:**
1. Use GitHub Actions: "Create Documentation Release" workflow
2. Or manually: Follow process in [RELEASE_SYSTEM.md](RELEASE_SYSTEM.md)

**Archived Versions:** [archive/versions/](archive/versions/)
