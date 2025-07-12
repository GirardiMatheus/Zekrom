from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "./data/database.sqlite3")

SNMP_LISTEN_PORT = int(os.getenv("SNMP_LISTEN_PORT", 162))
SNMP_COMMUNITY = os.getenv("SNMP_COMMUNITY", "public")

SSH_USERNAME = os.getenv("SSH_USERNAME", "admin")
SSH_PASSWORD = os.getenv("SSH_PASSWORD", "admin123")

