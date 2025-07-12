from app.schemas.models import IncidentModel
from datetime import datetime


class Incident:
    def __init__(self, data: IncidentModel):
        self.data = data

    def open(self):
        self.data.status = "open"
        self.data.timestamp = datetime.now()

    def resolve(self):
        self.data.status = "resolved"

    def is_critical(self):
        return self.data.severity.lower() == "critical"