from app.adapters.ssh_executor import SSHExecutor
from app.schemas.models import IncidentModel
from datetime import datetime


class SSHService:
    def __init__(self, ip: str, username: str, password: str):
        self.executor = SSHExecutor(ip, username, password)

    def run_command(self, command: str) -> str:
        return self.executor.run_command(command)

    def get_hostname(self) -> str:
        return self.executor.run_command("hostname")

    def check_uptime(self) -> str:
        return self.executor.run_command("uptime")

    def restart_service(self, service_name: str) -> str:
        return self.executor.run_command(f"sudo systemctl restart {service_name}")
    
    @staticmethod
    def verificar_output(output: str, device_id: int, command: str = "uptime") -> IncidentModel | None:
        # Lógica específica para diferentes comandos
        if command == "uptime":
            if "load average" not in output or output.strip() == "":
                return IncidentModel(
                    device_id=device_id,
                    message="Dispositivo inacessível ou comando uptime falhou",
                    severity="critical",
                    status="open",
                    timestamp=datetime.now()
                )
        elif command.startswith("ping"):
            if "0 received" in output or "100% packet loss" in output or output.strip() == "":
                return IncidentModel(
                    device_id=device_id,
                    message="Dispositivo não responde ao ping",
                    severity="critical", 
                    status="open",
                    timestamp=datetime.now()
                )
        elif "systemctl status" in command:
            if "inactive" in output or "failed" in output or output.strip() == "":
                service_name = command.split()[-1] if len(command.split()) > 2 else "serviço"
                return IncidentModel(
                    device_id=device_id,
                    message=f"Serviço {service_name} está inativo ou falhou",
                    severity="warning",
                    status="open", 
                    timestamp=datetime.now()
                )
        else:
            # Para comandos personalizados, verificar se há output
            if output.strip() == "" or "[ERROR]" in output:
                return IncidentModel(
                    device_id=device_id,
                    message=f"Comando '{command}' falhou ou retornou erro",
                    severity="warning",
                    status="open",
                    timestamp=datetime.now()
                )
        
        return None