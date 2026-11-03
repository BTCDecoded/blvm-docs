# Documentation Site Setup

## Domain Configuration

BTCDecoded documentation is hosted at **`docs.btcdecoded.org`**.

| Path | What |
|---|---|
| `/` | Hub: BLVM manual and Intelligence guide |
| `/blvm/` | BLVM mdBook |
| `/intelligence/` | Intelligence MCP guide |

The consensus specification stays on `thebitcoincommons.org`. Account, checkout, and BLVM downloads stay on `btcdecoded.org`.

`btcdecoded.org` DNS is Cloudflare. Add a **DNS-only** CNAME (grey cloud) so GitHub Pages can issue the certificate:

```
Type: CNAME
Name: docs
Domain: btcdecoded.org
Value: btcdecoded.github.io
Proxy: DNS only
```

### Previous host

The previous host served this book at the domain root. That hostname was `docs.thebitcoincommons.org`. `legacy-redirect/` is a one-page GitHub Pages site whose `CNAME` is that old host. Its `404.html` sends `/some/page` to `https://docs.btcdecoded.org/blvm/some/page`.

Publish `legacy-redirect/` only after this repository's Pages custom domain is `docs.btcdecoded.org`. Two Pages sites cannot claim the old host at the same time. `thebitcoincommons.org` DNS is Namecheap (`dns1.registrar-servers.com`); leave the existing `docs` CNAME pointed at `btcdecoded.github.io` so the redirect site can claim it.

### GitHub Pages Configuration

1. Go to repository Settings → Pages
2. Under "Source", select "GitHub Actions"
3. The workflow will automatically deploy on push to `main`

The `CNAME` file in the repository root tells GitHub Pages to serve the site at `docs.btcdecoded.org`. The deploy workflow assembles `publish/` from `hub/` plus the mdBook under `blvm/`.

## Integration with Commons Website

The `commons-website` repository has been updated with links to the documentation:

- **Hero section**: Added "Documentation" button in CTA area
- **FAQ section**: Updated "What documentation should I read?" answer
- **Footer**: Added "Documentation" link

## Alternative Options Considered

### Option 1: `docs.btcdecoded.org` ✅ (Selected)
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

- ✅ `blvm-docs` repository configured with `CNAME` file
- ✅ GitHub Actions workflow ready for deployment
- ✅ Links added to `commons-website`
- ⏳ DNS configuration needed (manual step)
- ⏳ GitHub Pages needs to be enabled (Settings → Pages)

## Next Steps

1. **Enable GitHub Pages**:
   - Go to `blvm-docs` repository Settings → Pages
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

