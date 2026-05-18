import { describe, it, expect } from "vitest";
import { parseC1Field, findInstitutionAuthors } from "../src/matcher/institutionMatcher.js";

describe("institutionMatcher", () => {
  it("should parse C1 field correctly", () => {
    const c1 = "[Author1; Author2] Test University";
    const result = parseC1Field(c1);
    expect(result).toHaveLength(1);
    expect(result[0].institution).toBe("Test University");
    expect(result[0].authors).toContain("Author1");
  });

  it("should find institution authors", () => {
    const c1 = "[Author1; Author2] Test University";
    const institutions = [{ name: "Test", pattern: "Test.*", regex: /Test/i }];
    const authors = findInstitutionAuthors(c1, institutions);
    expect(authors).toContain("Author1");
    expect(authors).toContain("Author2");
  });

  it("should return empty for no match", () => {
    const c1 = "[Author1] Other University";
    const institutions = [{ name: "Test", pattern: "Test.*", regex: /Test/i }];
    const authors = findInstitutionAuthors(c1, institutions);
    expect(authors).toHaveLength(0);
  });
});
