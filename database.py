import sqlite3
from config import DATABASE_PATH

# اتصال به دیتابیس
conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
cursor = conn.cursor()

# ایجاد جداول
def initialize_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            name TEXT,
            phone TEXT,
            address TEXT,
            tokens INTEGER DEFAULT 0,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            waste_type TEXT,
            quantity INTEGER,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

# توابع کمکی دیتابیس
def fetch_user(telegram_id):
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    return cursor.fetchone()

def add_user(telegram_id, name, phone):
    cursor.execute("""
        INSERT INTO users (telegram_id, name, phone)
        VALUES (?, ?, ?)
        ON CONFLICT(telegram_id) DO NOTHING
    """, (telegram_id, name, phone))
    conn.commit()

def update_user_tokens(telegram_id, tokens):
    cursor.execute("""
        UPDATE users
        SET tokens = tokens + ?
        WHERE telegram_id = ?
    """, (tokens, telegram_id))
    conn.commit()
