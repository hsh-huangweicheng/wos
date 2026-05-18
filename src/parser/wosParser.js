const fs = require("fs");
const path = require("path");

function parseWosFile(content) {
  const records = [];
  const recordBlocks = content.split(/\nER\n/);

  for (const block of recordBlocks) {
    if (!block.trim()) continue;
    const record = parseRecordBlock(block);
    if (record) {
      records.push(record);
    }
  }
  return records;
}

function parseRecordBlock(block) {
  const lines = block.split("\n");
  let ut = "";
  const authors = [];
  const affiliations = [];

  let currentField = "";
  let currentValue = "";

  for (const line of lines) {
    const fieldMatch = line.match(/^([A-Z0-9]+)\s+(.*)$/);
    if (fieldMatch) {
      if (currentField) {
        processFieldValue(currentField, currentValue.trim(), authors, affiliations, (v) => { ut = v; });
      }
      currentField = fieldMatch[1];
      currentValue = fieldMatch[2];
    } else if (line.startsWith("   ")) {
      currentValue += " " + line.trim();
    }
  }

  if (currentField) {
    processFieldValue(currentField, currentValue.trim(), authors, affiliations, (v) => { ut = v; });
  }

  if (!ut) return null;
  return { ut, authors, affiliations };
}

function processFieldValue(field, value, authors, affiliations, setUt) {
  switch (field) {
    case "UT":
      setUt(value.replace("WOS:", ""));
      break;
    case "AF":
      if (value) authors.push(value);
      break;
    case "C1":
      if (value) affiliations.push(value);
      break;
  }
}

async function parseWosDirectory(dirPath) {
  const files = fs.readdirSync(dirPath);
  const wosFiles = files.filter(f => f.endsWith(".txt") || f.endsWith(".rec"));

  const allRecords = [];
  for (const file of wosFiles) {
    const filePath = path.join(dirPath, file);
    const content = fs.readFileSync(filePath, "utf-8");
    const records = parseWosFile(content);
    allRecords.push(...records);
  }
  return allRecords;
}

module.exports = { parseWosFile, parseWosDirectory };
