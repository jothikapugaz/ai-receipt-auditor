import sqlite3

def create_table():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_expense(store_name, amount, category, date):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (store_name, amount, category, date)
        VALUES (?, ?, ?, ?)
    ''', (store_name, amount, category, date))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT store_name, amount, category, date FROM expenses ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows
