<<<<<<< HEAD
# AI Web Monitoring & Trend Detection Agent

An autonomous system that continuously scrapes AI & Technology news sources, detects emerging trends using keyword frequency and topic velocity analysis, and presents AI-generated insights on a real-time web dashboard.

**100% Local. No paid APIs. No Docker. No cloud services.**

---

## Screenshots

### Dashboard - Stats, Active Keywords & Top Trends
![Dashboard](screenshots/1.png)

### Trend Detail - Velocity History Chart
![Trend Detail](screenshots/2.png)

### Trend Detail - Related Articles
![Related Articles](screenshots/3.png)

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Ollama ([ollama.com](https://ollama.com)) - for AI insights (optional, app works without it)

## Quick Start

```bash
# 1. Install Ollama and pull the model (one time, ~4GB download)
ollama pull llama3

# 2. Install backend dependencies
cd backend
pip install -r requirements.txt

# 3. Install frontend dependencies
cd ../frontend
npm install

# 4. Start everything
cd ..
chmod +x start.sh
./start.sh
```

Open [http://localhost:3000](http://localhost:3000) to view the dashboard.

## Architecture

```
trend-agent/
├── backend/          Python FastAPI + SQLite + APScheduler
│   ├── app/
│   │   ├── api/          REST API endpoints
│   │   ├── models/       SQLAlchemy ORM models
│   │   ├── schemas/      Pydantic response schemas
│   │   ├── services/     RSS fetcher, trend analyzer, AI analyst, scheduler
│   │   └── utils/        Text cleaning, deduplication
│   └── run.py            One-command backend startup
│
├── frontend/         Next.js 14 + Tailwind CSS + Recharts + SWR
│   ├── app/              Pages (dashboard, trend detail, insights)
│   ├── components/       UI components (stats, charts, feeds, cards)
│   └── lib/              API client + SWR hooks
│
└── start.sh          Start both backend & frontend
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy (async), SQLite |
| Frontend | Next.js 14, React 18, Tailwind CSS, Recharts, SWR |
| AI | Ollama + LLaMA 3 (local, free) |
| Scraping | httpx, feedparser, BeautifulSoup4 |
| NLP | YAKE (keyword extraction) |
| Scheduling | APScheduler |

## How It Works

1. **Scraping** - Every 30 minutes, fetches articles from 10 AI/tech RSS feeds (TechCrunch, Ars Technica, The Verge, Wired, MIT Tech Review, VentureBeat, BBC Tech, Reuters Tech, InfoQ)
2. **Trend Analysis** - YAKE extracts multi-word keyphrases, calculates velocity scores, classifies trends as emerging/rising/stable/declining
3. **AI Insights** - Daily at 08:00 UTC (or on-demand), Ollama generates a structured trend briefing with key trends, market signals, and opportunities
4. **Dashboard** - Real-time web UI with auto-refreshing data, interactive charts, and clickable trend details

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trends` | All trends sorted by velocity |
| GET | `/api/trends/emerging` | Emerging & rising trends only |
| GET | `/api/trends/{id}` | Trend detail + related articles |
| GET | `/api/trends/{id}/history` | Velocity history for charting |
| GET | `/api/articles` | Paginated articles (filter by source) |
| GET | `/api/articles/latest` | 20 most recent articles |
| GET | `/api/insights` | All AI insights |
| GET | `/api/insights/latest` | Most recent insight |
| POST | `/api/insights/generate` | Trigger AI insight generation |
| GET | `/api/stats` | Dashboard KPIs + Ollama status |
| POST | `/api/scrape/trigger` | Manual scrape + trend analysis |

Full interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Configuration

All settings in `backend/.env` (no secrets needed):

```env
DATABASE_URL=sqlite+aiosqlite:///./trendagent.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
SCRAPE_INTERVAL_MINUTES=30
TREND_ANALYSIS_INTERVAL_MINUTES=60
CORS_ORIGINS=http://localhost:3000
```

## Graceful Degradation

If Ollama is not running, the app still works fully - scraping, trend analysis, and the dashboard all function normally. AI insight generation is simply skipped, and the dashboard shows an "Ollama offline" indicator.

## License

MIT
=======
# ai-web-monitoring-and-trend-detection-agent
A multi-agent AI platform that performs automated web monitoring, trend detection, and insight generation using Python, FastAPI, and a Next.js dashboard.
>>>>>>> 6f5937448ffc8876fa6cc7dfd7d37ef727f95a1e
