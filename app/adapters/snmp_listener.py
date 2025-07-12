from pysnmp.entity import engine, config as snmp_config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
from app.services.snmp_service import parse_snmp_trap, build_incident_from_trap
from app.repositories.db_repository import DBRepository
from app.core import config
import threading


class SNMPTrapListener(threading.Thread):
    def __init__(self, db: DBRepository):
        super().__init__()
        self.db = db
        self.daemon = True

    def run(self):
        print(f"SNMP Trap listener rodando na porta {config.SNMP_LISTEN_PORT}...")
        
        # Criar o SNMP engine
        snmp_engine = engine.SnmpEngine()

        # Configurar comunidade SNMP
        snmp_config.addV1System(snmp_engine, 'my-area', 'public')

        def callback(snmp_engine, state_ref, context_engine_id,
                     context_name, var_binds, cb_ctx):
            try:
                print(f'Notification received from {state_ref}')
                parsed = parse_snmp_trap(var_binds)
                print("Trap recebida:", parsed)

                devices = self.db.list_devices()
                if not devices:
                    print("[!] Nenhum dispositivo registrado.")
                    return

                incident = build_incident_from_trap(parsed, device_id=devices[0].id)
                self.db.add_incident(incident)
                print("[+] Incidente registrado no banco.")
            except Exception as e:
                print(f"[!] Erro ao processar trap: {e}")
                import traceback
                traceback.print_exc()

        # Registrar o transporte UDP
        snmp_config.addTransport(
            snmp_engine,
            udp.domainName,
            udp.UdpTransport().openServerMode(('0.0.0.0', config.SNMP_LISTEN_PORT))
        )

        # Registra o callback para traps SNMP
        ntfrcv.NotificationReceiver(snmp_engine, callback)

        print('SNMP trap receiver is ready...')
        snmp_engine.transportDispatcher.jobStarted(1)
        try:
            snmp_engine.transportDispatcher.runDispatcher()
        except KeyboardInterrupt:
            snmp_engine.transportDispatcher.closeDispatcher()
            print("Encerrando SNMP listener.")
