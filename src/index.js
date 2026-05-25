const path = require("path");
const { parseWosDirectory } = require("./parser/wosParser.js");
const { loadEmployeeConfig, loadInstitutionConfig } = require("./parser/csvParser.js");
const { parseC1Field } = require("./matcher/institutionMatcher.js");
const { writeResults, deduplicateResults } = require("./writer/resultWriter.js");
const { preprocessForMatch } = require("./matcher/preprocessor.js");

async function main() {
  console.log("WOS Author Matching Tool");
  console.log("============================");

  const wosDir = path.join(process.cwd(), "data", "wos");
  const employeeConfigPath = path.join(process.cwd(), "data", "config", "员工.csv");
  const institutionConfigPath = path.join(process.cwd(), "data", "config", "机构.csv");
  const outputPath = path.join(process.cwd(), "data", "结果.csv");

  console.log("Loading employee config...");
  const employees = loadEmployeeConfig(employeeConfigPath);
  console.log("Loaded " + employees.length + " employees");

  console.log("Loading institution config...");
  const institutions = loadInstitutionConfig(institutionConfigPath);
  console.log("Loaded " + institutions.length + " institutions");

  console.log("Parsing WOS files...");
  const records = await parseWosDirectory(wosDir);
  console.log("Found " + records.length + " records");

  console.log("Processing records...");
  const allResults = [];

  for (const record of records) {
    const c1Content = record.affiliations.join("\n");
    const parsedC1 = parseC1Field(c1Content);

    const instAuthorSet = new Set();
    const instAuthorMap = new Map();

    for (const item of parsedC1) {
      for (const inst of institutions) {
        if (inst.regex.test(item.institution)) {
          for (const author of item.authors) {
            const processed = preprocessForMatch(author);
            instAuthorSet.add(processed);
            instAuthorMap.set(processed, author);
          }
          break;
        }
      }
    }

    for (let i = 0; i < record.authors.length; i++) {
      const authorEnglish = record.authors[i];
      const processed = preprocessForMatch(authorEnglish);

      if (instAuthorSet.has(processed)) {
        let authorChinese = "";
        for (const emp of employees) {
          const empPinyins = emp.pinyin.split(";").map(p => preprocessForMatch(p.trim()));
          if (empPinyins.includes(processed)) {
            authorChinese = emp.chineseName;
            break;
          }
        }

        allResults.push({
          ut: record.ut,
          authorEnglish: authorEnglish,
          authorChinese: authorChinese,
          authorOrder: i + 1
        });
      }
    }
  }

  console.log("Deduplicating results...");
  const deduplicated = deduplicateResults(allResults);
  console.log("Writing " + deduplicated.length + " results...");
  writeResults(deduplicated, outputPath);
  console.log("Done!");
}

main().catch(console.error);
