function preprocessForMatch(str) {
  if (!str) return "";
  return str.toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
}

module.exports = { preprocessForMatch };
