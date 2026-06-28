# Offline Disaster Relief Intelligence

CPU-first Streamlit MVP for turning unstructured disaster-relief field notes into structured JSON records. The core extraction workflow runs locally with no cloud AI APIs.

## Phase 2 Demo

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the Streamlit app:

```bash
streamlit run app.py
```

3. Open the local URL shown by Streamlit.
4. Paste or upload a text field report.
5. Click `Extract JSON`.
6. Show the structured JSON, latency, confidence, and local record count.
7. Turn the network off and repeat extraction locally to demonstrate CPU-first offline behavior.

## Public Link

For a public demo link, deploy `app.py` on Streamlit Community Cloud.

- Main file path: `app.py`
- Requirements file: `requirements.txt`

Important: the public Streamlit link is only for access and judging convenience. The offline hackathon proof should be demonstrated by running `streamlit run app.py` locally with the network switched off.

## Input Scope

The current MVP supports text-like inputs: `.txt`, `.csv`, `.md`, `.json`, pasted OCR text, pasted transcript text, or copied field notes. Image, PDF, audio and video records can pass through the same flow after OCR/transcription text is available.

## Local AI Runtime Declaration

- Runtime: Python + Streamlit on CPU.
- Model approach: deterministic local extractor for disaster-response schema mapping.
- Cloud calls: none.
- Storage: local SQLite database, `relief_records.sqlite3`.
- Export: JSON download from the app.

## Extracted Schema

Each request is normalized into:

- `id`
- `sourceFile`
- `createdAt`
- `location`
- `urgency`
- `needs`
- `peopleAffected`
- `contact`
- `summary`
- `confidence`
- `runtime`
- `latencyMs`
- `rawText`

## Example Input

```txt
SOS: 52 people near Lake Road School need drinking water, food, blankets and medical help. Two children injured. Contact +91 90000 11111.
```

## Validation Commands

```bash
python -m py_compile app.py
```

The older Vite React frontend is still present in `src/`, but the Streamlit MVP entry point is `app.py`.
