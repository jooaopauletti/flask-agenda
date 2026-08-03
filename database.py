import sqlite3

def coluna_existe(cursor, tabela, coluna):
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [linha[1] for linha in cursor.fetchall()]
    return coluna in colunas

def criar_banco():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    if not coluna_existe(cursor, 'contatos', 'usuario_id'):
        cursor.execute('ALTER TABLE contatos ADD COLUMN usuario_id INTEGER')
    
    conn.commit()
    conn.close()