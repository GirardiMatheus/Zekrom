import typer
from app.scheduler.monitor_agent import MonitorAgent
from app.repositories.db_repository import DBRepository

app = typer.Typer()

@app.command("start")
def start_monitor():
    db = DBRepository()
    agent = MonitorAgent(db)
    agent.start()
    typer.echo("Agente de monitoramento iniciado. Pressione Ctrl+C para sair.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        typer.echo("Monitor encerrado.")