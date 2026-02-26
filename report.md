# SakshaAI — Project Report

Date: 26 Feb 2026

## Project Summary

SakshaAI is a hackathon prototype for an AI-powered corruption reporting system that lets citizens record bribe demands, automatically extracts evidence, drafts formal complaints, and (optionally) routes reports to appropriate authorities or trusted mediators while preserving anonymity.

The project purpose is to lower the practical and safety barriers that stop victims from reporting corruption: knowledge gaps, process complexity, and fear of retaliation.

## Problem Statement

- Millions of bribes occur yearly; a large majority are never reported.
- People often don't know where to report, fear retaliation, or find the complaint process opaque.
- Existing tools do not combine audio evidence collection, automated legal identification, and an anonymity-preserving submission flow.

## Solution Overview

SakshaAI provides a single streamlined flow:

1. User opens the app and records the interaction (one-party consent assumed where legal).
2. The browser transcribes audio in real time using the Web Speech API.
3. AI (Gemini) analyzes the transcript to extract: bribe amount, official name, department, likely law violations, evidence strength and recommended authority (ACB/Lokayukta/CVC).
4. A formal complaint letter is auto-generated and presented for review and optional editing.
5. User may file anonymously using recommended safe submission routes, or request a mediator (NGO/lawyer) to file on their behalf via the prototype mediator workflow.
6. Reports are aggregated into a public dashboard showing department breakdowns, heatmaps, and KPIs.

## Key Features

- Browser-based audio recording and live transcription (no server required for capture)
- Automatic evidence extraction (amount, official, department, violations)
- Auto-draft of formal complaint letters for authorities
- Anonymous mode and explicit anonymous-safe submission guidance
- Mediator channel for third-party filing and anonymized bundle generation
- Public dashboard with heatmap, department bars and recent reports

## Tech Stack

- Frontend: Plain HTML, CSS, vanilla JavaScript (no framework) — files: `index.html`, `report.html`, `dashboard.html`.
- Fonts: Google Fonts (`Syne`, `DM Sans`).
- Speech: Browser Web Speech API (real-time speech-to-text).
- AI: Google Gemini (optional) — client-side optional key; demo mode available when no key is provided.
- Backend (prototype): Python Flask app (`backend/app.py`) — serves static files, stores reports, mediations, and creates anonymized bundles.
- Storage: Local JSON files in `backend/data/` for hackathon prototype (`reports.json`, `mediations.json`, `mediators.json`).
- Dev/runtime: Python 3.x, `Flask`, `flask-cors`.

## Tools & Integrations

- Local development: `python -m http.server` (static) or run the Flask backend to serve and test mediator/report APIs.
- External AI: Google Gemini API (user-provided key or server-side proxy can be added).
- Optional: Object storage (S3) for production bundles; rate limiting / authentication for abuse protection.

## Architecture & Files

- Root frontend files: `index.html`, `report.html`, `dashboard.html` — single-page-style flows per feature.
- Backend service: `backend/app.py` — endpoints:
  - `POST /api/report` — accepts new reports (stored in `backend/data/reports.json`).
  - `GET /api/reports` — returns stored reports for dashboard.
  - `GET /api/summary` — returns KPIs and top departments.
  - `GET /api/mediators` — returns seeded mediator contacts.
  - `POST /api/mediate` — creates a mediation record and anonymized bundle.
- Data directory: `backend/data/` for JSON storage and `bundles/` for anonymized bundles.

## Workflow (User)

1. Setup: optional choose language and department, enable Anonymous Mode if desired.
2. Record: press the record button; Web Speech transcribes live into the transcript box.
3. Analyze: click “Analyze with Gemini AI” — with a Gemini key you get real model results; without a key you get Demo Mode where the app parses the transcript locally.
4. Review: the AI displays extracted fields, evidence rating, and recommended reporting authority.
5. Generate Complaint: produce a downloadable complaint letter, edit if needed.
6. File: user can download and submit manually, request a mediator to file on their behalf, or follow the anonymous-safe guidance.

## Security & Privacy Considerations

- Demo mode does not require keys and returns sample or locally parsed results.
- Client-provided API keys (Gemini) are currently entered by the user in the browser — this is convenient for demos but insecure for production.
- Recommended production change: host AI requests on the server side (proxy) using a single managed key, add rate limiting, abuse protection, and server-side logging controls.
- Anonymity: the app offers anonymous-safe submission guidance, a mediator path (third-party filing), and strips metadata from bundles; true anonymity cannot be guaranteed — advise users accordingly.

## How to Run Locally (Quick)

1. Clone or download the repo.
2. Recommended: run the Flask backend to serve files and APIs.

```powershell
cd sakshaai/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:5000/report.html` and `http://localhost:5000/dashboard.html`.

Alternative quick test: open `index.html` directly in a browser (no server), but mediator/backend features require the Flask backend.

## Demo Instructions (Hackathon pitch)

1. Open `report.html` (served via backend recommended).
2. Click “Use Demo Transcript” or record a short conversation using the record button.
3. Click “Analyze with Gemini AI” (leave key blank to use demo). Review extracted fields.
4. Click “Generate Complaint Letter”, edit if needed, then click “Mark as Filed”.
5. Optionally choose a mediator in Step 1; when filed the app will create an anonymized bundle and show a download link for the mediator.

## Limitations (Prototype)

- Data persistence is file-based and not suitable for production scale or concurrent write-heavy usage.
- No rate-limiting or authentication is implemented — add before public deployment.
- Mediator workflow is a simple prototype; real-world deployment requires partner agreements and secure routing.
- Audio files are not yet attached to bundles (only transcript); adding safe audio stripping and storage is suggested.

## Next Steps / Roadmap

1. Add server-side proxy for Gemini with secure key management and rate limiting.
2. Move storage to a database or object storage and add backup/retention policies.
3. Improve anonymization tooling (strip metadata, optionally transcode audio server-side).
4. Implement mediator workflow approval flow and secure notifications.
5. Add end-to-end tests, input validation, and basic unit tests for backend endpoints.
6. Polish copy/UX and externalize CSS/JS into modular files.

## Contact / Authors

Project created as a hackathon prototype. See repo files for authorship and contact information.

---

Generated automatically for the hackathon demo; use this report in presentation slides or README.
