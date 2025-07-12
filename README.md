# Incident Manager - SNMP + SSH CLI

Sistema de gerenciamento de incidentes detectados via SNMP e automatizados com SSH, usando Python puro com interface em linha de comando.

## Tecnologias:
- Python 3.11+
- Pexpect (automação via SSH)
- pysnmp (traps SNMP)
- Click + Rich (interface CLI)
- SQLite (persistência leve)

## Estrutura planejada
- `app/`: código da aplicação
- `tests/`: testes automatizados
- `.env`: configurações sensíveis

## Execução:
```bash
python app/cli/main.py

(em construção...)