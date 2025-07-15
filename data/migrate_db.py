import sqlite3

def migrate_add_monitor_command():
    conn = sqlite3.connect("data/database.sqlite3")
    cursor = conn.cursor()
    
    # Verificar se a coluna já existe
    cursor.execute("PRAGMA table_info(devices)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'monitor_command' not in columns:
        # Adicionar a nova coluna com valor padrão
        cursor.execute("""
            ALTER TABLE devices 
            ADD COLUMN monitor_command TEXT DEFAULT 'uptime'
        """)
        print("Coluna monitor_command adicionada com sucesso!")
    else:
        print("Coluna monitor_command já existe.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_add_monitor_command()