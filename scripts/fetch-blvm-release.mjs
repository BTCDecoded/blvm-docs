#!/usr/bin/env node
/**
 * Fetches BTCDecoded/blvm latest GitHub release and writes
 * src/install/install-content.json for render-installation.mjs.
 *
 * CI: run with --strict before mdbook build (see .github/workflows/deploy.yml).
 * Local: node scripts/fetch-blvm-release.mjs && node scripts/render-installation.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DEST = path.join(ROOT, "src/install/install-content.json");
const STATIC = path.join(ROOT, "src/install/install-content.static.json");
const FALLBACK = path.join(ROOT, "src/install/install-content.fallback.json");

const args = new Set(process.argv.slice(2));

async function ghFetch(url) {
  const headers = {
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
  };
  const token = process.env.GITHUB_TOKEN;
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(url, { headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`GitHub API ${res.status} ${url}: ${text.slice(0, 400)}`);
  }
  return res.json();
}

function semverFromTag(tag) {
  if (!tag) return "";
  return tag.startsWith("v") ? tag.slice(1) : tag;
}

function pickAsset(assets, slot) {
  const { suffix, includes } = slot.pick;
  const candidates = assets.filter((a) => {
    const n = a.name.toLowerCase();
    if (!n.endsWith(suffix.toLowerCase())) return false;
    return includes.every((frag) => n.includes(frag.toLowerCase()));
  });
  if (candidates.length > 0) return candidates[0];

  const loose = assets.filter((a) => a.name.toLowerCase().endsWith(suffix.toLowerCase()));
  return loose[0] ?? null;
}

function aggregateChecksumFilename(assets) {
  const hit = assets.find((a) => a.name.toLowerCase() === "checksums.sha256");
  return hit?.name ?? null;
}

function perFileChecksumFilename(assets, pkgFilename) {
  const exact = `${pkgFilename}.sha256`;
  const hit = assets.find((a) => a.name === exact || a.name.toLowerCase() === exact.toLowerCase());
  return hit?.name ?? null;
}

function releaseDownloadUrl(repo, tag, filename) {
  return `https://github.com/${repo}/releases/download/${tag}/${filename}`;
}

function verifyForPackage(slot, filename, assets, verifyTemplate, repo, tag) {
  const aggregate = aggregateChecksumFilename(assets);
  const checksumsName = aggregate ?? "checksums.sha256";

  if (slot.id === "exe" || slot.id === "zip") {
    const checksumsUrl = releaseDownloadUrl(repo, tag, checksumsName);
    return (
      `# PowerShell — same folder as ${filename}\n` +
      `Invoke-WebRequest -Uri '${checksumsUrl}' -OutFile checksums.sha256\n` +
      `$expected = ((Get-Content checksums.sha256 | Select-String -SimpleMatch '${filename}').Line -split '\\s+')[0]\n` +
      `$actual = (Get-FileHash ${filename} -Algorithm SHA256).Hash\n` +
      `if ($expected.ToUpper() -eq $actual) { 'Checksum OK' } else { throw 'Checksum MISMATCH' }`
    );
  }

  if (aggregate) {
    const checksumsUrl = releaseDownloadUrl(repo, tag, aggregate);
    return (
      `# Run in the folder where you saved ${filename}\n` +
      `curl -LO ${checksumsUrl}\n` +
      `grep '${filename}' ${aggregate} | sha256sum --check`
    );
  }

  const checkName = perFileChecksumFilename(assets, filename);
  if (checkName) {
    return verifyTemplate.replaceAll("{{CHECKFILE}}", checkName);
  }
  return (
    `sha256sum ${filename}\n` +
    `# Compare the digest to ${checksumsName} on the GitHub release page`
  );
}

function installForPackage(slot, filename) {
  if (slot.id === "exe" || slot.id === "zip") {
    return null;
  }
  return slot.installCmdTemplate.replaceAll("{{FILENAME}}", filename);
}

function runForPackage(slot, filename) {
  if (slot.id === "exe") {
    return `# PowerShell — after download + verify\n.\\${filename} --help`;
  }
  return null;
}

function substituteDocker(docker, semver) {
  if (!docker) return null;
  const sub = (s) => (s ?? "").replaceAll("{{VERSION}}", semver);
  return {
    ...docker,
    pullCmd: sub(docker.pullCmd),
    runCmd: sub(docker.runCmd),
  };
}

function buildPackages(staticData, assets, repo, tag) {
  const packages = [];
  for (const slot of staticData.packageSlots) {
    const asset = pickAsset(assets, slot);
    if (!asset) {
      if (slot.optional) continue;
      throw new Error(`No release asset matches slot "${slot.id}" (${JSON.stringify(slot.pick)})`);
    }
    const filename = asset.name;
    const verify = verifyForPackage(slot, filename, assets, slot.verifyTemplate, repo, tag);
    const installCmd = installForPackage(slot, filename);
    const runCmd = runForPackage(slot, filename);

    packages.push({
      id: slot.id,
      label: slot.label,
      ext: slot.ext,
      icon: slot.icon,
      group: slot.group ?? null,
      description: slot.description,
      filename,
      downloadUrl: asset.browser_download_url,
      installCmd,
      runCmd,
      verify,
    });
  }
  if (packages.length === 0) {
    throw new Error("No matching release packages (check packageSlots vs release assets)");
  }
  return packages;
}

async function main() {
  if (!fs.existsSync(STATIC)) {
    console.error("fetch-blvm-release: missing", STATIC);
    process.exit(1);
  }
  const staticData = JSON.parse(fs.readFileSync(STATIC, "utf8"));
  const repo = staticData.releaseRepo ?? "BTCDecoded/blvm";

  if (args.has("--fallback")) {
    if (fs.existsSync(FALLBACK)) {
      fs.copyFileSync(FALLBACK, DEST);
      console.log("fetch-blvm-release: copied install-content.fallback.json → install-content.json");
      return;
    }
    console.warn("fetch-blvm-release: no fallback file, keeping existing install-content.json");
    return;
  }

  try {
    const latest = await ghFetch(`https://api.github.com/repos/${repo}/releases/latest`);
    const tag = latest.tag_name ?? "unknown";
    const releasesLatestUrl = `https://github.com/${repo}/releases/latest`;
    const releasesTagUrl = latest.html_url ?? `https://github.com/${repo}/releases/tag/${tag}`;
    const semver = semverFromTag(tag);
    const assets = latest.assets ?? [];

    const releasesList = await ghFetch(`https://api.github.com/repos/${repo}/releases?per_page=12`).catch(() => []);

    const releaseHistory = Array.isArray(releasesList)
      ? releasesList
          .filter((r) => !r.draft)
          .slice(0, 8)
          .map((r) => ({
            tag: r.tag_name,
            name: r.name ?? r.tag_name,
            url: r.html_url,
            publishedAt: r.published_at,
          }))
      : [];

    const packages = buildPackages(staticData, assets, repo, tag);

    const out = {
      version: 3,
      generatedAt: new Date().toISOString(),
      source: `github://${repo}`,
      release: {
        tag,
        semver,
        releasesLatestUrl,
        releasesTagUrl,
        body: latest.body ?? "",
      },
      releaseHistory,
      packageGroups: staticData.packageGroups ?? [],
      page: staticData.page,
      packages,
      docker: substituteDocker(staticData.docker, semver),
      comingSoonNote: staticData.comingSoonNote ?? "",
      markdownDoc: staticData.markdownDoc ?? {},
    };

    fs.mkdirSync(path.dirname(DEST), { recursive: true });
    fs.writeFileSync(DEST, JSON.stringify(out, null, 2) + "\n", "utf8");
    console.log(`fetch-blvm-release: wrote ${DEST} (tag ${tag}, ${packages.length} packages)`);
  } catch (e) {
    console.error("fetch-blvm-release:", e.message ?? e);
    if (process.env.CI === "true" || args.has("--strict")) {
      process.exit(1);
    }
    if (fs.existsSync(FALLBACK)) {
      fs.copyFileSync(FALLBACK, DEST);
      console.warn("fetch-blvm-release: using install-content.fallback.json");
      return;
    }
    process.exit(1);
  }
}

main();
