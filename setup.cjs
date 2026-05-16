const fs = require("fs");
const path = require("path");

const dir = "C:/Workspace/wos/src/utils";
if (!fs.existsSync(dir)) fs.mkdirSync(dir, {recursive:true});

const content = `import { WOSRecord, AuthorInfo } from "../types";

function splitRecords(content: string): string[] {
  const records: string[] = [];
  const lines = content.split("\n");
  let currentRecord: string[] = [];
  for (const line of lines) {
    if (line.startsWith("PT ")) {
      if (currentRecord.length > 0) records.push(currentRecord.join("\n"));
      currentRecord = [line];
    } else if (line.startsWith("ER")) {
      currentRecord.push(line);
      records.push(currentRecord.join("\n"));
      currentRecord = [];
    } else if (currentRecord.length > 0) {
      currentRecord.push(line);
    }
  }
  return records;
}

function parseField(lines: string[], field: string): string {
  for (const line of lines) {
    if (line.startsWith(field + " ")) return line.slice(field.length + 1).trim();
    if (line.startsWith(field + "\t")) return line.slice(field.length + 1).trim();
  }
  return "";
}

function parseMultiLineField(lines: string[], field: string): string[] {
  const values: string[] = [];
  for (const line of lines) {
    if (line.startsWith(field + " ")) values.push(line.slice(field.length + 1).trim());
    else if (line.startsWith("   ") && values.length > 0) values[values.length - 1] += " " + line.trim();
  }
  return values;
}

function parseC1Field(c1: string): AuthorInfo[] {
  const authors: AuthorInfo[] = [];
  const parts = c1.split("]");
  for (const part of parts) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    let name = "", institution = "";
    if (trimmed.startsWith("[")) {
      const closeIdx = trimmed.indexOf("]");
      if (closeIdx > 0) {
        name = trimmed.slice(1, closeIdx).trim();
        institution = trimmed.slice(closeIdx + 1).trim();
      }
    } else {
      const commaIdx = trimmed.indexOf(",");
      if (commaIdx > 0) {
        name = trimmed.slice(0, commaIdx).trim();
        institution = trimmed.slice(commaIdx + 1).trim();
      } else {
        name = trimmed;
      }
    }
    if (name) {
      institution = institution.replace(/^,\s*/, "").replace(/\s*Peoples R China\.?$/i, "").replace(/\s*China\.?$/i, "").trim();
      authors.push({ name, fullName: name, institution, institutionCn: "", matched: false });
    }
  }
  return authors;
}

export function parseWOSFile(content: string): WOSRecord[] {
  const records = splitRecords(content);
  const results: WOSRecord[] = [];
  for (const record of records) {
    if (!record.trim()) continue;
    const lines = record.split("\n");
    const au = parseMultiLineField(lines, "AU");
    const af = parseMultiLineField(lines, "AF");
    const c1 = parseField(lines, "C1");
    const authors = c1 ? parseC1Field(c1) : au.map(n => ({ name: n, fullName: n, institution: "", institutionCn: "", matched: false }));
    results.push({
      id: crypto.randomUUID(),
      pt: parseField(lines, "PT"),
      ut: parseField(lines, "UT"),
      ti: parseField(lines, "TI"),
      so: parseField(lines, "SO"),
      py: parseField(lines, "PY"),
      au, af, c1,
      em: parseField(lines, "EM"),
      di: parseField(lines, "DI"),
      tc: parseField(lines, "TC"),
      authors
    });
  }
  return results;
}
`;
fs.writeFileSync(path.join(dir, "wosParser.ts"), content);
console.log("Created wosParser.ts");
