from fastapi import APIRouter, HTTPException
from typing import List
from api.models.driver import Driver, DriverCreate, DriverUpdate
from api.state import db

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("/", response_model=List[Driver])
def list_drivers():
    return list(db.drivers.values())


@router.get("/{driver_id}", response_model=Driver)
def get_driver(driver_id: int):
    if driver_id not in db.drivers:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db.drivers[driver_id]


@router.post("/", response_model=Driver)
def create_driver(payload: DriverCreate):
    driver_id = db.next_driver_id()
    driver = Driver(id=driver_id, **payload.model_dump())
    db.drivers[driver_id] = driver
    return driver


@router.patch("/{driver_id}", response_model=Driver)
def update_driver(driver_id: int, payload: DriverUpdate):
    if driver_id not in db.drivers:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver = db.drivers[driver_id]
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(driver, field, val)
    return driver


@router.delete("/{driver_id}")
def delete_driver(driver_id: int):
    if driver_id not in db.drivers:
        raise HTTPException(status_code=404, detail="Driver not found")
    del db.drivers[driver_id]
    return {"status": "deleted"}


@router.get("/{driver_id}/stats")
def driver_stats(driver_id: int):
    if driver_id not in db.drivers:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver = db.drivers[driver_id]
    fleet_avg = sum(d.loads_today for d in db.drivers.values()) / max(len(db.drivers), 1)
    delta_pct = ((driver.loads_today - fleet_avg) / max(fleet_avg, 1)) * 100
    return {
        "driver": driver,
        "fleet_avg_loads_today": round(fleet_avg, 2),
        "delta_pct": round(delta_pct, 1),
        "burnout_flag": driver.burnout_flag,
    }
