#!/usr/bin/env node
/**
 * Generates getting-started/installation.md from src/install/install-content.json.
 * Run from blvm-docs repo root: node scripts/render-installation.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const jsonPath = path.join(root, "src/install/install-content.json");
const outPath = path.join(root, "src/getting-started/installation.md");

const data = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
const { page, release, packages, managed, platforms, markdownDoc } = data;

let md = `<!-- Generated from src/install/install-content.json. Do not edit by hand. Run: node scripts/render-installation.mjs -->\n\n`;
md += `# Installation\n\n`;
md += `${page.lead}\n\n`;
md += `**Current release:** [${release.tag} on GitHub →](${release.releasesTagUrl})  \n`;
md += `**All builds:** [GitHub Releases (latest)](${release.releasesLatestUrl})\n\n`;
md += `Each artifact ships with a \`.sha256\` file and a detached GPG signature (\`.sig\`). See the [signature verification guide](${page.verificationGuideUrl}).\n\n`;
md += `## Pre-built packages\n\n`;

for (const p of packages) {
  md += `### ${p.label} (\`${p.ext}\`)\n\n`;
  md += `${p.description}\n\n`;
  md += `**Download:** get \`${p.filename}\` from [GitHub Releases](${release.releasesLatestUrl}).\n\n`;
  md += `**Install:**\n\n`;
  md += `\`\`\`bash\n${p.installCmd}\n\`\`\`\n\n`;
  md += `**Verify checksum:**\n\n`;
  md += `\`\`\`bash\n${p.verify}\n\`\`\`\n\n`;
  md += `Detached signature: \`${p.filename}.sig\`.\n\n`;
}

md += `## Managed installs (${managed.badge})\n\n`;
md += `> ${managed.banner}\n\n`;
md += `${managed.intro}\n\n`;

for (const plat of platforms) {
  md += `### ${plat.name}\n\n`;
  md += `${plat.description}\n\n`;
  md += `1. ${plat.steps.join("\n1. ")}\n\n`;
  md += `- [Full documentation](${plat.docsLink})\n`;
  md += `- [${plat.supportLinkLabel}](${plat.supportLink})\n\n`;
}

md += `## Build from source\n\n`;
md += `For other architectures or development, see [build instructions](${page.buildFromSourceUrl}).\n\n`;

if (markdownDoc?.extraSectionsAfterPackages) {
  md += markdownDoc.extraSectionsAfterPackages;
}

fs.writeFileSync(outPath, md, "utf8");
console.log(`Wrote ${path.relative(root, outPath)}`);
