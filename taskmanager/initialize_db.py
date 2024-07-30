import sqlite3

def initialize_db():
    # Conectar ao banco de dados SQLite (ou criar o banco se não existir)
    conn = sqlite3.connect('task_reports.db')
    cursor = conn.cursor()
    
    # Criar a tabela para armazenar informações sobre os relatórios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chame a função para inicializar o banco de dados
if __name__ == '__main__':
    initialize_db()
