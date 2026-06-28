import { useMemo, useState } from "react";
import { extractReliefRecord } from "../lib/extractor";
import { clearRecords, exportRecords, loadRecords, saveRecord } from "../lib/storage";

const SAMPLE_TEXT =
  "URGENT: 38 people trapped near River View Colony. Drinking water, food packets, blankets and medical help needed. Contact +91 98765 43210. Flood water rising.";

function UploadForm() {
  const [text, setText] = useState(SAMPLE_TEXT);
  const [fileName, setFileName] = useState("sample-field-report.txt");
  const [records, setRecords] = useState(() => loadRecords());
  const [status, setStatus] = useState("Ready for offline CPU processing");
  const [isProcessing, setIsProcessing] = useState(false);

  const latestRecord = records[0];
  const metrics = useMemo(() => {
    const highPriority = records.filter((record) => ["critical", "high"].includes(record.urgency)).length;
    const avgLatency = records.length
      ? Math.round(records.reduce((sum, record) => sum + record.latencyMs, 0) / records.length)
      : 0;
    return { highPriority, avgLatency };
  }, [records]);

  async function handleFileChange(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setStatus("Reading file locally");

    if (!file.type.includes("text") && !file.name.match(/\.(txt|csv|md|json)$/i)) {
      setStatus("This MVP accepts text-like records. Paste OCR/transcript text for images, PDFs, audio or video.");
      return;
    }

    setText(await file.text());
    setStatus("File loaded without network access");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!text.trim()) {
      setStatus("Add a request note or upload a text record first.");
      return;
    }

    setIsProcessing(true);
    setStatus("Normalizing text and extracting structured relief fields on CPU");

    try {
      const record = await extractReliefRecord({ text, fileName });
      setRecords(saveRecord(record));
      setStatus(`Stored locally with ${record.confidence}% schema confidence`);
    } catch (error) {
      setStatus(`Processing failed gracefully: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  }

  function handleExport() {
    const url = exportRecords(records);
    const link = document.createElement("a");
    link.href = url;
    link.download = "offline-relief-records.json";
    link.click();
    URL.revokeObjectURL(url);
  }

  function handleClear() {
    clearRecords();
    setRecords([]);
    setStatus("Local cache cleared");
  }

  return (
    <section className="workspace">
      <form className="ingest-panel" onSubmit={handleSubmit}>
        <label className="field-label" htmlFor="record-file">
          Disaster record
        </label>
        <input id="record-file" type="file" accept=".txt,.csv,.md,.json,text/*" onChange={handleFileChange} />

        <label className="field-label" htmlFor="record-text">
          OCR, transcript or field-note text
        </label>
        <textarea
          id="record-text"
          value={text}
          onChange={(event) => setText(event.target.value)}
          rows={10}
          spellCheck="true"
        />

        <div className="actions">
          <button type="submit" disabled={isProcessing}>
            {isProcessing ? "Processing..." : "Extract JSON"}
          </button>
          <button type="button" className="secondary" onClick={handleExport} disabled={!records.length}>
            Export
          </button>
          <button type="button" className="secondary" onClick={handleClear} disabled={!records.length}>
            Clear
          </button>
        </div>

        <p className="status">{status}</p>
      </form>

      <div className="output-panel">
        <div className="metrics">
          <div>
            <span>{records.length}</span>
            <small>cached records</small>
          </div>
          <div>
            <span>{metrics.highPriority}</span>
            <small>high priority</small>
          </div>
          <div>
            <span>{metrics.avgLatency}ms</span>
            <small>avg latency</small>
          </div>
        </div>

        {latestRecord ? (
          <div className="record-view">
            <div className={`urgency ${latestRecord.urgency}`}>{latestRecord.urgency}</div>
            <h2>{latestRecord.summary}</h2>
            <dl>
              <div>
                <dt>Location</dt>
                <dd>{latestRecord.location || "Needs review"}</dd>
              </div>
              <div>
                <dt>People affected</dt>
                <dd>{latestRecord.peopleAffected || "Unknown"}</dd>
              </div>
              <div>
                <dt>Needs</dt>
                <dd>{latestRecord.needs.length ? latestRecord.needs.join(", ") : "Needs review"}</dd>
              </div>
              <div>
                <dt>Contact</dt>
                <dd>{latestRecord.contact.phone || latestRecord.contact.email || "Not found"}</dd>
              </div>
            </dl>
            <pre>{JSON.stringify(latestRecord, null, 2)}</pre>
          </div>
        ) : (
          <div className="empty-state">
            <h2>No structured records yet</h2>
            <p>Process a real field note to create a locally cached JSON record.</p>
          </div>
        )}
      </div>
    </section>
  );
}

export default UploadForm;
