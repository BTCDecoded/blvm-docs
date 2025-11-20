# Deployment Checklist

## ✅ Completed
- [x] DNS CNAME record added (`docs` → `BTCDecoded.github.io`)

## Next Steps

### 1. Enable GitHub Pages
1. Go to: https://github.com/BTCDecoded/bllvm-docs/settings/pages
2. Under "Source", select: **"GitHub Actions"**
3. Save the settings

### 2. Commit and Push Changes
```bash
cd bllvm-docs
git add .
git commit -m "Initial documentation system setup"
git push origin main
```

### 3. Verify GitHub Actions Workflow
1. Go to: https://github.com/BTCDecoded/bllvm-docs/actions
2. Check that the "Deploy Documentation" workflow runs
3. Wait for it to complete successfully

### 4. Wait for DNS Propagation
- DNS changes can take 5 minutes to 48 hours
- Usually propagates within 1-2 hours
- Check propagation: `dig docs.thebitcoincommons.org` or use https://dnschecker.org

### 5. Verify Site is Live
- Visit: https://docs.thebitcoincommons.org
- Should see the mdBook documentation site
- If you see a 404, DNS might not have propagated yet

### 6. Test Links from Commons Website
- Visit: https://thebitcoincommons.org
- Click the "Documentation" button in hero section
- Verify it links correctly to docs site

## Troubleshooting

### If GitHub Pages shows "Not yet published"
- Check that GitHub Actions workflow completed successfully
- Verify "Source" is set to "GitHub Actions" (not "Deploy from a branch")
- Check workflow logs for errors

### If DNS doesn't resolve
- Verify CNAME record is correct: `docs` → `BTCDecoded.github.io`
- Check DNS propagation: https://dnschecker.org
- Wait longer (can take up to 48 hours)

### If site shows 404
- DNS might not have propagated
- Check GitHub Pages settings show the site is published
- Verify CNAME file in repository matches DNS record

### If build fails
- Check GitHub Actions logs
- Verify all submodules are accessible
- Check that mdBook build completes successfully

