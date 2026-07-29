# Pedal to the Metal

**Dispatch SaaS prototype for concrete fleet managers. Built by a dispatcher, for dispatchers.**

> Stop managing your fleet in a spreadsheet.

Creator: **Shane Brazelton**  
Built together by **Shane Brazelton + Claude (Anthropic)**

---

## Privacy Notice

This public prototype uses synthetic sample data only. Do not commit real SRM employee names, driver rosters, phone numbers, customer details, plant contact lists, jobsite data, dispatch screenshots, schedules, PODs, or private daily/home tasks.

---

## Features

| Module | Description |
|--------|-------------|
| **Driver Management** | Synthetic 14-driver sample roster, CDL status, availability, run history |
| **Route Dispatch** | Zone-based assignment, auto-rotation, no double-booking |
| **Load Tracking** | Demo haul queues and zone runs tracked with status |
| **Daily Reporting** | End-of-day summaries, POD confirmation counts, anomaly flags |
| **Fairness Engine** | Load delta tracking, burnout detection, override logging |

## Quick Start

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs  
Dashboard: http://localhost:8000/app

## API Endpoints

```text
GET  /api/drivers/             — list all drivers
POST /api/drivers/             — add driver
GET  /api/drivers/{id}/stats   — driver fairness stats

POST /api/dispatch/assign      — assign a load
GET  /api/dispatch/fairness    — full fleet fairness report
GET  /api/dispatch/queue/bridgeport — demo premium haul queue
GET  /api/dispatch/queue/scrap — demo scrap run queue
POST /api/dispatch/reset-day   — reset daily counters

GET  /api/loads/               — list loads
POST /api/loads/               — create load
POST /api/loads/{id}/pod       — confirm POD
GET  /api/loads/report/daily   — daily report per driver
```

## Sample Driver Roster

Driver 01 · Driver 02 · Driver 03 · Driver 04 · Driver 05 · Driver 06 · Driver 07  
Driver 08 · Driver 09 · Driver 10 · Driver 11 · Driver 12 · Driver 13 · Driver 14

## Architecture

```text
/api/main.py          — FastAPI app
/api/state.py         — in-memory store (swap for SQLite/Postgres)
/api/models/          — Pydantic models
/api/routes/          — REST routes
/frontend/index.html  — API-backed dispatch dashboard
/index.html           — GitHub Pages shell
```

## Status

v0.1 — early public scaffold using demo data only.
