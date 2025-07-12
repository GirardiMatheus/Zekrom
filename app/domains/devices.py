from app.schemas.models import DeviceModel


class Device:
    def __init__(self, data: DeviceModel):
        self.data = data

    def connect(self):
        # Placeholder - lógica será feita na camada de serviço
        return f"Connecting to {self.data.hostname} at {self.data.ip}"