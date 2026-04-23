"""
Dispatch engine — zone rotation, fairness scoring, scrap/Bridgeport scheduling,
burnout detection, and POD tracking.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from typing import Optional
from api.models.load import Load, LoadCreate, LoadStatus, LoadType
from api.models.driver import Driver
from api.state import db

router = APIRouter(prefix="/dispatch", tags=["dispatch"])

ROSTER = [
    "Marcus", "Brittany", "Eboni", "Deletra", "Stacey", "Alexis",
    "Kenny", "Charlie", "Jamie", "Bryant", "Jonathon", "Jimmy", "Eddie", "Roberto",
]

# A driver is flagged when their load count is more than 20% above fleet average
BURNOUT_DELTA_THRESHOLD = 0.20


def _fleet_avg_loads() -> float:
    drivers = list(db.drivers.values())
    if not drivers:
        return 0.0
    return sum(d.loads_today for d in drivers) / len(drivers)


def _check_burnout(driver: Driver, fleet_avg: float) -> bool:
    if fleet_avg == 0:
        return False
    delta = (driver.loads_today - fleet_avg) / fleet_avg
    return delta > BURNOUT_DELTA_THRESHOLD


def _pick_driver(zone: Optional[str], load_type: LoadType) -> Optional[Driver]:
    """
    Select the best available driver using fairness scoring:
    - Eligible = available + not burnout-flagged (unless everyone is flagged)
    - For scrap/Bridgeport, prefer drivers with fewest special runs today
    - Tiebreak by fewest loads_today, then last_run_time (longest wait first)
    """
    all_drivers = [d for d in db.drivers.values() if d.available]
    if not all_drivers:
        return None

    fleet_avg = _fleet_avg_loads()
    eligible = [d for d in all_drivers if not _check_burnout(d, fleet_avg)]
    if not eligible:
        eligible = all_drivers  # everyone overloaded — pick least loaded

    def score(driver: Driver) -> tuple:
        if load_type == LoadType.SCRAP:
            return (driver.scrap_runs_today, driver.loads_today, driver.last_run_time or datetime.min.replace(tzinfo=timezone.utc))
        if load_type == LoadType.BRIDGEPORT:
            return (driver.bridgeport_runs_today, driver.loads_today, driver.last_run_time or datetime.min.replace(tzinfo=timezone.utc))
        return (driver.loads_today, driver.last_run_time or datetime.min.replace(tzinfo=timezone.utc))

    return min(eligible, key=score)


@router.post("/assign")
def assign_load(payload: LoadCreate, override_driver_id: Optional[int] = None):
    """
    Assign a load. Optionally override with a specific driver_id (override_reason required).
    """
    load_id = db.next_load_id()
    load = Load(id=load_id, **payload.model_dump(), status=LoadStatus.ASSIGNED, assigned_at=datetime.now(timezone.utc))

    if override_driver_id is not None:
        driver = db.drivers.get(override_driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Override driver not found")
        load.override_reason = load.override_reason or "Manual override by dispatcher"
    else:
        driver = _pick_driver(payload.zone, payload.load_type)
        if not driver:
            raise HTTPException(status_code=503, detail="No available drivers")

    load.driver_id = driver.id
    load.driver_name = driver.name
    db.loads[load_id] = load

    # Update driver state
    driver.loads_today += 1
    driver.loads_week += 1
    driver.loads_total += 1
    driver.last_run_zone = payload.zone
    driver.last_run_time = datetime.now(timezone.utc)

    if payload.load_type == LoadType.SCRAP:
        driver.scrap_runs_today += 1
    if payload.load_type == LoadType.BRIDGEPORT:
        driver.bridgeport_runs_today += 1

    fleet_avg = _fleet_avg_loads()
    driver.burnout_flag = _check_burnout(driver, fleet_avg)

    return {
        "load": load,
        "assigned_to": driver.name,
        "burnout_flag": driver.burnout_flag,
        "fleet_avg_loads_today": round(fleet_avg, 2),
    }


@router.get("/fairness")
def fairness_report():
    """
    Full fleet fairness snapshot — load distribution, delta from average, burnout flags.
    """
    drivers = list(db.drivers.values())
    fleet_avg = _fleet_avg_loads()
    rows = []
    for d in drivers:
        delta = (d.loads_today - fleet_avg) if fleet_avg > 0 else 0
        delta_pct = (delta / fleet_avg * 100) if fleet_avg > 0 else 0
        burnout = _check_burnout(d, fleet_avg)
        if burnout != d.burnout_flag:
            d.burnout_flag = burnout
        rows.append({
            "id": d.id,
            "name": d.name,
            "available": d.available,
            "loads_today": d.loads_today,
            "scrap_runs_today": d.scrap_runs_today,
            "bridgeport_runs_today": d.bridgeport_runs_today,
            "delta_from_avg": round(delta, 2),
            "delta_pct": round(delta_pct, 1),
            "burnout_flag": d.burnout_flag,
            "last_zone": d.last_run_zone,
        })
    rows.sort(key=lambda r: -r["loads_today"])
    return {
        "fleet_avg_loads_today": round(fleet_avg, 2),
        "total_drivers": len(drivers),
        "available_drivers": len([d for d in drivers if d.available]),
        "burnout_flags": len([r for r in rows if r["burnout_flag"]]),
        "drivers": rows,
    }


@router.get("/queue/bridgeport")
def bridgeport_queue():
    """Return drivers ordered by fewest Bridgeport hauls today — next in queue first."""
    available = [d for d in db.drivers.values() if d.available]
    if not available:
        return {"queue": [], "message": "No available drivers"}
    queue = sorted(available, key=lambda d: (d.bridgeport_runs_today, d.loads_today))
    return {
        "queue": [{"id": d.id, "name": d.name, "bridgeport_runs_today": d.bridgeport_runs_today, "loads_today": d.loads_today} for d in queue]
    }


@router.get("/queue/scrap")
def scrap_queue():
    """Return drivers ordered by fewest scrap runs today — next in queue first."""
    available = [d for d in db.drivers.values() if d.available]
    if not available:
        return {"queue": [], "message": "No available drivers"}
    queue = sorted(available, key=lambda d: (d.scrap_runs_today, d.loads_today))
    return {
        "queue": [{"id": d.id, "name": d.name, "scrap_runs_today": d.scrap_runs_today, "loads_today": d.loads_today} for d in queue]
    }


@router.post("/reset-day")
def reset_daily_counters():
    """Reset all daily counters (run at start of shift)."""
    for driver in db.drivers.values():
        driver.loads_today = 0
        driver.scrap_runs_today = 0
        driver.bridgeport_runs_today = 0
        driver.burnout_flag = False
        driver.last_run_zone = None
        driver.last_run_time = None
    db.loads.clear()
    return {"status": "Daily counters reset", "drivers_reset": len(db.drivers)}
