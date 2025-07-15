import threading
import schedule
import time
from app.repositories.db_repository import DBRepository
from app.services.ssh_service import SSHService

class MonitorAgent(threading.Thread):
    def __init__(self, db: DBRepository):
        super().__init__()
        self.db = db
        self.daemon = True

    def run(self):
        schedule.every(1).minutes.do(self.check_devices)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def check_devices(self):
        devices = self.db.list_devices()
        for device in devices:
            try:
                # Criar instância do SSHService para cada device
                ssh_service = SSHService(
                    ip=device.ip,
                    username=device.username,
                    password=device.password
                )
                
                # Usar o comando configurado para cada dispositivo
                command = device.monitor_command or "uptime"
                output = ssh_service.run_command(command)
                print(f"[✓] {device.hostname} executou '{command}': {output}")
                
                # Verificar o output e criar incidente se necessário
                incident = SSHService.verificar_output(output, device.id, command)
                if incident:
                    self.db.add_incident(incident)
                    print(f"[!] Incidente criado para {device.hostname}: {incident.message}")
                    
            except Exception as e:
                print(f"[X] Erro ao conectar {device.hostname}: {e}")
                # Criar incidente para erro de conexão
                incident = SSHService.verificar_output("", device.id, device.monitor_command or "uptime")
                if incident:
                    incident.message = f"Erro de conexão SSH: {str(e)}"
                    self.db.add_incident(incident)
                    print(f"[!] Incidente de conexão criado para {device.hostname}")