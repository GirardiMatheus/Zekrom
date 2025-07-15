from app.adapters.snmp_listener import SNMPTrapListener
from app.repositories.db_repository import DBRepository

if __name__ == "__main__":
    db = DBRepository()
    listener = SNMPTrapListener(db)
    listener.start()

    input("SNMP Listener rodando. Pressione Enter para encerrar...\n")