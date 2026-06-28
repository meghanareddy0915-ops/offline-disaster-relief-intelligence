import UploadForm from "../components/UploadForm";

function Upload() {
  return (
    <div style={{ padding: "30px" }}>
      <h1>Upload Disaster Request</h1>

      <p>
        Upload a disaster request document or image for processing.
      </p>

      <UploadForm />
    </div>
  );
}

export default Upload;