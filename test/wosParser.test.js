import { describe, it, expect } from "vitest";
import { parseWosFile } from "../src/parser/wosParser.js";

describe("wosParser", () => {
  it("should parse a single record", () => {
    const content = "UT WOS:000123456789001\nAF Test, Author\nC1 [Test] University\nER";
    const records = parseWosFile(content);
    expect(records).toHaveLength(1);
    expect(records[0].ut).toBe("000123456789001");
    expect(records[0].authors).toContain("Test, Author");
  });

  it("should parse multiple records", () => {
    const content = "UT WOS:0001\nAF One\nER\nUT WOS:0002\nAF Two\nER";
    const records = parseWosFile(content);
    expect(records).toHaveLength(2);
  });

  it("should return empty for empty content", () => {
    expect(parseWosFile("")).toHaveLength(0);
  });

  it("should return empty for record without UT", () => {
    const content = "AF Test, Author\nER";
    const records = parseWosFile(content);
    expect(records).toHaveLength(0);
  });

  it("should handle multi-line continuation", () => {
    const content = "UT WOS:0001\nAF Author One\n   and Author Two\nER";
    const records = parseWosFile(content);
    expect(records[0].authors[0]).toBe("Author One and Author Two");
  });

  it("should extract C1 affiliations", () => {
    const content = "UT WOS:0001\nC1 [Author] Test Univ\nER";
    const records = parseWosFile(content);
    expect(records[0].affiliations).toContain("[Author] Test Univ");
  });
});
