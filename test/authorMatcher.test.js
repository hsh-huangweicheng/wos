import { describe, it, expect } from "vitest";
import { matchAuthors } from "../src/matcher/authorMatcher.js";

describe("authorMatcher", () => {
  it("should match authors by pinyin", () => {
    const authors = ["zhang xiaojuan"];
    const employees = [{ chineseName: "张小娟", department: "CS", pinyin: "zhang xiaojuan" }];
    const results = matchAuthors(authors, employees);
    expect(results).toHaveLength(1);
    expect(results[0].authorChinese).toBe("张小娟");
  });

  it("should handle multiple pinyin separated by semicolon", () => {
    const authors = ["zhang xiaojuan"];
    const employees = [{ chineseName: "张小娟", department: "CS", pinyin: "zsx;zhang xiaojuan;zxj" }];
    const results = matchAuthors(authors, employees);
    expect(results).toHaveLength(1);
  });
  it("should return empty for no match", () => {
    const authors = ["unknown author"];
    const employees = [{ chineseName: "张三", department: "CS", pinyin: "zhang san" }];
    const results = matchAuthors(authors, employees);
    expect(results).toHaveLength(0);
  });

  it("should set correct author order", () => {
    const authors = ["zhang san", "li si"];
    const employees = [{ chineseName: "张三", department: "CS", pinyin: "zhang san" }];
    const results = matchAuthors(authors, employees);
    expect(results[0].authorOrder).toBe(1);
  });
});
