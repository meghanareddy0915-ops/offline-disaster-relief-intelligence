# Offline Disaster Relief Intelligence

CPU-first Streamlit MVP for converting unstructured disaster-relief field notes into structured JSON records. The whole demo now runs from the repository root through `app.py`.

## Phase 2 Demo

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

3. Paste or upload a text field report.
4. Click `Extract JSON`.
5. Show the structured dataset, SQLite record count, confidence, and latency.
6. Turn Wi-Fi off and repeat extraction locally to prove the core workflow is offline and CPU-only.

## Streamlit Cloud Settings

Use these exact values:

```txt
Repository: meghanareddy0915-ops/offline-disaster-relief-intelligence
Branch: main
Main file path: app.py
```

The public Streamlit link is only for access. The offline-first proof should be shown locally with `streamlit run app.py`.

## Input Scope

The MVP supports text-like records: pasted field notes, OCR text, transcripts, `.txt`, `.csv`, `.md`, and `.json` files.

## Local Runtime Declaration

- App runtime: Streamlit
- Processing: local deterministic CPU extraction
- Cloud AI APIs: none
- Storage: local SQLite database, `disaster_relief.db`
- Output: structured JSON and downloadable JSON export

## Extracted Schema

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

## Validation

```bash
python -m py_compile app.py
```

## License

This project is licensed under the GPL-3.0 License.
