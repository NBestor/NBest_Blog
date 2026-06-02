# Private Blog System

阶段 1：项目工程化初始化。

## Tech Stack

- Frontend: React 18, React Router, Axios, ESLint, Prettier, Vite
- Backend: FastAPI, SQLite, CORS, local static resources

## Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check: `http://localhost:8000/api/health`

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`
