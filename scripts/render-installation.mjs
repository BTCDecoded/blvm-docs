#!/usr/bin/env node
/**
 * Generates getting-started/installation.md from src/install/install-content.json.
 * Run from blvm-docs repo root after fetch-blvm-release.mjs:
 *   node scripts/fetch-blvm-release.mjs && node scripts/render-installation.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const jsonPath = path.join(root, "src/install/install-content.json");
const outPath = path.join(root, "src/getting-started/installation.md");

const data = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
const { page, release, packages, packageGroups, docker, comingSoonNote, markdownDoc } = data;

const groups = packageGroups ?? [];
const byGroup = new Map();
for (const p of packages) {
  const g = p.group ?? "other";
  if (!byGroup.has(g)) byGroup.set(g, []);
  byGroup.get(g).push(p);
}

let md = `<!-- Generated from src/install/install-content.json. Do not edit by hand. Run: node scripts/fetch-blvm-release.mjs && node scripts/render-installation.mjs -->\n\n`;
md += `# Installation\n\n`;
md += `${page.lead}\n\n`;
md += `**Current release:** [${release.tag} on GitHub →](${release.releasesTagUrl})  \n`;
md += `**All builds:** [GitHub Releases (latest)](${release.releasesLatestUrl})\n\n`;
md += `Download checksums.sha256 from the release page and verify each artifact before running.\n\n`;
md += `## Pre-built packages\n\n`;

for (const group of groups) {
  const pkgs = byGroup.get(group.id) ?? [];
  if (pkgs.length === 0) continue;
  md += `### ${group.title}\n\n`;
  for (const p of pkgs) {
    md += `#### ${p.label} (\`${p.ext}\`)\n\n`;
    md += `${p.description}\n\n`;
    md += `**Download:** [\`${p.filename}\`](${p.downloadUrl}) · [GitHub Releases](${release.releasesLatestUrl})\n\n`;
    if (p.installCmd) {
      md += `**Install:**\n\n`;
      md += `\`\`\`bash\n${p.installCmd}\n\`\`\`\n\n`;
    }
    if (p.runCmd) {
      md += `**Run:**\n\n`;
      md += `\`\`\`bash\n${p.runCmd}\n\`\`\`\n\n`;
    }
    md += `**Verify:**\n\n`;
    const fence = p.id === "exe" ? "powershell" : "bash";
    md += `\`\`\`${fence}\n${p.verify}\n\`\`\`\n\n`;
  }
}

const ungrouped = byGroup.get("other") ?? [];
if (ungrouped.length > 0) {
  md += `### Other packages\n\n`;
  for (const p of ungrouped) {
    md += `#### ${p.label}\n\n`;
    md += `**Download:** [\`${p.filename}\`](${p.downloadUrl})\n\n`;
    if (p.installCmd) {
      md += `\`\`\`bash\n${p.installCmd}\n\`\`\`\n\n`;
    }
    md += `\`\`\`bash\n${p.verify}\n\`\`\`\n\n`;
  }
}

if (docker) {
  md += `## ${docker.title}\n\n`;
  md += `${docker.description}\n\n`;
  md += `**Pull:**\n\n`;
  md += `\`\`\`bash\n${docker.pullCmd}\n\`\`\`\n\n`;
  md += `**Run:**\n\n`;
  md += `\`\`\`bash\n${docker.runCmd}\n\`\`\`\n\n`;
  if (docker.packageUrl) {
    md += `[${docker.packageLinkLabel ?? "Package registry"}](${docker.packageUrl})\n\n`;
  }
}

if (comingSoonNote) {
  md += `## Managed installs (Not ready yet)\n\n`;
  md += `> ${comingSoonNote} Use the packages above, Docker on GHCR, or build from source until managed marketplace listings ship.\n\n`;
}

if (markdownDoc?.experimentalVariantSection) {
  md += markdownDoc.experimentalVariantSection;
  md += "\n";
}

md += `## Build from source\n\n`;
md += `For other architectures, experimental features, or development, see [build instructions](${page.buildFromSourceUrl}) and [Release process](../development/release-process.md).\n\n`;

if (markdownDoc?.extraSectionsAfterPackages) {
  md += markdownDoc.extraSectionsAfterPackages;
}

fs.writeFileSync(outPath, md, "utf8");
console.log(`Wrote ${path.relative(root, outPath)}`);
