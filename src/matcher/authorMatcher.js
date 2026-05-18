const { preprocessForMatch } = require("./preprocessor.js");

function matchAuthors(authors, employees) {
  const results = [];

  for (let i = 0; i < authors.length; i++) {
    const authorEnglish = authors[i];
    const processedAuthor = preprocessForMatch(authorEnglish);

    for (const emp of employees) {
      const empPinyins = emp.pinyin.split(";").map(p => p.trim());

      for (const pinyin of empPinyins) {
        const processedPinyin = preprocessForMatch(pinyin);

        if (processedAuthor === processedPinyin) {
          results.push({
            authorEnglish,
            authorChinese: emp.chineseName,
            authorOrder: i + 1,
            ut: ""
          });
          break;
        }
      }
    }
  }

  return results;
}

module.exports = { matchAuthors };
