from fastapi import FastAPI
from database.database import create_table

app = FastAPI(
    title="Offline Disaster Relief Intelligence API",
    version="1.0.0"
)

create_table()

@app.get("/")
def home():
    return {"message": "Offline Disaster Relief Intelligence API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/upload")
def upload():
    return {"message": "Upload endpoint is ready"}