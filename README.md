# Campus Complaint Management System

A full-stack campus complaint management system built with React and FastAPI.

## Stack
- Frontend: React + Vite
- Backend: Python + FastAPI
- Database: SQLite (development)
- API docs: OpenAPI / Swagger

## Project structure
```
frontend/   React web application
backend/    FastAPI REST API
```

## Development
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Backend API: http://localhost:8000  
Swagger docs: http://localhost:8000/docs
