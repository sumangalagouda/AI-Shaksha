# Backend for SakshaAI (Prototype)

This lightweight Flask backend is a simple prototype to collect anonymous reports and provide a minimal API for the dashboard.

Run locally (recommended in a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The backend will start on port `5000` and serves the static frontend files from the project root. API endpoints:

- `POST /api/report` — add a report (JSON)
- `GET  /api/reports` — list reports
- `GET  /api/summary` — basic KPIs

Data is stored in `backend/data/reports.json` (simple JSON append for hackathon demo).
