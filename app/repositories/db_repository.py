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
            "INSERT INTO devices (hostname, ip, username, password, monitor_command) VALUES (?, ?, ?, ?, ?)",
            (device.hostname, device.ip, device.username, device.password, device.monitor_command)
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
            # Compatibilidade com banco antigo (sem monitor_command)
            monitor_command = row[5] if len(row) > 5 else "uptime"
            return DeviceModel(
                id=row[0], 
                hostname=row[1], 
                ip=row[2], 
                username=row[3], 
                password=row[4],
                monitor_command=monitor_command
            )
        return None

    def list_devices(self) -> List[DeviceModel]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices")
        rows = cursor.fetchall()
        conn.close()
        devices = []
        for r in rows:
            # Compatibilidade com banco antigo (sem monitor_command)
            monitor_command = r[5] if len(r) > 5 else "uptime"
            devices.append(DeviceModel(
                id=r[0], 
                hostname=r[1], 
                ip=r[2], 
                username=r[3], 
                password=r[4],
                monitor_command=monitor_command
            ))
        return devices

    def update_device_monitor_command(self, device_id: int, monitor_command: str):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE devices SET monitor_command = ? WHERE id = ?",
            (monitor_command, device_id)
        )
        conn.commit()
        conn.close()

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

    def list_incidents(
        self, 
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[IncidentModel]:
        conn = self._connect()
        cursor = conn.cursor()
        
        # Build dynamic query with filters
        query = "SELECT * FROM incidents WHERE 1=1"
        params = []
        
        if from_date:
            query += " AND timestamp >= ?"
            params.append(from_date)
            
        if to_date:
            query += " AND timestamp <= ?"
            params.append(to_date)
            
        if severity:
            query += " AND LOWER(severity) = LOWER(?)"
            params.append(severity)
            
        if status:
            query += " AND LOWER(status) = LOWER(?)"
            params.append(status)
            
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
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