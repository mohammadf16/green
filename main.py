from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start import start_handler
from handlers.register import register_handler
from handlers.collect_waste import collect_waste_handler
from handlers.admin import admin_handler

# توکن ربات (در فایل config.py ذخیره شده)
from config import TELEGRAM_BOT_TOKEN

def main():
    # ساخت اپلیکیشن ربات
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # اضافه کردن هندلرها
    app.add_handler(start_handler)
    app.add_handler(register_handler)
    app.add_handler(collect_waste_handler)
    app.add_handler(admin_handler)

    print("ربات در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()
