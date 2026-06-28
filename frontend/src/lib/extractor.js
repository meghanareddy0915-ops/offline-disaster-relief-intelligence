const SUPPLY_KEYWORDS = {
  water: ["water", "drinking", "bottle", "litre", "liter"],
  food: ["food", "meal", "rice", "ration", "milk", "baby food"],
  shelter: ["shelter", "tent", "tarpaulin", "blanket", "camp"],
  medical: ["medicine", "medical", "doctor", "first aid", "insulin", "injured"],
  rescue: ["rescue", "trapped", "evacuate", "evacuation", "boat"],
  power: ["power", "electricity", "generator", "charging", "lights"],
};

const LOCATION_HINTS = [
  /\b(?:at|near|from|in)\s+([A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*){0,4})/g,
  /\blocation\s*[:-]\s*([^\n,.;]+)/gi,
  /\baddress\s*[:-]\s*([^\n.;]+)/gi,
];

function normalizeText(text) {
  return text
    .replace(/\r/g, "\n")
    .replace(/[ \t]+/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function unique(values) {
  return [...new Set(values.filter(Boolean).map((value) => value.trim()))];
}

function findPeople(text) {
  const explicit = [...text.matchAll(/\b(?:people|persons|families|children|patients)\s*[:-]?\s*(\d{1,5})/gi)]
    .map((match) => Number(match[1]));
  const contextual = [...text.matchAll(/\b(\d{1,5})\s+(?:people|persons|families|children|patients)\b/gi)]
    .map((match) => Number(match[1]));
  return Math.max(0, ...explicit, ...contextual);
}

function findContact(text) {
  const phone = text.match(/(?:\+?\d[\d\s-]{7,}\d)/);
  const email = text.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i);
  return {
    phone: phone ? phone[0].replace(/\s+/g, " ").trim() : "",
    email: email ? email[0] : "",
  };
}

function findLocation(text) {
  for (const pattern of LOCATION_HINTS) {
    const matches = [...text.matchAll(pattern)].map((match) => match[1].trim());
    const likely = matches.find((match) => match.length > 2 && !/\b(help|water|food|urgent)\b/i.test(match));
    if (likely) return likely.replace(/\s+/g, " ");
  }
  return "";
}

function findSupplies(text) {
  const lower = text.toLowerCase();
  return Object.entries(SUPPLY_KEYWORDS)
    .filter(([, words]) => words.some((word) => lower.includes(word)))
    .map(([category]) => category);
}

function findUrgency(text) {
  const lower = text.toLowerCase();
  const critical = ["critical", "sos", "trapped", "life threatening", "immediate", "urgent"];
  const high = ["flood", "injured", "no food", "no water", "evacuate", "medical"];
  if (critical.some((word) => lower.includes(word))) return "critical";
  if (high.some((word) => lower.includes(word))) return "high";
  if (lower.includes("soon") || lower.includes("within 24")) return "medium";
  return "low";
}

function buildSummary(fields) {
  const needs = fields.needs.length ? fields.needs.join(", ") : "general relief";
  const people = fields.peopleAffected ? `${fields.peopleAffected} people` : "affected residents";
  const place = fields.location ? ` near ${fields.location}` : "";
  return `${people}${place} need ${needs}.`;
}

function scoreConfidence(fields) {
  const checks = [
    Boolean(fields.location),
    Boolean(fields.peopleAffected),
    fields.needs.length > 0,
    Boolean(fields.contact.phone || fields.contact.email),
    fields.urgency !== "low",
  ];
  return Math.round((checks.filter(Boolean).length / checks.length) * 100);
}

export async function extractReliefRecord({ text, fileName = "manual-entry" }) {
  const startedAt = performance.now();
  const normalized = normalizeText(text);
  await new Promise((resolve) => window.setTimeout(resolve, 160));

  const fields = {
    id: crypto.randomUUID(),
    sourceFile: fileName,
    createdAt: new Date().toISOString(),
    location: findLocation(normalized),
    urgency: findUrgency(normalized),
    needs: unique(findSupplies(normalized)),
    peopleAffected: findPeople(normalized),
    contact: findContact(normalized),
    rawText: normalized,
  };

  return {
    ...fields,
    summary: buildSummary(fields),
    confidence: scoreConfidence(fields),
    runtime: "Local CPU heuristic extractor v1",
    latencyMs: Math.round(performance.now() - startedAt),
  };
}
