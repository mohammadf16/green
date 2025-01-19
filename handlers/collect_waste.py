from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from database import update_user_tokens

# مراحل ثبت پسماند
WASTE_TYPE, WASTE_AMOUNT, COLLECTION_DAY, COLLECTION_ADDRESS = range(4)

# شروع ثبت پسماند
async def start_collect_waste(update, context):
    keyboard = [
        [InlineKeyboardButton("پلاستیک", callback_data='plastic')],
        [InlineKeyboardButton("شیشه", callback_data='glass')],
        [InlineKeyboardButton("فلز", callback_data='metal')],
        [InlineKeyboardButton("کاغذ", callback_data='paper')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفاً نوع پسماند را انتخاب کنید:", reply_markup=reply_markup)
    return WASTE_TYPE

# دریافت نوع پسماند
async def get_waste_type(update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['waste_type'] = query.data
    await query.edit_message_text(f"شما {query.data} را انتخاب کردید. لطفاً مقدار پسماند (وزن) را وارد کنید:")
    return WASTE_AMOUNT

# دریافت مقدار پسماند
async def get_waste_amount(update, context):
    context.user_data['waste_amount'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("دوشنبه", callback_data='Monday')],
        [InlineKeyboardButton("پنج‌شنبه", callback_data='Thursday')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفاً روز جمع‌آوری را انتخاب کنید:", reply_markup=reply_markup)
    return COLLECTION_DAY

# دریافت روز جمع‌آوری
async def get_collection_day(update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['collection_day'] = query.data
    await query.edit_message_text(f"روز جمع‌آوری: {query.data}. لطفاً آدرس خود را وارد کنید:")
    return COLLECTION_ADDRESS

# دریافت آدرس و ذخیره اطلاعات
async def get_collection_address(update, context):
    context.user_data['collection_address'] = update.message.text

    # اطلاعات پسماند
    waste_type = context.user_data['waste_type']
    waste_amount = float(context.user_data['waste_amount'])
    collection_day = context.user_data['collection_day']
    collection_address = context.user_data['collection_address']

    # پیام تایید
    await update.message.reply_text(
        f"درخواست شما ثبت شد:\n"
        f"- نوع پسماند: {waste_type}\n"
        f"- مقدار: {waste_amount} کیلوگرم\n"
        f"- روز جمع‌آوری: {collection_day}\n"
        f"- آدرس: {collection_address}\n"
        f"✅ منتظر تایید مدیر باشید."
    )
    return ConversationHandler.END

# ایجاد ConversationHandler
collect_waste_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^(ثبت پسماند)$"), start_collect_waste)],
    states={
        WASTE_TYPE: [CallbackQueryHandler(get_waste_type)],
        WASTE_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_waste_amount)],
        COLLECTION_DAY: [CallbackQueryHandler(get_collection_day)],
        COLLECTION_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_collection_address)],
    },
    fallbacks=[]
)
