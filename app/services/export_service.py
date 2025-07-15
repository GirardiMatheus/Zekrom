import csv
from app.repositories.db_repository import DBRepository
from datetime import datetime
from pathlib import Path
from typing import Optional

class ExportService:
    def __init__(self, db: DBRepository):
        self.db = db

    def export_incidents(
        self, 
        file_path: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None
    ):
        incidents = self.db.list_incidents(
            from_date=from_date,
            to_date=to_date,
            severity=severity,
            status=status
        )
        
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Device ID", "Mensagem", "Gravidade", "Status", "Timestamp"])
            for i in incidents:
                writer.writerow([
                    i.id, i.device_id, i.message, i.severity, i.status, i.timestamp
                ])
        
        # Show filter summary
        filter_info = []
        if from_date:
            filter_info.append(f"data inicial: {from_date}")
        if to_date:
            filter_info.append(f"data final: {to_date}")
        if severity:
            filter_info.append(f"gravidade: {severity}")
        if status:
            filter_info.append(f"status: {status}")
            
        filter_text = f" (filtros: {', '.join(filter_info)})" if filter_info else ""
        print(f"[✓] {len(incidents)} incidentes exportados para {file_path}{filter_text}")

    def export_devices(self, file_path: str):
        devices = self.db.list_devices()
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Hostname", "IP", "Username"])
            for d in devices:
                writer.writerow([
                    d.id, d.hostname, d.ip, d.username
                ])
        print(f"[✓] Dispositivos exportados para {file_path}")