# Dad of Anton

A full-stack application with FastAPI backend and Next.js frontend, integrated with Supabase.

## Project Structure

```
dad-of-anton/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── api/v1/
│   │   └── core/
│   ├── .env
│   └── requirements.txt
├── frontend/          # Next.js application
│   ├── app/
│   ├── lib/
│   └── package.json
└── start.sh           # Start both applications
```

## Prerequisites

- Python 3.9+
- Node.js 18+
- Supabase account (for database)

## Setup

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Frontend

```bash
cd frontend
npm install
```

### 3. Environment Variables

Copy `.env.example` to `.env` in the backend folder and add your Supabase credentials:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

## Running the Application

### Quick Start (Recommended)

```bash
./start.sh
```

This will start both servers:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### Manual Start

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/health | Health check |

## Tech Stack

- **Backend:** FastAPI, Pydantic, Supabase
- **Frontend:** Next.js 15, React 19, TypeScript
- **Database:** Supabase (PostgreSQL)
