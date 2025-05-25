import sqlite3

DB_NAME = 'files.db'

def init_db():
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            category TEXT,
            dropbox_link TEXT,
            title TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_file(filename, category, dropbox_link, title):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO documents (filename, category, dropbox_link, title)
        VALUES (?, ?, ?, ?)
    ''', (filename, category, dropbox_link, title))
    conn.commit()
    conn.close()


def get_all_files():
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('SELECT * FROM documents')
    rows = c.fetchall()
    conn.close()
    return rows


