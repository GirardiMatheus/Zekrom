import typer
from rich.table import Table
from rich.console import Console
from app.repositories.db_repository import DBRepository

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

    for dev in devices:
        table.add_row(str(dev.id), dev.hostname, dev.ip)

    console.print(table)