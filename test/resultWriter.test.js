import { describe, it, expect, beforeEach } from "vitest";
import { deduplicateResults, writeResults } from "../src/writer/resultWriter.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

describe("resultWriter", () => {
  describe("deduplicateResults", () => {
    it("should deduplicate by UT and author", () => {
      const results = [
        { ut: "001", authorEnglish: "Zhang", authorChinese: "张三", authorOrder: 1 },
        { ut: "001", authorEnglish: "Zhang", authorChinese: "张三", authorOrder: 1 },
        { ut: "002", authorEnglish: "Li", authorChinese: "李四", authorOrder: 1 }
      ];
      const deduped = deduplicateResults(results);
      expect(deduped).toHaveLength(2);
    });
  });

  describe("writeResults", () => {
    let testPath;

    beforeEach(() => {
      testPath = path.join(__dirname, "test_output.csv");
    });

    it("should write header and data", () => {
      const results = [{ ut: "001", authorEnglish: "Zhang", authorChinese: "张三", authorOrder: 1 }];
      writeResults(results, testPath);
      const content = fs.readFileSync(testPath, "utf-8");
      expect(content).toContain("UT");
    });
  });
});
