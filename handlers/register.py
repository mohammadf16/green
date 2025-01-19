from telegram.ext import ConversationHandler, MessageHandler, filters
from database import add_user

# مراحل ثبت‌نام
NAME, PHONE = range(2)

# شروع ثبت‌نام
async def register_start(update, context):
    await update.message.reply_text("لطفاً نام خود را وارد کنید:")
    return NAME

# دریافت نام
async def get_name(update, context):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("لطفاً شماره تماس خود را وارد کنید:")
    return PHONE

# دریافت شماره تماس و تکمیل ثبت‌نام
async def get_phone(update, context):
    telegram_id = update.message.from_user.id
    name = context.user_data['name']
    phone = update.message.text

    # ذخیره اطلاعات کاربر در دیتابیس
    add_user(telegram_id, name, phone)

    await update.message.reply_text("ثبت‌نام شما با موفقیت انجام شد!")
    return ConversationHandler.END

# ایجاد ConversationHandler
register_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^(ثبت‌نام)$"), register_start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
    },
    fallbacks=[]
)
