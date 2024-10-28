import sqlite3

def initialize_db():
   
    conn = sqlite3.connect('task_reports.db')
    cursor = conn.cursor()
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    initialize_db()
