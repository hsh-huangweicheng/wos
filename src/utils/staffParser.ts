import Papa from "papaparse";
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
