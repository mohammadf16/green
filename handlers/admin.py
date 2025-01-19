from telegram.ext import CommandHandler
from database import cursor, conn

# مشاهده تمام درخواست‌ها
async def view_all_requests(update, context):
    telegram_id = update.message.from_user.id

    # بررسی دسترسی مدیر
    cursor.execute("""
        SELECT is_admin
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))
    user = cursor.fetchone()

    if not user or not user[0]:
        await update.message.reply_text("شما دسترسی لازم برای این بخش را ندارید.")
        return

    # استخراج تمام درخواست‌ها
    cursor.execute("""
        SELECT id, user_id, waste_type, quantity, status, created_at
        FROM requests
        ORDER BY created_at DESC
    """)
    requests = cursor.fetchall()

    if not requests:
        await update.message.reply_text("هیچ درخواستی برای مدیریت وجود ندارد.")
        return

    response = "📋 لیست درخواست‌ها:\n\n"
    for (req_id, user_id, waste_type, quantity, status, created_at) in requests:
        response += (
            f"🔢 درخواست {req_id}:\n"
            f"👤 کاربر: {user_id}\n"
            f"📦 نوع پسماند: {waste_type}\n"
            f"⚖️ مقدار: {quantity} کیلوگرم\n"
            f"📅 تاریخ: {created_at}\n"
            f"📌 وضعیت: {status}\n"
            f"-----------------------\n"
        )

    await update.message.reply_text(response)

# ایجاد CommandHandler
admin_handler = CommandHandler("view_requests", view_all_requests)
