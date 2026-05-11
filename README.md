# NearDeals 📍

> **Hyperlocal Deals Discovery Platform**  
> Full-stack college project — Geolocation filtering + Interactive Map + AI Deal Assistant

---

## 🗂 Project Structure

```
neardeals/
├── frontend/
│   └── index.html          # Single-page app (HTML + CSS + JS)
├── backend/
│   ├── main.py             # FastAPI backend
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variable template
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python 3.10+, FastAPI, Uvicorn |
| AI Assistant | Anthropic API (proxied via backend) |
| Geolocation | Browser Geolocation API + OpenStreetMap Nominatim |
| Maps | Google Maps Embed API |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/neardeals.git
cd neardeals
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run the server
uvicorn main:app --reload --port 8000
```

API live at → `http://localhost:8000`  
Swagger docs → `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend

# Option A — open directly in browser
open index.html

# Option B — serve locally (avoids CORS issues)
python -m http.server 3000
# Visit http://localhost:3000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/deals` | Fetch deals `?radius=5&cat=all&sort=distance` |
| GET | `/deals/{id}` | Single deal detail |
| GET | `/stats` | Dashboard stats `?radius=5` |
| POST | `/book` | Book a table |
| POST | `/register-shop` | Submit shop for listing |
| POST | `/ai-chat` | AI deal assistant |

---

## ✨ Features

- 📍 Geolocation-based filtering with adjustable radius
- 🗺 Interactive map with deal pins + Google Maps live embed
- 🤖 AI Deal Assistant (natural language queries via FastAPI)
- 🪑 Table booking — seat selector, time slots, guest count
- 📦 Live stock tracking on grocery/pharmacy cards
- ❤️ Save/bookmark favourite deals
- ⏰ Expiry alerts for urgent deals
- 📱 Fully responsive — mobile + desktop

---

## 📌 Notes

- Deals stored **in-memory** for this prototype — swap with SQLite/PostgreSQL for production.
- AI API key stays on the server — never exposed to the browser.
- Reverse geocoding via OpenStreetMap Nominatim (free, no key needed).

---

## 👤 Author

**[Your Name]** · Dept. of Computer Science · [College] · [Year]
