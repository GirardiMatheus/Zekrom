import typer
from rich.table import Table
from rich.console import Console
from app.repositories.db_repository import DBRepository
from typing import Optional

app = typer.Typer()
console = Console()
repo = DBRepository()

@app.command("list")
def list_incidents(
    from_date: Optional[str] = typer.Option(None, "--from-date", help="Data inicial (YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS)"),
    to_date: Optional[str] = typer.Option(None, "--to-date", help="Data final (YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS)"),
    severity: Optional[str] = typer.Option(None, "--severity", help="Filtrar por gravidade (critical, warning, info)"),
    status: Optional[str] = typer.Option(None, "--status", help="Filtrar por status (open, resolved)")
):
    """Listar incidentes com filtros opcionais"""
    
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

    incidents = repo.list_incidents(
        from_date=from_date,
        to_date=to_date,
        severity=severity,
        status=status
    )

    if not incidents:
        filter_info = []
        if from_date:
            filter_info.append(f"data inicial: {from_date}")
        if to_date:
            filter_info.append(f"data final: {to_date}")
        if severity:
            filter_info.append(f"gravidade: {severity}")
        if status:
            filter_info.append(f"status: {status}")
            
        filter_text = f" com os filtros aplicados ({', '.join(filter_info)})" if filter_info else ""
        console.print(f"[red]Nenhum incidente encontrado{filter_text}.[/red]")
        return

    # Build title with filter info
    title_parts = ["Incidentes"]
    if any([from_date, to_date, severity, status]):
        filter_parts = []
        if from_date:
            filter_parts.append(f"de {from_date}")
        if to_date:
            filter_parts.append(f"até {to_date}")
        if severity:
            filter_parts.append(f"gravidade: {severity}")
        if status:
            filter_parts.append(f"status: {status}")
        title_parts.append(f"({', '.join(filter_parts)})")
    
    table = Table(title=" ".join(title_parts))
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Dispositivo", style="green")
    table.add_column("Mensagem", style="yellow")
    table.add_column("Gravidade", style="red")
    table.add_column("Status", style="blue")
    table.add_column("Timestamp", style="magenta")

    for inc in incidents:
        # Color code severity
        severity_color = "red" if inc.severity.lower() == "critical" else "yellow" if inc.severity.lower() == "warning" else "green"
        status_color = "red" if inc.status.lower() == "open" else "green"
        
        table.add_row(
            str(inc.id), 
            str(inc.device_id), 
            inc.message,
            f"[{severity_color}]{inc.severity}[/{severity_color}]",
            f"[{status_color}]{inc.status}[/{status_color}]",
            str(inc.timestamp)
        )

    console.print(table)
    console.print(f"\n[green]Total: {len(incidents)} incidentes encontrados[/green]")