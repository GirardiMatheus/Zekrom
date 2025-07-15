import typer
from typing import Optional
from app.repositories.db_repository import DBRepository
from app.services.export_service import ExportService
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command("incidents")
def export_incidents(
    path: str = typer.Option("incidentes.csv", "--output", "-o", help="Caminho do arquivo de saída"),
    from_date: Optional[str] = typer.Option(None, "--from-date", help="Data inicial (YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS)"),
    to_date: Optional[str] = typer.Option(None, "--to-date", help="Data final (YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS)"),
    severity: Optional[str] = typer.Option(None, "--severity", help="Filtrar por gravidade (critical, warning, info)"),
    status: Optional[str] = typer.Option(None, "--status", help="Filtrar por status (open, resolved)")
):
    """Exportar incidentes para CSV com filtros opcionais"""
    
    # Validate severity options
    if severity and severity.lower() not in ['critical', 'warning', 'info']:
        console.print("[red]Erro: Gravidade deve ser 'critical', 'warning' ou 'info'[/red]")
        raise typer.Exit(1)
    
    # Validate status options  
    if status and status.lower() not in ['open', 'resolved']:
        console.print("[red]Erro: Status deve ser 'open' ou 'resolved'[/red]")
        raise typer.Exit(1)
    
    # Validate date format (basic check)
    for date_param, date_name in [(from_date, "from-date"), (to_date, "to-date")]:
        if date_param:
            try:
                # Try to parse the date to validate format
                if len(date_param) == 10:  # YYYY-MM-DD
                    from datetime import datetime
                    datetime.strptime(date_param, "%Y-%m-%d")
                elif len(date_param) == 19:  # YYYY-MM-DD HH:MM:SS
                    from datetime import datetime
                    datetime.strptime(date_param, "%Y-%m-%d %H:%M:%S")
                else:
                    raise ValueError("Formato inválido")
            except ValueError:
                console.print(f"[red]Erro: {date_name} deve estar no formato YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS[/red]")
                raise typer.Exit(1)
    
    service = ExportService(DBRepository())
    service.export_incidents(
        path, 
        from_date=from_date,
        to_date=to_date,
        severity=severity,
        status=status
    )

@app.command("devices")
def export_devices(
    path: str = typer.Option("dispositivos.csv", "--output", "-o", help="Caminho do arquivo de saída")
):
    """Exportar dispositivos para CSV"""
    service = ExportService(DBRepository())
    service.export_devices(path)

@app.command("help")
def show_help():
    """Mostrar exemplos de uso dos comandos de exportação"""
    console.print("[bold cyan]Exemplos de uso dos comandos de exportação:[/bold cyan]\n")
    
    console.print("[yellow]Exportar todos os incidentes:[/yellow]")
    console.print("  python -m app.cli.main export incidents\n")
    
    console.print("[yellow]Exportar incidentes críticos:[/yellow]")
    console.print("  python -m app.cli.main export incidents --severity critical\n")
    
    console.print("[yellow]Exportar incidentes abertos:[/yellow]")
    console.print("  python -m app.cli.main export incidents --status open\n")
    
    console.print("[yellow]Exportar incidentes de uma data específica:[/yellow]")
    console.print("  python -m app.cli.main export incidents --from-date 2025-01-01 --to-date 2025-01-31\n")
    
    console.print("[yellow]Combinar filtros:[/yellow]")
    console.print("  python -m app.cli.main export incidents --severity critical --status open --from-date 2025-01-01\n")
    
    console.print("[yellow]Especificar arquivo de saída:[/yellow]")
    console.print("  python -m app.cli.main export incidents --output /path/to/incidents.csv\n")
    
    console.print("[bold green]Valores válidos:[/bold green]")
    console.print("  • Severity: critical, warning, info")
    console.print("  • Status: open, resolved")
    console.print("  • Dates: YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS")