import { pinyin } from "pinyin-pro";

const logger = {
  info: (msg: string, ...args: any[]) => console.log(`[Pinyin] ${msg}`, ...args),
}

export function generatePinyinVariants(name: string): string[] {
  if (!name) return [];

  const variants: string[] = [];
  logger.info(`为 "${name}" 生成拼音变体`)
  const pyFull = pinyin(name, { pattern: "first" }) as string;
  
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
  const normalizedAuthor = authorName.toLowerCase().replace(/,/g, " ").replace(/./g, "");
  
  for (const variant of variants) {
    const normalizedVariant = variant.toLowerCase();
    if (normalizedAuthor.includes(normalizedVariant) || normalizedVariant.includes(normalizedAuthor)) {
      return true;
    }
  }
  return false;
}

export default { generatePinyinVariants, matchAuthor };
