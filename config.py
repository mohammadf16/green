import os

# توکن ربات تلگرام
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# مسیر دیتابیس SQLite
DATABASE_PATH = os.getenv("DATABASE_PATH", "local_database.db")
