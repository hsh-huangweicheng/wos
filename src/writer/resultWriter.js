const fs = require("fs");

function deduplicateResults(results) {
  const seen = new Map();

  for (const r of results) {
    const key = r.ut + "|" + r.authorEnglish;
    if (!seen.has(key)) {
      seen.set(key, r);
    }
  }

  return Array.from(seen.values());
}

function writeResults(results, outputPath) {
  const lines = ["UT,英文姓名,中文姓名,作者顺序"];

  for (const r of results) {
    const chinese = r.authorChinese || "";
    lines.push([r.ut, r.authorEnglish, chinese, r.authorOrder].join(","));
  }

  fs.writeFileSync(outputPath, "\uFEFF" + lines.join("\n"), "utf8");
}

module.exports = { writeResults, deduplicateResults };
