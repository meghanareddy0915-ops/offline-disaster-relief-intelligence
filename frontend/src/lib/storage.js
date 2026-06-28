const STORAGE_KEY = "offline-relief-records-v1";

export function loadRecords() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

export function saveRecord(record) {
  const records = [record, ...loadRecords()].slice(0, 50);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
  return records;
}

export function clearRecords() {
  localStorage.removeItem(STORAGE_KEY);
}

export function exportRecords(records) {
  const payload = JSON.stringify(records, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  return URL.createObjectURL(blob);
}
