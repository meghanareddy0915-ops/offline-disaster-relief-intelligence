import argparse
import json
import re
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("disaster_relief.db")

SUPPLY_KEYWORDS = {
    "water": ["water", "drinking", "bottle", "litre", "liter"],
    "food": ["food", "meal", "rice", "ration", "milk", "baby food"],
    "shelter": ["shelter", "tent", "tarpaulin", "blanket", "camp"],
    "medical": ["medicine", "medical", "doctor", "first aid", "insulin", "injured"],
    "rescue": ["rescue", "trapped", "evacuate", "evacuation", "boat"],
    "power": ["power", "electricity", "generator", "charging", "lights"],
}


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS disaster_requests (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                source_file TEXT NOT NULL,
                location TEXT,
                urgency TEXT NOT NULL,
                needs TEXT NOT NULL,
                people_affected INTEGER NOT NULL,
                contact TEXT NOT NULL,
                summary TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                runtime TEXT NOT NULL,
                latency_ms INTEGER NOT NULL,
                raw_text TEXT NOT NULL
            )
            """
        )


def normalize_text(text):
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def unique(values):
    seen = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return seen


def find_people(text):
    patterns = [
        r"\b(?:people|persons|families|children|patients)\s*[:-]?\s*(\d{1,5})",
        r"\b(\d{1,5})\s+(?:people|persons|families|children|patients)\b",
    ]
    values = []
    for pattern in patterns:
        values.extend(int(match) for match in re.findall(pattern, text, flags=re.I))
    return max(values) if values else 0


def find_contact(text):
    phone = re.search(r"(?:\+?\d[\d\s-]{7,}\d)", text)
    email = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", text, flags=re.I)
    return {
        "phone": re.sub(r"\s+", " ", phone.group(0)).strip() if phone else "",
        "email": email.group(0) if email else "",
    }


def find_location(text):
    patterns = [
        r"\b(?:at|near|from|in)\s+([A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*){0,4})",
        r"\blocation\s*[:-]\s*([^\n,.;]+)",
        r"\baddress\s*[:-]\s*([^\n.;]+)",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, text, flags=re.I):
            location = re.sub(r"\s+", " ", match).strip()
            if len(location) > 2 and not re.search(
                r"\b(help|water|food|urgent)\b", location, flags=re.I
            ):
                return location
    return ""


def find_needs(text):
    lower = text.lower()
    return [
        category
        for category, words in SUPPLY_KEYWORDS.items()
        if any(word in lower for word in words)
    ]


def find_urgency(text):
    lower = text.lower()
    if any(
        word in lower
        for word in [
            "critical",
            "sos",
            "trapped",
            "life threatening",
            "immediate",
            "urgent",
        ]
    ):
        return "critical"
    if any(
        word in lower
        for word in ["flood", "injured", "no food", "no water", "evacuate", "medical"]
    ):
        return "high"
    if "soon" in lower or "within 24" in lower:
        return "medium"
    return "low"


def build_summary(record):
    people = (
        f"{record['peopleAffected']} people"
        if record["peopleAffected"]
        else "affected residents"
    )
    place = f" near {record['location']}" if record["location"] else ""
    needs = ", ".join(record["needs"]) if record["needs"] else "general relief"
    return f"{people}{place} need {needs}."


def score_confidence(record):
    checks = [
        bool(record["location"]),
        bool(record["peopleAffected"]),
        bool(record["needs"]),
        bool(record["contact"]["phone"] or record["contact"]["email"]),
        record["urgency"] != "low",
    ]
    return round((sum(checks) / len(checks)) * 100)


def extract_record(text, source_file):
    started = time.perf_counter()
    normalized = normalize_text(text)
    record = {
        "id": str(uuid.uuid4()),
        "sourceFile": source_file,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "location": find_location(normalized),
        "urgency": find_urgency(normalized),
        "needs": unique(find_needs(normalized)),
        "peopleAffected": find_people(normalized),
        "contact": find_contact(normalized),
        "rawText": normalized,
    }
    record["summary"] = build_summary(record)
    record["confidence"] = score_confidence(record)
    record["runtime"] = "Local CPU CLI extractor + SQLite"
    record["latencyMs"] = round((time.perf_counter() - started) * 1000)
    return record


def save_record(record):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO disaster_requests (
                id, created_at, source_file, location, urgency, needs, people_affected,
                contact, summary, confidence, runtime, latency_ms, raw_text
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["createdAt"],
                record["sourceFile"],
                record["location"],
                record["urgency"],
                json.dumps(record["needs"]),
                record["peopleAffected"],
                json.dumps(record["contact"]),
                record["summary"],
                record["confidence"],
                record["runtime"],
                record["latencyMs"],
                record["rawText"],
            ),
        )


def read_input(args):
    if args.text:
        return args.text, "inline-text"
    if args.input:
        path = Path(args.input)
        return path.read_text(encoding="utf-8"), str(path)
    raise SystemExit('Provide --input path/to/file.txt or --text "request text"')


def main():
    parser = argparse.ArgumentParser(
        description="Offline disaster relief JSON extractor"
    )
    parser.add_argument("--input", help="Path to a text-like disaster request file")
    parser.add_argument("--text", help="Inline disaster request text")
    parser.add_argument(
        "--no-save", action="store_true", help="Print JSON without saving to SQLite"
    )
    args = parser.parse_args()

    text, source_file = read_input(args)
    init_db()
    record = extract_record(text, source_file)
    if not args.no_save:
        save_record(record)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
