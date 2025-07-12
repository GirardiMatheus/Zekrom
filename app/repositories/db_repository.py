import sqlite3
from typing import List, Optional
from app.schemas.models import DeviceModel, IncidentModel
from app.core import config


class DBRepository:
    def __init__(self, db_path: str = config.DB_PATH):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # Devices
    def add_device(self, device: DeviceModel) -> int:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO devices (hostname, ip, username, password) VALUES (?, ?, ?, ?)",
            (device.hostname, device.ip, device.username, device.password)
        )
        conn.commit()
        device_id = cursor.lastrowid
        conn.close()
        return device_id

    def get_device_by_id(self, device_id: int) -> Optional[DeviceModel]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return DeviceModel(id=row[0], hostname=row[1], ip=row[2], username=row[3], password=row[4])
        return None

    def list_devices(self) -> List[DeviceModel]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices")
        rows = cursor.fetchall()
        conn.close()
        return [DeviceModel(id=r[0], hostname=r[1], ip=r[2], username=r[3], password=r[4]) for r in rows]

    # Incidents
    def add_incident(self, incident: IncidentModel) -> int:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO incidents (device_id, message, severity, timestamp, status) VALUES (?, ?, ?, ?, ?)",
            (incident.device_id, incident.message, incident.severity, incident.timestamp.isoformat(), incident.status)
        )
        conn.commit()
        incident_id = cursor.lastrowid
        conn.close()
        return incident_id

    def list_incidents(self) -> List[IncidentModel]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidents")
        rows = cursor.fetchall()
        conn.close()
        return [
            IncidentModel(
                id=r[0],
                device_id=r[1],
                message=r[2],
                severity=r[3],
                timestamp=r[4],
                status=r[5]
            ) for r in rows
        ]

    def update_incident_status(self, incident_id: int, new_status: str):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE incidents SET status = ? WHERE id = ?",
            (new_status, incident_id)
        )
        conn.commit()
        conn.close()
