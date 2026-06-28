import json
import re
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st


DB_PATH = Path("relief_records.sqlite3")

SUPPLY_KEYWORDS = {
    "water": ["water", "drinking", "bottle", "litre", "liter"],
    "food": ["food", "meal", "rice", "ration", "milk", "baby food"],
    "shelter": ["shelter", "tent", "tarpaulin", "blanket", "camp"],
    "medical": ["medicine", "medical", "doctor", "first aid", "insulin", "injured"],
    "rescue": ["rescue", "trapped", "evacuate", "evacuation", "boat"],
    "power": ["power", "electricity", "generator", "charging", "lights"],
}

SAMPLE_TEXT = (
    "URGENT: 38 people trapped near River View Colony. Drinking water, food packets, "
    "blankets and medical help needed. Contact +91 98765 43210. Flood water rising."
)


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS relief_records (
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
        clean = value.strip()
        if clean and clean not in seen:
            seen.append(clean)
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
            if len(location) > 2 and not re.search(r"\b(help|water|food|urgent)\b", location, flags=re.I):
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
    critical = ["critical", "sos", "trapped", "life threatening", "immediate", "urgent"]
    high = ["flood", "injured", "no food", "no water", "evacuate", "medical"]
    if any(word in lower for word in critical):
        return "critical"
    if any(word in lower for word in high):
        return "high"
    if "soon" in lower or "within 24" in lower:
        return "medium"
    return "low"


def build_summary(record):
    people = f"{record['peopleAffected']} people" if record["peopleAffected"] else "affected residents"
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


def extract_relief_record(text, source_file):
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
    record["runtime"] = "Local CPU heuristic extractor v1 - Streamlit"
    record["latencyMs"] = round((time.perf_counter() - started) * 1000)
    return record


def save_record(record):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO relief_records (
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


def load_records():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM relief_records ORDER BY created_at DESC LIMIT 50"
        ).fetchall()

    records = []
    for row in rows:
        records.append(
            {
                "id": row["id"],
                "sourceFile": row["source_file"],
                "createdAt": row["created_at"],
                "location": row["location"],
                "urgency": row["urgency"],
                "needs": json.loads(row["needs"]),
                "peopleAffected": row["people_affected"],
                "contact": json.loads(row["contact"]),
                "summary": row["summary"],
                "confidence": row["confidence"],
                "runtime": row["runtime"],
                "latencyMs": row["latency_ms"],
                "rawText": row["raw_text"],
            }
        )
    return records


def clear_records():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM relief_records")


st.set_page_config(
    page_title="Offline Disaster Relief Intelligence",
    page_icon="🧭",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    .status-card {
        border: 1px solid #d7e2d2;
        border-radius: 8px;
        padding: 14px;
        background: #f5f8f2;
    }
    .runtime-note {
        color: #53615a;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_db()

st.title("Offline Disaster Relief Intelligence")
st.caption("CPU-first Streamlit MVP: unstructured field notes to structured local records.")

left, right = st.columns([0.95, 1.05], gap="large")

with left:
    st.subheader("Ingest")
    uploaded_file = st.file_uploader(
        "Upload text-like disaster record",
        type=["txt", "csv", "md", "json"],
    )

    source_file = "manual-entry.txt"
    initial_text = SAMPLE_TEXT
    if uploaded_file is not None:
        source_file = uploaded_file.name
        initial_text = uploaded_file.read().decode("utf-8", errors="replace")

    text = st.text_area(
        "OCR, transcript or field-note text",
        value=initial_text,
        height=260,
    )

    col_a, col_b = st.columns(2)
    extract_clicked = col_a.button("Extract JSON", type="primary", use_container_width=True)
    clear_clicked = col_b.button("Clear cache", use_container_width=True)

    st.markdown(
        """
        <div class="status-card">
        <strong>Runtime declaration</strong><br>
        Local CPU-only extraction, SQLite persistence, no OpenAI/Anthropic/cloud AI calls.
        </div>
        """,
        unsafe_allow_html=True,
    )

if clear_clicked:
    clear_records()
    st.success("Local SQLite cache cleared.")

if extract_clicked:
    if not text.strip():
        st.warning("Paste or upload a disaster request first.")
    else:
        with st.spinner("Processing locally on CPU..."):
            record = extract_relief_record(text, source_file)
            save_record(record)
        st.success(f"Stored locally with {record['confidence']}% schema confidence.")

records = load_records()
latest = records[0] if records else None
high_priority = sum(1 for record in records if record["urgency"] in {"critical", "high"})
avg_latency = round(sum(record["latencyMs"] for record in records) / len(records)) if records else 0

with right:
    st.subheader("Structured output")
    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Cached records", len(records))
    metric_b.metric("High priority", high_priority)
    metric_c.metric("Avg latency", f"{avg_latency} ms")

    if latest:
        st.markdown(f"### {latest['summary']}")
        detail_a, detail_b = st.columns(2)
        detail_a.info(f"Urgency: {latest['urgency'].upper()}")
        detail_b.info(f"Confidence: {latest['confidence']}%")

        st.json(latest)
        st.download_button(
            "Download all records as JSON",
            data=json.dumps(records, indent=2),
            file_name="offline-relief-records.json",
            mime="application/json",
            use_container_width=True,
        )
    else:
        st.info("No records yet. Process a field note to create the first structured JSON record.")

st.markdown(
    """
    <p class="runtime-note">
    Demo note: the Streamlit app can be hosted for a public URL, but the hackathon offline proof
    should be shown by running this app locally with the network switched off.
    </p>
    """,
    unsafe_allow_html=True,
)
