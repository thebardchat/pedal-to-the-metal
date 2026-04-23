from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Driver(BaseModel):
    id: Optional[int] = None
    name: str
    cdl_class: str = "A"
    available: bool = True
    zone_preference: Optional[str] = None
    loads_today: int = 0
    loads_week: int = 0
    loads_total: int = 0
    scrap_runs_today: int = 0
    bridgeport_runs_today: int = 0
    last_run_zone: Optional[str] = None
    last_run_time: Optional[datetime] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    burnout_flag: bool = False


class DriverCreate(BaseModel):
    name: str
    cdl_class: str = "A"
    phone: Optional[str] = None
    zone_preference: Optional[str] = None
    notes: Optional[str] = None


class DriverUpdate(BaseModel):
    available: Optional[bool] = None
    cdl_class: Optional[str] = None
    phone: Optional[str] = None
    zone_preference: Optional[str] = None
    notes: Optional[str] = None
