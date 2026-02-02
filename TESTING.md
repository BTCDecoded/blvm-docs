# Testing Guide

## Initial Deployment Test

### 1. Check GitHub Actions Workflow
- Go to: https://github.com/BTCDecoded/blvm-docs/actions
- Verify "Deploy Documentation" workflow is running or completed
- Check for any errors in the workflow logs

### 2. Verify GitHub Pages Status
- Go to: https://github.com/BTCDecoded/blvm-docs/settings/pages
- Should show: "Your site is live at https://docs.thebitcoincommons.org"
- Source should be: "GitHub Actions"

### 3. Test Site Access
- **Primary URL**: https://docs.thebitcoincommons.org
- **GitHub Pages URL**: https://btcdecoded.github.io/blvm-docs/ (fallback)
- Check that the mdBook site loads correctly
- Verify navigation works

### 4. Test DNS Resolution
```bash
# Check DNS propagation
dig docs.thebitcoincommons.org CNAME

# Or use online tool
# https://dnschecker.org/#CNAME/docs.thebitcoincommons.org
```

### 5. Test Content Inclusion
- Check that included content from source repositories renders:
  - Orange Paper (reference/orange-paper.md)
  - Consensus overview (consensus/overview.md)
  - Governance model (governance/governance-model.md)
  - System overview (architecture/system-overview.md)

### 6. Test Navigation
- Click through all major sections:
  - Introduction
  - Getting Started
  - Architecture
  - Consensus Layer
  - Protocol Layer
  - Node Implementation
  - Developer SDK
  - Governance
  - Reference
  - Appendices

### 7. Test Search Functionality
- Use the search box in mdBook
- Search for common terms: "consensus", "governance", "bitcoin"
- Verify results are relevant

### 8. Test Links from Commons Website
- Visit: https://thebitcoincommons.org
- Click "Documentation" button in hero section
- Verify it links to https://docs.thebitcoincommons.org
- Check footer link works
- Verify FAQ link works

### 9. Test Mobile Responsiveness
- Open site on mobile device or resize browser
- Verify navigation works on mobile
- Check that content is readable

### 10. Test Broken Links
- Check for any 404 errors
- Verify all internal links work
- Check external links (GitHub, docs.rs, etc.)

## Common Issues

### Site shows 404
- **Cause**: DNS not propagated or GitHub Pages not enabled
- **Fix**: Wait for DNS propagation, verify GitHub Pages settings

### Included content not showing
- **Cause**: `{{#include}}` directives pointing to incorrect paths
- **Fix**: Verify include paths match actual file locations in source repositories

### Build fails
- **Cause**: mdBook errors or missing files
- **Fix**: Check GitHub Actions logs for specific errors

### Links broken
- **Cause**: Incorrect paths in SUMMARY.md or included files
- **Fix**: Verify relative paths are correct

## Next Steps After Testing

1. **Fill in placeholder content** - Replace "Documentation will be aggregated..." with actual content
2. **Add more includes** - Include more content from source repositories
3. **Improve navigation** - Adjust SUMMARY.md based on what users need
4. **Add cross-references** - Link related sections together
5. **Update regularly** - Documentation automatically reflects source repository changes

