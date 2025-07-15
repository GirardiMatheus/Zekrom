import typer
from rich.console import Console

from app.cli.commands import devices, incidents, ssh, monitor, export
app = typer.Typer()
console = Console()

app.add_typer(devices.app, name="devices")
app.add_typer(incidents.app, name="incidents")
app.add_typer(ssh.app, name="ssh")
app.add_typer(monitor.app, name="monitor")
app.add_typer(export.app, name="export")


@app.command()
def menu():
    console.print("[bold cyan]Zekrom CLI - Painel de Operações[/bold cyan]")
    console.print("- devices: Gerenciar dispositivos")
    console.print("- incidents: Visualizar incidentes")
    console.print("- ssh: Executar comandos remotos")
    console.print("- monitor: Iniciar agente de monitoramento")
    console.print("- export: Exportar dados")


if __name__ == "__main__":
    app()