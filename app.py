import os
import re
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

WAITING_ORDER = 1

def get_main_keyboard():
    buttons = [
        [KeyboardButton("📋 Тарифы"), KeyboardButton("📞 Заказать бота")],
        [KeyboardButton("ℹ️ О нас")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['in_order'] = False
    await update.message.reply_text(
        "👋 Добро пожаловать в студию по разработке Telegram-ботов!\n\n"
        "Я помогу вам выбрать и заказать бота для вашего бизнеса.\n"
        "Используйте кнопки ниже, или просто напишите свой вопрос.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

async def show_tariffs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 **Наши тарифы**\n\n"
        "🔹 **Базовый** – от 500 ₽\n"
        "   - Создание простого бота для бизнеса или личных нужд\n"
        "   - Бесплатный хостинг (может быть нестабилен, подвержен атакам, бота могут отключить)\n"
        "   - Клиент самостоятельно управляет бесплатным хостингом\n"
        "   - Поддержка и обслуживание – 1 месяц\n\n"
        "🔹 **Продвинутый** – от 1000 ₽ + стоимость хостинга\n"
        "   - Создание бота с базой данных (SQLite, PostgreSQL)\n"
        "   - Качественный платный хостинг (надёжность, скорость)\n"
        "   - Полное обслуживание и поддержка\n"
        "   - Стоимость хостинга обсуждается отдельно с клиентом\n\n"
        "Для заказа нажмите кнопку «Заказать бота»."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ **О нас**\n\n"
        "Мы — команда разработчиков с опытом создания ботов для бизнеса.\n"
        "Работаем быстро, качественно, с гарантией.\n"
        "Свяжитесь с нами через кнопку «Заказать бота» или просто напишите."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Опишите, какой бот вам нужен.\n"
        "Напишите в одном сообщении:\n"
        "- цель бота\n"
        "- какие функции нужны\n"
        "- бюджет\n"
        "- контактные данные\n\n"
        "Я передам вашу заявку разработчику."
    )
    context.user_data['in_order'] = True
    return WAITING_ORDER

async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🆕 **Новая заявка!**\n"
             f"👤 От: {user.full_name} (ID: {user.id})\n"
             f"📩 Текст заявки:\n{text}"
    )

    await update.message.reply_text(
        "✅ Ваша заявка отправлена! Мы свяжемся с вами в ближайшее время.\n"
        "Вернуться в меню — нажмите /start",
        reply_markup=get_main_keyboard()
    )
    context.user_data['in_order'] = False
    return ConversationHandler.END

# Пересылка любых сообщений от клиентов админу
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == ADMIN_ID:
        return
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"💬 Сообщение от {user.full_name} (ID: {user.id}):\n{update.message.text}"
    )
    await update.message.reply_text(
        "✅ Ваше сообщение передано менеджеру. Мы ответим вам в ближайшее время."
    )

# Обработка ответов администратора
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if update.message.reply_to_message:
        original = update.message.reply_to_message.text
        match = re.search(r'ID:\s*(\d+)', original)
        if match:
            user_id = int(match.group(1))
            await context.bot.send_message(chat_id=user_id, text=update.message.text)
            await update.message.reply_text("✅ Ответ отправлен клиенту.")
        else:
            await update.message.reply_text("⚠️ Не удалось определить клиента.")
    else:
        await update.message.reply_text(
            "ℹ️ Чтобы ответить клиенту, нажмите «Ответить» на его сообщении в этом чате."
        )

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('in_order'):
        return await receive_order(update, context)
    if update.effective_user.id != ADMIN_ID:
        return await forward_to_admin(update, context)
    await update.message.reply_text(
        "Используйте кнопки меню или ответьте на сообщение клиента.",
        reply_markup=get_main_keyboard()
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['in_order'] = False
    await update.message.reply_text(
        "Диалог отменён. Возвращаю в меню.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(📞 Заказать бота)$"), start_order)],
        states={
            WAITING_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_order)],
        },
        fallbacks=[CommandHandler("start", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.Regex("^(📋 Тарифы)$"), show_tariffs))
    app.add_handler(MessageHandler(filters.Regex("^(ℹ️ О нас)$"), about_us))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), handle_admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    print("🚀 Бот запущен на хостинге!")
    app.run_polling()

if __name__ == "__main__":
    main()
