from fastapi import FastAPI

app = FastAPI(
    title="Offline Disaster Relief Intelligence API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Offline Disaster Relief Intelligence API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }