import typer
from app.services.ssh_service import SSHService

app = typer.Typer()

@app.command("exec")
def exec_ssh(
    ip: str = typer.Option(..., "--ip", help="IP do dispositivo"),
    user: str = typer.Option(..., "--user", help="Usuário SSH"),
    password: str = typer.Option(..., "--password", help="Senha SSH"),
    cmd: str = typer.Option(..., "--cmd", help="Comando a ser executado")
):
    ssh_service = SSHService(ip=ip, username=user, password=password)
    output = ssh_service.run_command(cmd)
    typer.echo(output)