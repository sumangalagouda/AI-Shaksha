# ⚖️ SakshaAI — AI-Powered Corruption Reporter

> *India's first AI-powered corruption reporting platform. Built at Hackathon.*

---

## 🚀 Quick Start

No installation needed. Just open the HTML files in a browser.

```
index.html      → Landing page
report.html     → Report a bribe (main feature)
dashboard.html  → City corruption dashboard
```

```bash
# Option 1: Open directly
# (Windows: double-click index.html)

# Option 2: Simple server
python -m http.server 3000
# Then visit http://localhost:3000

---

## 🔑 API Key Setup

On the Report page, enter your API key:

| Key | Where to Get |
|-----|-------------|
| Google Gemini API Key | aistudio.google.com/app/apikey |


Optional backend prototype (collect reports)
------------------------------------------
This repo includes a minimal Flask prototype in `backend/` that stores posted reports to a JSON file and provides a small API used by dashboards.

Run the backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Frontend files are served by the backend at http://localhost:5000 when the backend is running.
**No key? Use Demo Mode** — full AI simulation with sample data.

---

## 🧩 Features

### Report Page (`report.html`)
- 🎙️ Browser-based audio recording
- 📝 Web Speech live transcription (Hindi, Tamil, Telugu, etc.)
- 🧠 Gemini AI corruption analysis
- 📊 Evidence scoring (STRONG/MODERATE/WEAK)
- ⚖️ Automatic law identification (PCA 1988)
- 🎯 Smart routing to correct authority
- 📄 Auto-generated formal complaint letter
- 🔒 Anonymous mode

### Dashboard (`dashboard.html`)
- 📈 Live activity heatmap
- 🏛️ Department breakdown
- 🗺️ City hotspot map
- 📊 Monthly trend charts
- 📋 Recent anonymous reports table
- 🌆 Multi-city support

---

## 🛠️ Tech Stack

```
Frontend    React-free vanilla JS + HTML/CSS
AI          Google Gemini API (gemini-1.5-flash)
Voice       Browser Web Speech API
Fonts       Syne + DM Sans (Google Fonts)
Charts      Pure CSS animations
No backend  required for demo
```

---

## ⚖️ Legal Disclaimer

- Recording is legal under Indian one-party consent law when you are party to the conversation
- SakshaAI provides a reporting tool only — not legal advice
- Complaints are submitted to authorities for investigation
- Evidence is not submitted directly to courts

---

## 📁 File Structure

```
sakshaai/
├── index.html      # Landing page
├── report.html     # Main reporting interface  
├── dashboard.html  # Public corruption dashboard
└── README.md       # This file
```

---

## 🏆 Built for  Hackathon

**Problem:** 15 million bribes paid annually in India. 97% never reported.
**Solution:** Record → AI analyzes → Complaint filed in 60 seconds.
**Impact:** Crowdsourced corruption intelligence for systemic change.

---

## 💬 Demo Script

1. Open `report.html`
2. Click "Use Demo Transcript"
3. Click "Analyze with AI" (uses demo data without keys)
4. View evidence analysis
5. Generate complaint letter
6. Download and "file"
7. Check `dashboard.html` for city-wide impact

---

*Built with ❤️ for India. Every complaint counts.*
