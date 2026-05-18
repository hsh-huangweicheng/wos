import { describe, it, expect } from "vitest";
import { preprocessForMatch } from "../src/matcher/preprocessor.js";

describe("preprocessor", () => {
  it("should lowercase the string", () => {
    expect(preprocessForMatch("Zhang Xiaojuan")).toBe("zhang xiaojuan");
  });

  it("should remove non-alphanumeric except space", () => {
    expect(preprocessForMatch("Zhang, Xiaojuan (Professor)")).toBe("zhang xiaojuan professor");
  });

  it("should collapse multiple spaces", () => {
    expect(preprocessForMatch("zhang    xiaojuan")).toBe("zhang xiaojuan");
  });

  it("should return empty string for empty input", () => {
    expect(preprocessForMatch("")).toBe("");
  });

  it("should trim whitespace", () => {
    expect(preprocessForMatch("  zhang  ")).toBe("zhang");
  });
});
