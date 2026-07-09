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
        [KeyboardButton("📋 Тарифы"), KeyboardButton("📩 Заказать бота")],
        [KeyboardButton("ℹ️ О студии")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['in_order'] = False
    await update.message.reply_photo(
        photo="https://via.placeholder.com/800x200/FFFFFF/1E90FF?text=Студия+разработки+ботов",
        caption=(
            "💎 *Уважаемый клиент!*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Вы обратились в студию разработки Telegram-ботов.\n"
            "Мы создаём автоматизированные решения для бизнеса:\n\n"
            "❄️ запись клиентов и управление расписанием;\n"
            "🌀 демонстрация портфолио и услуг;\n"
            "🌊 администрирование заказов через панель управления;\n"
            "💠 интеграция с внешними сервисами.\n\n"
            "Наши разработки адаптированы под различные сферы:\n"
            "💅 салоны красоты, 🛍️ розница, 🎓 образование, и другие.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📌 *Ознакомьтесь с тарифами или оставьте заявку* —\n"
            "мы подготовим индивидуальное предложение.\n\n"
            "👇 Используйте кнопки ниже для навигации."
        ),
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END
async def show_tariffs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💼 *НАШИ ТАРИФЫ*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔹 *Базовый* – от 500 ₽\n"
        "   • Разработка базового бота для бизнеса или личного использования\n"
        "   • Бесплатный хостинг (управление – самостоятельно или с нашей помощью)\n"
        "   • Техническая поддержка и обслуживание – *от 1 месяца* (далее 199 ₽/мес)\n"
        "   • Возможность перехода на платный хостинг – по вашему желанию\n\n"
        "🔹 *Продвинутый* – от 1000 ₽ + стоимость хостинга\n"
        "   • Бот с базой данных (SQLite / PostgreSQL)\n"
        "   • Размещение на надёжном платном хостинге (высокая доступность и скорость)\n"
        "   • Полное сопровождение и техническая поддержка\n"
        "   • Стоимость хостинга – от 100 ₽/мес (зависит от нагрузки)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🖌️ *Для всех тарифов* – мы разрабатываем индивидуальный дизайн:\n"
        "   цветовая схема, логотип, тональность общения – всё под ваш бренд.\n\n"
        "📢 *Дополнительные опции (любой тариф):*\n"
        "   • Встроенная реклама внутри бота\n"
        "   • Обязательная подписка на ваш Telegram-канал – привлекайте новых клиентов!\n\n"
        "📩 Для заказа нажмите кнопку «Заказать бота» в главном меню."
    )
    await update.message.reply_text(text, parse_mode="Markdown")
async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo="",
        caption=(
            "ℹ️ *О НАШЕЙ СТУДИИ*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Мы — небольшая студия разработчиков, специализирующаяся на создании Telegram-ботов\n"
            "для бизнеса. Наш ведущий специалист имеет сертификат об окончании\n"
            "*очного курса программирования на Python от МФТИ (Московского физико-технического института)*\n"
            "и является Junior-программистом Python.\n\n"
            "🔹 *Наши принципы:*\n"
            "   ✅ Качество и надёжность кода\n"
            "   ✅ Соблюдение согласованных сроков\n"
            "   ✅ Индивидуальный подход к каждому проекту\n"
            "   ✅ Открытость и честность в ценообразовании\n"
            "   ✅ Личное участие в проекте на всех этапах\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📬 Для сотрудничества воспользуйтесь кнопкой «Заказать бота»\n"
            "или напишите нам напрямую – мы всегда на связи."
        ),
        parse_mode="Markdown"
    )
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 *ОФОРМЛЕНИЕ ЗАЯВКИ*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Пожалуйста, опишите ваш проект в одном сообщении. Укажите:\n\n"
        "❄️ *Цель и сфера* – для чего нужен бот, какая у вас деятельность\n"
        "🌀 *Функционал* – запись, портфолио, админ-панель, онлайн-оплата и т.д.\n"
        "🌊 *Бюджет* – желаемый диапазон стоимости\n"
        "💠 *Контактные данные* – ваш Telegram, телефон (для оперативной связи)\n\n"
        "Дополнительно отметьте, хотите ли вы:\n"
        "• Встроить рекламные блоки\n"
        "• Сделать обязательную подписку на ваш Telegram-канал\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⏳ *Ожидайте ответа в течение 12 часов* – мы изучим ваши пожелания\n"
        "и подготовим предложение.\n\n"
        "Для отмены диалога нажмите /start."
    )
    await update.message.reply_text(text, parse_mode="Markdown")
    context.user_data['in_order'] = True
    return WAITING_ORDER
async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🆕 *НОВАЯ ЗАЯВКА*\n"
             f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
             f"👤 Клиент: {user.full_name} (ID: `{user.id}`)\n"
             f"📩 Текст заявки:\n{text}",
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        "✅ *Ваша заявка принята!*\n\n"
        "Мы свяжемся с вами в ближайшее время (обычно в течение 12 часов).\n"
        "Чтобы вернуться в главное меню, нажмите /start.",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
    context.user_data['in_order'] = False
    return ConversationHandler.END
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == ADMIN_ID:
        return
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"💬 *Сообщение от клиента*\n"
             f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
             f"👤 {user.full_name} (ID: `{user.id}`):\n{update.message.text}",
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        "✅ *Сообщение доставлено менеджеру.*\n"
        "Ответ придёт в течение 12 часов.",
        parse_mode="Markdown"
    )
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if update.message.reply_to_message:
        original = update.message.reply_to_message.text
        match = re.search(r'ID:\s*(\d+)', original)
        if match:
            user_id = int(match.group(1))
            reply_text = f"👨‍💼 *Ответ менеджера:*\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{update.message.text}"
            await context.bot.send_message(
                chat_id=user_id,
                text=reply_text,
                parse_mode="Markdown"
            )
            await update.message.reply_text("✅ *Ответ успешно отправлен клиенту.*", parse_mode="Markdown")
        else:
            await update.message.reply_text(
                "⚠️ *Не удалось определить получателя.*\n"
                "Убедитесь, что вы отвечаете на сообщение, пересланное от клиента.",
                parse_mode="Markdown"
            )
    else:
        await update.message.reply_text(
            "ℹ️ *Чтобы ответить клиенту,* нажмите «Ответить» на его сообщении в этом чате.",
            parse_mode="Markdown"
        )
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('in_order'):
        return await receive_order(update, context)
    if update.effective_user.id != ADMIN_ID:
        return await forward_to_admin(update, context)
    await update.message.reply_text(
        "Используйте, пожалуйста, кнопки меню для навигации.",
        reply_markup=get_main_keyboard()
    )
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['in_order'] = False
    await update.message.reply_text(
        "⏹ *Диалог отменён.* Вы вернулись в главное меню.",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(📩 Заказать бота)$"), start_order)],
        states={
            WAITING_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_order)],
        },
        fallbacks=[CommandHandler("start", cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.Regex("^(📋 Тарифы)$"), show_tariffs))
    app.add_handler(MessageHandler(filters.Regex("^(ℹ️ О студии)$"), about_us))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), handle_admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    print("🚀 Бот запущен в обновлённом стиле (бело-синий дизайн).")
    app.run_polling()
if __name__ == "__main__":
    main()
