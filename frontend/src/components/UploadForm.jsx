function UploadForm() {
  return (
    <div style={{ marginTop: "20px" }}>
      <input type="file" />

      <br />
      <br />

      <button>Upload File</button>

      <p>
        Supported formats: PDF, JPG, PNG, TXT
      </p>
    </div>
  );
}

export default UploadForm;