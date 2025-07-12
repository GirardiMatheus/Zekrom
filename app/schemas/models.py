from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeviceModel(BaseModel):
    id: Optional[int]
    hostname: str
    ip: str
    username: str
    password: str


class IncidentModel(BaseModel):
    id: Optional[int]
    device_id: int
    message: str
    severity: str  # Ex: "critical", "warning", "info"
    timestamp: datetime
    status: str  # Ex: "open", "resolved"