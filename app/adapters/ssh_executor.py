import pexpect
import sys


class SSHExecutor:
    def __init__(self, ip: str, username: str, password: str, timeout: int = 10):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout

    def run_command(self, command: str) -> str:
        try:
            ssh = pexpect.spawn(f"ssh {self.username}@{self.ip}", timeout=self.timeout)
            ssh.expect("password:")
            ssh.sendline(self.password)

            ssh.expect(r"[#$]")  # prompt básico
            ssh.sendline(command)

            ssh.expect(r"[#$]")  # aguarda comando terminar
            output = ssh.before.decode("utf-8")

            ssh.sendline("exit")
            ssh.close()

            return output.strip()

        except pexpect.TIMEOUT:
            return "[ERROR] Conexão expirou."
        except pexpect.exceptions.EOF:
            return "[ERROR] Conexão encerrada inesperadamente."
        except Exception as e:
            return f"[ERROR] {str(e)}"
