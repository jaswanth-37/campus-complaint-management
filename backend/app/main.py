from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routes_auth import router as auth_router
from .routes_complaints import router as complaints_router
from .routes_admin import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus Complaint Management API",
    version="0.2.0",
    description="REST API for campus complaint management.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads", check_dir=False), name="uploads")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "campus-complaint-management"}

app.include_router(auth_router)
app.include_router(complaints_router)
app.include_router(admin_router)
