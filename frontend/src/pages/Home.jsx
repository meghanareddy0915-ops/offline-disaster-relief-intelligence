function Home() {
  return (
    <div style={{ padding: "30px" }}>
      <h1>Welcome</h1>

      <p>
        An offline AI system that converts disaster relief requests into
        structured data.
      </p>

      <button>Upload File</button>

      <h3>Features</h3>

      <ul>
        <li>Offline First</li>
        <li>CPU Optimized</li>
        <li>Local AI Processing</li>
        <li>SQLite Storage</li>
      </ul>
    </div>
  );
}

export default Home;