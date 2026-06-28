import UploadForm from "../components/UploadForm";

function Upload() {
  return (
    <main className="page-shell">
      <section className="intro">
        <div>
          <p className="eyebrow">Phase 2 MVP</p>
          <h1>Offline relief request intelligence</h1>
          <p>
            Convert messy field notes, OCR text or transcripts into a clean disaster-response schema.
            The demo runs fully in-browser on CPU and persists records without a network.
          </p>
        </div>
        <div className="runtime-strip">
          <span>Runtime: browser CPU</span>
          <span>Storage: local cache</span>
          <span>Network: optional</span>
        </div>
      </section>
      <UploadForm />
    </main>
  );
}

export default Upload;
