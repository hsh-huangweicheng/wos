const fs = require("fs");

function parseCSV(content) {
  const lines = content.split(/\r?\n/).filter(line => line.trim());
  if (lines.length < 2) return [];

  const headers = lines[0].split(",").map(h => h.trim());
  const records = [];

  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    const record = {};
    headers.forEach((header, index) => {
      record[header] = values[index] || "";
    });
    records.push(record);
  }

  return records;
}

function parseCSVLine(line) {
  const values = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === "\"") {
      if (inQuotes && line[i + 1] === "\"") {
        current += "\"";
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === "," && !inQuotes) {
      values.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }
  values.push(current.trim());
  return values;
}

function loadEmployeeConfig(filePath) {
  const content = fs.readFileSync(filePath, "utf-8");
  const records = parseCSV(content);

  return records.map(record => {
    const keys = Object.keys(record);
    const nameKey = keys.find(k => k.includes("姓") || k.includes("name"));
    const deptKey = keys.find(k => k.includes("部门") || k.includes("department") || k.includes("部门"));
    const pinyinKey = keys.find(k => k.includes("拼音") || k.includes("pinyin"));

    return {
      chineseName: record[nameKey] || "",
      department: record[deptKey] || "",
      pinyin: record[pinyinKey] || ""
    };
  }).filter(emp => emp.chineseName && emp.pinyin);
}

function loadInstitutionConfig(filePath) {
  const content = fs.readFileSync(filePath, "utf-8");
  const records = parseCSV(content);

  return records.map(record => {
    const keys = Object.keys(record);
    const patternKey = keys.find(k => k.includes("英文") || k.includes("pattern") || k.includes("mode"));

    const pattern = record[patternKey] || "";
    let regex;
    try {
      regex = new RegExp(pattern, "i");
    } catch (e) {
      regex = new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");
    }

    return {
      pattern: pattern,
      regex: regex,
      raw: record
    };
  }).filter(cfg => cfg.pattern);
}

module.exports = { loadEmployeeConfig, loadInstitutionConfig };
