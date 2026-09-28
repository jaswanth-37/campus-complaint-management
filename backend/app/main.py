from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Campus Complaint Management API",
    version="0.1.0",
    description="REST API for campus complaint management.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "campus-complaint-management"}

@app.get("/api/complaints")
def list_complaints():
    return []
