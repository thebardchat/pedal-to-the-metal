from pydantic import BaseModel
from typing import Optional, List


class Zone(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    is_bridgeport: bool = False
    is_scrap: bool = False
    avg_haul_minutes: Optional[int] = None
    active: bool = True


class ZoneCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_bridgeport: bool = False
    is_scrap: bool = False
    avg_haul_minutes: Optional[int] = None


PREDEFINED_ZONES = [
    Zone(id=1, name="North", description="North Alabama zone"),
    Zone(id=2, name="South", description="South zone"),
    Zone(id=3, name="East", description="East zone"),
    Zone(id=4, name="West", description="West zone"),
    Zone(id=5, name="Bridgeport", description="Bridgeport haul route", is_bridgeport=True, avg_haul_minutes=90),
    Zone(id=6, name="Scrap", description="Scrap run", is_scrap=True, avg_haul_minutes=45),
]
