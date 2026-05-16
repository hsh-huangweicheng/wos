import { Staff } from "../types";

export function deduplicateStaff(staff: Staff[]): Staff[] {
  const seen = new Map<string, Staff>();
  
  for (const s of staff) {
    const key = `${s.name}-${s.department}`;
    if (!seen.has(key)) {
      seen.set(key, s);
    }
  }
  
  return Array.from(seen.values());
}

export default { deduplicateStaff };
