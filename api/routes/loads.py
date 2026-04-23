from fastapi import APIRouter, HTTPException
from typing import List, Optional
from api.models.load import Load, LoadCreate, LoadUpdate, LoadStatus
from api.state import db

router = APIRouter(prefix="/loads", tags=["loads"])


@router.get("/", response_model=List[Load])
def list_loads(status: Optional[str] = None, driver_id: Optional[int] = None):
    loads = list(db.loads.values())
    if status:
        loads = [l for l in loads if l.status == status]
    if driver_id:
        loads = [l for l in loads if l.driver_id == driver_id]
    return loads


@router.get("/{load_id}", response_model=Load)
def get_load(load_id: int):
    if load_id not in db.loads:
        raise HTTPException(status_code=404, detail="Load not found")
    return db.loads[load_id]


@router.post("/", response_model=Load)
def create_load(payload: LoadCreate):
    load_id = db.next_load_id()
    load = Load(id=load_id, **payload.model_dump())
    db.loads[load_id] = load
    return load


@router.patch("/{load_id}", response_model=Load)
def update_load(load_id: int, payload: LoadUpdate):
    if load_id not in db.loads:
        raise HTTPException(status_code=404, detail="Load not found")
    load = db.loads[load_id]
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(load, field, val)
    return load


@router.post("/{load_id}/pod")
def confirm_pod(load_id: int):
    from datetime import datetime, timezone
    if load_id not in db.loads:
        raise HTTPException(status_code=404, detail="Load not found")
    load = db.loads[load_id]
    load.pod_confirmed = True
    load.pod_at = datetime.now(timezone.utc)
    load.status = LoadStatus.POD_CONFIRMED
    return {"status": "POD confirmed", "load_id": load_id}


@router.get("/report/daily")
def daily_report():
    loads = list(db.loads.values())
    report = {}
    for driver in db.drivers.values():
        driver_loads = [l for l in loads if l.driver_id == driver.id]
        report[driver.name] = {
            "total": len(driver_loads),
            "delivered": len([l for l in driver_loads if l.status in [LoadStatus.DELIVERED, LoadStatus.POD_CONFIRMED]]),
            "pod_confirmed": len([l for l in driver_loads if l.pod_confirmed]),
            "scrap_runs": driver.scrap_runs_today,
            "bridgeport_runs": driver.bridgeport_runs_today,
            "burnout_flag": driver.burnout_flag,
        }
    return {"date": "today", "drivers": report, "total_loads": len(loads)}
