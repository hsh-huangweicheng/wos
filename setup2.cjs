const fs = require("fs");
const path = require("path");

// Create staffParser.ts
const staffContent = `import Papa from "papaparse";
import { Staff } from "../types";
import { generatePinyinVariants } from "./pinyinMatcher";

export function parseStaffCSV(content: string): Staff[] {
  const result = Papa.parse(content, {
    header: true,
    skipEmptyLines: true,
  });
  
  return (result.data as any[]).map((row, index) => ({
    id: index + 1,
    department: row["现部门"] || "",
    name: row["姓名"] || "",
    position: row["单位职务"] || "",
    pinyinVariants: generatePinyinVariants(row["姓名"] || ""),
    createdAt: new Date().toISOString(),
  }));
}

export default { parseStaffCSV };
`;

fs.writeFileSync("C:/Workspace/wos/src/utils/staffParser.ts", staffContent);
console.log("Created staffParser.ts");

// Create pinyinMatcher.ts  
const pinyinContent = `import { pinyin } from "pinyin-pro";

export function generatePinyinVariants(name: string): string[] {
  if (!name) return [];
  
  const variants: string[] = [];
  const py = pinyin(name, { pattern: "first" }) as string;
  const pyFull = pinyin(name, { pattern: "all" }) as string;
  
  // Extract surname and given name
  const surname = pyFull.slice(0, 1);
  const givenName = pyFull.slice(1);
  
  // Variant 1: surname + givenName (no space)
  variants.push(surname + givenName);
  
  // Variant 2: surname + space + givenName
  variants.push(surname + " " + givenName);
  
  // Variant 3: surname + hyphen + givenName  
  variants.push(surname + "-" + givenName);
  
  // Variant 4: surname initial. givenName initial.
  const surnameInitial = surname.charAt(0).toUpperCase();
  const givenNameInitials = givenName.split("").map(c => c.charAt(0).toUpperCase()).join(". ");
  variants.push(surnameInitial + ". " + givenNameInitials + ".");
  
  // Variant 5: givenName + surname (reversed)
  variants.push(givenName + " " + surname);
  
  // Variant 6: surname + givenName initial.
  const givenNameFirst = givenName.charAt(0).toUpperCase();
  variants.push(surname + " " + givenNameFirst + ".");
  
  // Additional variants
  variants.push(surname.toUpperCase() + " " + givenName.toUpperCase());
  variants.push(surname.charAt(0).toUpperCase() + givenName);
  
  return [...new Set(variants)];
}

export function matchAuthor(staffName: string, authorName: string): boolean {
  const variants = generatePinyinVariants(staffName);
  const normalizedAuthor = authorName.toLowerCase().replace(/,/g, " ").replace(/\./g, "");
  
  for (const variant of variants) {
    const normalizedVariant = variant.toLowerCase();
    if (normalizedAuthor.includes(normalizedVariant) || normalizedVariant.includes(normalizedAuthor)) {
      return true;
    }
  }
  return false;
}

export default { generatePinyinVariants, matchAuthor };
`;

fs.writeFileSync("C:/Workspace/wos/src/utils/pinyinMatcher.ts", pinyinContent);
console.log("Created pinyinMatcher.ts");

// Create deduplicator.ts
const dedupContent = `import { Staff } from "../types";

export function deduplicateStaff(staff: Staff[]): Staff[] {
  const seen = new Map<string, Staff>();
  
  for (const s of staff) {
    const key = \`\${s.name}-\${s.department}\`;
    if (!seen.has(key)) {
      seen.set(key, s);
    }
  }
  
  return Array.from(seen.values());
}

export default { deduplicateStaff };
`;

fs.writeFileSync("C:/Workspace/wos/src/utils/deduplicator.ts", dedupContent);
console.log("Created deduplicator.ts");

