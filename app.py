import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
load_dotenv()
BOT_TOKEN = os.environ['BOT_TOKEN']
ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))
WELCOME_IMAGE_URL = os.environ.get('WELCOME_IMAGE_URL')
WAITING_ORDER = 1
LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📋 Тарифы", callback_data="tariffs")],
        [InlineKeyboardButton("📩 Заказать бота", callback_data="order")],
        [InlineKeyboardButton("ℹ️ О студии", callback_data="about")]
    ]
    return InlineKeyboardMarkup(keyboard)
def get_cancel_keyboard():
    keyboard = [[InlineKeyboardButton("❌ Отменить заказ", callback_data="cancel_order")]]
    return InlineKeyboardMarkup(keyboard)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['in_order'] = False
    caption = (
        f"✨ *Уважаемый клиент!* ✨\n"
        f"{LINE}\n\n"
        "Вы обратились в студию разработки Telegram-ботов.\n"
        "Мы создаём *автоматизированные решения* для вашего бизнеса.\n\n"
        "💎 *Что мы предлагаем:*\n"
        "   ❄️ Запись клиентов и управление расписанием\n"
        "   🌀 Демонстрация портфолио и услуг\n"
        "   🌊 Администрирование заказов через панель управления\n"
        "   💠 Интеграция с внешними сервисами и CRM\n"
        "   🧠 Генерация идей для YouTube-контента\n"
        "   🛡️ Техническая поддержка для сайтов и бизнеса\n\n"
        "📌 *Сферы, в которых мы работаем:*\n"
        "   💅 Салоны красоты\n"
        "   🛍️ Розничная торговля\n"
        "   🎓 Образование и курсы\n"
        "   🏢 Корпоративный сектор\n"
        "   🎬 YouTube-блогеры и создатели контента\n"
        "   🌐 Интернет-магазины, сайты и онлайн-сервисы\n"
        "   и другие — подберём решение под ваши задачи.\n\n"
        f"{LINE}\n"
        "📌 *Ознакомьтесь с тарифами* или *оставьте заявку* —\n"
        "мы подготовим индивидуальное коммерческое предложение.\n\n"
        "👇 *Нажмите на кнопку ниже, чтобы продолжить*"
    )
    if WELCOME_IMAGE_URL:
        try:
            await update.message.reply_photo(photo=WELCOME_IMAGE_URL, caption=caption, parse_mode="Markdown", reply_markup=get_main_keyboard())
        except Exception:
            await update.message.reply_text(caption, parse_mode="Markdown", reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text(caption, parse_mode="Markdown", reply_markup=get_main_keyboard())
    return ConversationHandler.END
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "tariffs":
        await show_tariffs(update, context)
    elif data == "order":
        await start_order(update, context)
    elif data == "about":
        await about_us(update, context)
    elif data == "cancel_order":
        await cancel(update, context)
async def show_tariffs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"💼 *НАШИ ТАРИФЫ*\n"
        f"{LINE}\n\n"
        "🔹 *Базовый* – от 549 ₽\n"
        "   • Разработка базового бота для бизнеса или личного использования\n"
        "   • Бесплатный хостинг (управление – самостоятельно или с нашей помощью)\n"
        "   • Техническая поддержка и обслуживание – *от 1 месяца* (далее 199 ₽/мес)\n"
        "   • Возможность перехода на платный хостинг – по вашему желанию\n\n"
        "🔹 *Продвинутый* – от 1049 ₽ + стоимость хостинга\n"
        "   • Бот с базой данных (SQLite / PostgreSQL)\n"
        "   • Размещение на надёжном платном хостинге (высокая доступность и скорость)\n"
        "   • Полное сопровождение и техническая поддержка\n"
        "   • Стоимость хостинга – от 99 ₽/мес (зависит от нагрузки)\n\n"
        f"{LINE}\n"
        "🖌️ *Для всех тарифов* – мы разрабатываем индивидуальный дизайн:\n"
        "   цветовая схема, логотип, тональность общения – всё под ваш бренд.\n\n"
        "📢 *Дополнительные опции (любой тариф):*\n"
        "   • Встроенная реклама внутри бота\n"
        "   • Обязательная подписка на ваш Telegram-канал – привлекайте новых клиентов!\n"
        "   • Размещение исходного кода на GitHub (по вашему желанию)\n"
        "   • Внесение изменений и доработок в любое время после сдачи проекта (стоимость зависит от сложности)\n"
        "   • Боты для YouTube (генерация идей, интерактивные опросы, аналитика)\n"
        "   • Боты для техподдержки сайтов, онлайн-магазинов, CRM-интеграция\n\n"
        "📩 Для заказа нажмите кнопку «Заказать бота» в главном меню."
    )
    await update.effective_message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())
