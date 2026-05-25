function parseC1Field(c1Content) {
  const lines = c1Content.split(/\n/);
  const results = [];

  for (const line of lines) {
    const regex = /\[([^\]]+)\]\s*([^\[]+)/g;
    let match;
    while ((match = regex.exec(line)) !== null) {
      const authorsStr = match[1];
      const institution = match[2].trim();
      const authors = authorsStr.split(";").map(a => a.trim()).filter(a => a);
      results.push({ institution, authors });
    }
  }

  return results;
}

function findInstitutionAuthors(c1Content, institutions) {
  const parsed = parseC1Field(c1Content);
  const matchedAuthors = [];

  for (const item of parsed) {
    for (const inst of institutions) {
      if (inst.regex.test(item.institution)) {
        matchedAuthors.push(...item.authors);
        break;
      }
    }
  }

  return matchedAuthors;
}

module.exports = { parseC1Field, findInstitutionAuthors };
