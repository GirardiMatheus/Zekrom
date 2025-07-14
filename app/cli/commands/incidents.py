import typer
from rich.table import Table
from rich.console import Console
from app.repositories.db_repository import DBRepository

app = typer.Typer()
console = Console()
repo = DBRepository()

@app.command("list")
def list_incidents():
    incidents = repo.list_incidents()

    if not incidents:
        console.print("[red]Nenhum incidente registrado.[/red]")
        return

    table = Table(title="Incidentes")
    table.add_column("ID", justify="center")
    table.add_column("Dispositivo", style="green")
    table.add_column("Mensagem", style="yellow")

    for inc in incidents:
        table.add_row(str(inc.id), str(inc.device_id), inc.message)

    console.print(table)