async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"ℹ️ *О НАШЕЙ СТУДИИ*\n"
        f"{LINE}\n\n"
        "Мы — небольшая студия разработчиков, специализирующаяся на создании Telegram-ботов для бизнеса.\n"
        "Наш ведущий специалист имеет сертификат об окончании\n"
        "*очного курса программирования на Python от МФТИ (Московского физико-технического института)*\n"
        "и является Junior-программистом Python.\n\n"
        "🔹 *Наши принципы:*\n"
        "   ✅ Качество и надёжность кода\n"
        "   ✅ Соблюдение согласованных сроков\n"
        "   ✅ Индивидуальный подход к каждому проекту\n"
        "   ✅ Открытость и честность в ценообразовании\n"
        "   ✅ Личное участие в проекте на всех этапах\n"
        "   ✅ Доступ к исходному коду (по желанию клиента, например, через GitHub)\n"
        "   ✅ Готовность дорабатывать бота под новые задачи в любой момент\n\n"
        "📌 *Примеры наших работ:*\n"
        "   • Боты для YouTube-каналов с генерацией идей для контента\n"
        "   • Боты-помощники для техподдержки сайтов и интернет-магазинов\n"
        "   • Автоматизация записи и управления клиентами в разных сферах\n\n"
        f"{LINE}\n"
        "📬 Для сотрудничества воспользуйтесь кнопкой «Заказать бота»\n"
        "или напишите нам напрямую – мы всегда на связи."
    )
    await update.effective_message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"📝 *ОФОРМЛЕНИЕ ЗАЯВКИ*\n"
        f"{LINE}\n\n"
        "Пожалуйста, опишите ваш проект в одном сообщении. Укажите:\n\n"
        "❄️ *Цель и сфера* – для чего нужен бот, какая у вас деятельность\n"
        "🌀 *Функционал* – запись, портфолио, админ-панель, онлайн-оплата, генерация идей, техподдержка и т.д.\n"
        "🌊 *Бюджет* – желаемый диапазон стоимости\n"
        "💠 *Контактные данные* – ваш Telegram, телефон (для оперативной связи)\n\n"
        "Дополнительно отметьте, хотите ли вы:\n"
        "• Встроить рекламные блоки\n"
        "• Сделать обязательную подписку на ваш Telegram-канал\n"
        "• Получить исходный код на GitHub\n\n"
        f"{LINE}\n"
        "⏳ *Ожидайте ответа в течение 12 часов* – мы изучим ваши пожелания\n"
        "и подготовим предложение.\n\n"
        "Для отмены диалога нажмите кнопку ниже."
    )
    await update.effective_message.reply_text(text, parse_mode="Markdown", reply_markup=get_cancel_keyboard())
    context.user_data['in_order'] = True
    return WAITING_ORDER
async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🆕 *НОВАЯ ЗАЯВКА*\n"
             f"{LINE}\n"
             f"👤 Клиент: {user.full_name} (ID: `{user.id}`)\n"
             f"📩 Текст заявки:\n{text}",
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        "✅ *Ваша заявка принята!*\n\n"
        "Мы свяжемся с вами в ближайшее время (обычно в течение 12 часов).\n"
        "Чтобы вернуться в главное меню, нажмите кнопку ниже.",
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
             f"{LINE}\n"
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
            reply_text = f"👨‍💼 *Ответ менеджера:*\n{LINE}\n{update.message.text}"
            await context.bot.send_message(chat_id=user_id, text=reply_text, parse_mode="Markdown")
            await update.message.reply_text("✅ *Ответ успешно отправлен клиенту.*", parse_mode="Markdown")
        else:
            await update.message.reply_text("⚠️ *Не удалось определить получателя.*\nУбедитесь, что вы отвечаете на сообщение, пересланное от клиента.", parse_mode="Markdown")
    else:
        await update.message.reply_text("ℹ️ *Чтобы ответить клиенту,* нажмите «Ответить» на его сообщении в этом чате.", parse_mode="Markdown")
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('in_order'):
        return await receive_order(update, context)
    if update.effective_user.id != ADMIN_ID:
        return await forward_to_admin(update, context)
    await update.message.reply_text("Используйте, пожалуйста, кнопки меню для навигации.", reply_markup=get_main_keyboard())
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['in_order'] = False
    await update.effective_message.reply_text("⏹ *Диалог отменён.* Вы вернулись в главное меню.", parse_mode="Markdown", reply_markup=get_main_keyboard())
    return ConversationHandler.END
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_order, pattern="^order$")],
        states={
            WAITING_ORDER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_order),
                CallbackQueryHandler(cancel, pattern="^cancel_order$")
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        per_message=True,
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(tariffs|order|about|cancel_order)$"))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), handle_admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    print("🚀 Бот запущен.")
    app.run_polling()
if __name__ == "__main__":
    main()
