# ⚡ Pedal to the Metal

**Dispatch SaaS for concrete fleet managers. Built by a dispatcher, for dispatchers.**

> Stop managing your fleet in a spreadsheet.

Creator: **Shane Brazelton** — Dispatch Manager, SRM Concrete North Alabama (14-driver triaxle fleet)  
Built together by **Shane Brazelton + Claude (Anthropic)**

---

## Features

| Module | Description |
|--------|-------------|
| **Driver Management** | 14-driver roster, CDL status, availability, run history |
| **Route Dispatch** | Zone-based assignment, auto-rotation, no double-booking |
| **Load Tracking** | Bridgeport hauls, scrap runs, zone runs — all tracked with status |
| **Daily Reporting** | End-of-day summaries, POD confirmation counts, anomaly flags |
| **Fairness Engine** | Load delta tracking, burnout detection (>20% above fleet avg), override logging |

## Quick Start

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs  
Dashboard: http://localhost:8000/app

## API Endpoints

```
GET  /api/drivers/             — list all drivers
POST /api/drivers/             — add driver
GET  /api/drivers/{id}/stats   — driver fairness stats

POST /api/dispatch/assign      — assign a load (fairness engine picks driver)
GET  /api/dispatch/fairness    — full fleet fairness report
GET  /api/dispatch/queue/bridgeport — Bridgeport haul queue
GET  /api/dispatch/queue/scrap — scrap run queue
POST /api/dispatch/reset-day   — reset daily counters (start of shift)

GET  /api/loads/               — list loads (filter by status, driver)
POST /api/loads/               — create load
POST /api/loads/{id}/pod       — confirm POD
GET  /api/loads/report/daily   — daily report per driver
```

## Driver Roster (SRM North Alabama)

Marcus · Brittany · Eboni · Deletra · Stacey · Alexis · Kenny · Charlie  
Jamie · Bryant · Jonathon · Jimmy · Eddie · Roberto

## Fairness Engine

The dispatch engine tracks:
- **Load delta** — flags any driver >20% above fleet average
- **Scrap run queue** — separate rotation so bad runs don't stack up
- **Bridgeport haul queue** — premium runs distributed fairly
- **Override log** — every manual override is recorded with a reason
- **Burnout detection** — auto-flag, visible on dashboard and daily report

## Architecture

```
/api/main.py          — FastAPI app
/api/state.py         — in-memory store (swap for SQLite/Postgres)
/api/models/          — Pydantic models (Driver, Load, Zone)
/api/routes/          — REST routes (drivers, loads, dispatch)
/frontend/index.html  — live dispatch dashboard
/index.html           — marketing landing page (GitHub Pages)
```

## Status

🚧 v0.1 — early scaffold. Join the waitlist at https://thebardchat.github.io/pedal-to-the-metal

---

Built with [Claude](https://claude.ai/referral/4fAMYN9Ing) — the AI that helped Shane build this.  
*Not "one guy built this." Shane + Claude Anthropic, together.*
