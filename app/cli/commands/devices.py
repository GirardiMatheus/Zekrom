import typer
from rich.table import Table
from rich.console import Console
from app.repositories.db_repository import DBRepository
from app.schemas.models import DeviceModel

app = typer.Typer()
console = Console()
repo = DBRepository()

@app.command("list")
def list_devices():
    devices = repo.list_devices()

    if not devices:
        console.print("[red]Nenhum dispositivo encontrado.[/red]")
        return

    table = Table(title="Dispositivos Registrados")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Nome", style="green")
    table.add_column("IP", style="yellow")
    table.add_column("Comando Monitor", style="magenta")

    for dev in devices:
        table.add_row(
            str(dev.id), 
            dev.hostname, 
            dev.ip, 
            dev.monitor_command or "uptime"
        )

    console.print(table)

@app.command("add")
def add_device(
    hostname: str = typer.Option(..., "--hostname", help="Nome do dispositivo"),
    ip: str = typer.Option(..., "--ip", help="IP do dispositivo"),
    username: str = typer.Option(..., "--username", help="Usuário SSH"),
    password: str = typer.Option(..., "--password", help="Senha SSH"),
    monitor_command: str = typer.Option("uptime", "--monitor-cmd", help="Comando para monitoramento")
):
    device = DeviceModel(
        hostname=hostname,
        ip=ip,
        username=username,
        password=password,
        monitor_command=monitor_command
    )
    
    device_id = repo.add_device(device)
    console.print(f"[green]Dispositivo {hostname} adicionado com ID {device_id}[/green]")
    console.print(f"[yellow]Comando de monitoramento: {monitor_command}[/yellow]")

@app.command("update-monitor-cmd")
def update_monitor_command(
    device_id: int = typer.Option(..., "--id", help="ID do dispositivo"),
    monitor_command: str = typer.Option(..., "--cmd", help="Novo comando de monitoramento")
):
    device = repo.get_device_by_id(device_id)
    if not device:
        console.print(f"[red]Dispositivo com ID {device_id} não encontrado.[/red]")
        return
    
    repo.update_device_monitor_command(device_id, monitor_command)
    console.print(f"[green]Comando de monitoramento do dispositivo {device.hostname} atualizado para: {monitor_command}[/green]")