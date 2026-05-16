import Dexie, { Table } from "dexie";
import { Staff, Institution, WOSRecord, MatchResult } from "../types";

export class WOSDatabase extends Dexie {
  staff!: Table<Staff, number>;
  institutions!: Table<Institution, number>;
  wosRecords!: Table<WOSRecord, string>;
  matchResults!: Table<MatchResult, string>;

  constructor() {
    super("WOSMatchingTool");
    this.version(1).stores({
      staff: "++id, department, name",
      institutions: "++id, nameCn, nameEn",
      wosRecords: "++id, ut, pt",
      matchResults: "++id, wosRecord.id, matchType"
    });
  }
}

export const db = new WOSDatabase();

export default { db };
