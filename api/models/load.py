from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class LoadType(str, Enum):
    ZONE = "zone"
    SCRAP = "scrap"
    BRIDGEPORT = "bridgeport"


class LoadStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    POD_CONFIRMED = "pod_confirmed"


class Load(BaseModel):
    id: Optional[int] = None
    load_type: LoadType = LoadType.ZONE
    status: LoadStatus = LoadStatus.PENDING
    zone: Optional[str] = None
    driver_id: Optional[int] = None
    driver_name: Optional[str] = None
    destination: Optional[str] = None
    pickup_location: Optional[str] = None
    assigned_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    pod_at: Optional[datetime] = None
    pod_confirmed: bool = False
    notes: Optional[str] = None
    override_reason: Optional[str] = None


class LoadCreate(BaseModel):
    load_type: LoadType = LoadType.ZONE
    zone: Optional[str] = None
    destination: Optional[str] = None
    pickup_location: Optional[str] = None
    notes: Optional[str] = None


class LoadUpdate(BaseModel):
    status: Optional[LoadStatus] = None
    driver_id: Optional[int] = None
    destination: Optional[str] = None
    pod_confirmed: Optional[bool] = None
    notes: Optional[str] = None
    override_reason: Optional[str] = None
