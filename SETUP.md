# Documentation Site Setup

## Domain Configuration

The documentation site is configured to be hosted at **`docs.thebitcoincommons.org`**.

### DNS Configuration Required

Since `thebitcoincommons.org` is already used by the `commons-website` repository, you need to add a **CNAME record** (not an A record) for the subdomain:

```
Type: CNAME
Name: docs
Domain: thebitcoincommons.org
Value: BTCDecoded.github.io
```

This creates `docs.thebitcoincommons.org` as a subdomain pointing to GitHub Pages.

**Note**: Use CNAME (not A record) because:
- GitHub Pages uses CNAME records for subdomains
- CNAME allows GitHub to handle SSL certificates automatically
- A records would require manual IP management which changes

### GitHub Pages Configuration

1. Go to repository Settings → Pages
2. Under "Source", select "GitHub Actions"
3. The workflow will automatically deploy on push to `main`

The `CNAME` file in the repository root tells GitHub Pages to serve the site at `docs.thebitcoincommons.org`.

## Integration with Commons Website

The `commons-website` repository has been updated with links to the documentation:

- **Hero section**: Added "Documentation" button in CTA area
- **FAQ section**: Updated "What documentation should I read?" answer
- **Footer**: Added "Documentation" link

## Alternative Options Considered

### Option 1: `docs.thebitcoincommons.org` ✅ (Selected)
- **Pros**: Standard convention, clear separation, independent deployment
- **Cons**: Requires DNS configuration
- **Best for**: Production deployment with custom domain

### Option 2: `library.thebitcoincommons.org`
- **Pros**: Suggests a library/reference nature
- **Cons**: Less standard, might be confused with code libraries
- **Best for**: If you want to emphasize the "library" aspect

### Option 3: Integrated into `commons-website`
- **Pros**: Single domain, simpler setup
- **Cons**: Mixes marketing and technical docs, harder to manage
- **Best for**: If you want everything in one place (not recommended)

## Current Setup

- ✅ `bllvm-docs` repository configured with `CNAME` file
- ✅ GitHub Actions workflow ready for deployment
- ✅ Links added to `commons-website`
- ⏳ DNS configuration needed (manual step)
- ⏳ GitHub Pages needs to be enabled (Settings → Pages)

## Next Steps

1. **Enable GitHub Pages**:
   - Go to `bllvm-docs` repository Settings → Pages
   - Select "GitHub Actions" as source

2. **Configure DNS**:
   - Add CNAME record: `docs` → `BTCDecoded.github.io` (or your GitHub Pages domain)

3. **Test Deployment**:
   - Push changes to `main` branch
   - GitHub Actions will build and deploy
   - Verify site is accessible

4. **Verify Links**:
   - Check that links from `commons-website` work correctly
   - Test navigation between sites

