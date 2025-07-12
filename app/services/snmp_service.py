from app.schemas.models import IncidentModel
from datetime import datetime
import random


def parse_snmp_trap(var_binds) -> dict:
    """
    Converte varBinds do SNMP para um dicionário simples.
    """
    parsed = {}
    for name, val in var_binds:
        parsed[str(name)] = str(val)
    return parsed


def build_incident_from_trap(trap_data: dict, device_id: int) -> IncidentModel:
    """
    Gera um incidente a partir do dicionário do SNMP.
    """
    return IncidentModel(
        device_id=device_id,
        message=trap_data.get("1.3.6.1.2.1.1.3.0", "Trap recebida"),
        severity="critical",  # ou usar OID para definir criticidade
        timestamp=datetime.now(),
        status="open"
    )
