from app.adapters.ssh_executor import SSHExecutor


class SSHService:
    def __init__(self, ip: str, username: str, password: str):
        self.executor = SSHExecutor(ip, username, password)

    def get_hostname(self) -> str:
        return self.executor.run_command("hostname")

    def check_uptime(self) -> str:
        return self.executor.run_command("uptime")

    def restart_service(self, service_name: str) -> str:
        return self.executor.run_command(f"sudo systemctl restart {service_name}")
