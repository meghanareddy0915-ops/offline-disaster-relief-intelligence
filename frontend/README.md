# Offline Disaster Relief Intelligence

CPU-first web MVP for turning unstructured disaster-relief field notes into structured JSON records. The core workflow runs locally in the browser with no cloud APIs.

## Phase 2 Demo

1. Run `npm install` if dependencies are not present.
2. Start the app with `npm run dev`.
3. Open `http://127.0.0.1:5173`.
4. Paste or upload a text field report.
5. Click `Extract JSON`.
6. Switch the network off and refresh after the first load to demonstrate the offline app shell and local cache.

## Input Scope

The current MVP supports text-like inputs: `.txt`, `.csv`, `.md`, `.json`, pasted OCR text, pasted transcript text, or copied field notes. Image, PDF, audio and video records can be passed through the same flow after OCR/transcription text is available.

## Local AI Runtime Declaration

- Runtime: browser JavaScript on CPU.
- Model approach: deterministic small local extractor for disaster-response schema mapping.
- Cloud calls: none.
- Storage: browser `localStorage` cache with JSON export.
- Offline support: service worker caches app shell and assets after first load.

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

## Validation Commands

```bash
npm run lint
npm run build
```
