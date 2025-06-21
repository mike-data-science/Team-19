import sqlite3
import os

DB_FILE = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filepath TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_file_to_db(filename, filepath):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO files (filename, filepath) VALUES (?, ?)', (filename, filepath))
    conn.commit()
    file_id = cursor.lastrowid
    conn.close()
    return file_id

def get_file_path(file_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT filepath FROM files WHERE id = ?', (file_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# Inițializează DB la pornire
init_db()
