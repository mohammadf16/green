from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from database import fetch_user

# هندلر برای مدیریت دستور /start
async def start(update, context):
    telegram_id = update.message.from_user.id

    # بررسی وضعیت ثبت‌نام کاربر
    user = fetch_user(telegram_id)

    if not user:
        # کاربر ثبت‌نام نکرده است
        keyboard = [[
            "ثبت‌نام"
        ]]
        message = "سلام! لطفاً ابتدا ثبت‌نام کنید:"
    else:
        # کاربر ثبت‌نام کرده است
        keyboard = [
            ["ثبت پسماند"],
            ["مشاهده درخواست‌ها", "مشاهده توکن‌ها"]
        ]
        message = f"سلام {user[2]}! از گزینه‌های زیر استفاده کنید:"

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(message, reply_markup=reply_markup)

# ایجاد CommandHandler
start_handler = CommandHandler("start", start)
