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
        "Уважаемый клиент!\n\n"
        "Добро пожаловать в студию разработки Telegram-ботов.\n"
        "Мы предлагаем готовые решения для автоматизации бизнеса в различных направлениях:\n"
        "• салоны красоты (запись, портфолио, админ-панель);\n"
        "• розничная торговля, услуги, образование и другие сферы.\n\n"
        "Наши боты позволяют организовать удобную запись клиентов,\n"
        "демонстрировать портфолио, управлять заказами и аналитикой\n"
        "через интуитивно понятную панель управления.\n\n"
        "Для получения подробной информации воспользуйтесь кнопками ниже.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

async def show_tariffs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 **Тарифы**\n\n"
        "🔹 **Базовый** – от 500 ₽\n"
        "   - Разработка базового бота для бизнеса или личного использования;\n"
        "   - Бесплатный хостинг (клиент может управлять им самостоятельно\n"
        "     или с нашей помощью – по вашему желанию);\n"
        "   - Техническая поддержка и обслуживание – **от 1 месяца**\n"
        "     (далее 199 ₽/мес);\n"
        "   - Возможность подключения платного хостинга – по усмотрению клиента.\n\n"
        "🔹 **Продвинутый** – от 1000 ₽ + стоимость хостинга\n"
        "   - Разработка бота с использованием баз данных (SQLite, PostgreSQL);\n"
        "   - Размещение на надёжном платном хостинге (высокая доступность, скорость);\n"
        "   - Полное сопровождение и техническая поддержка;\n"
        "   - Минимальная стоимость хостинга – от 100 ₽/мес (зависит от нагрузки).\n\n"
        "🖌️ **Для всех тарифов** – мы подбираем индивидуальное визуальное оформление\n"
        "   совместно с клиентом (цветовая гамма, логотип, стиль общения).\n\n"
        "📢 **Дополнительные опции** – интеграция рекламных блоков внутри бота\n"
        "   или обязательная подписка на ваш Telegram-канал.\n"
        "   Это позволит вам привлекать новых подписчиков и повысить узнаваемость.\n\n"
        "Для оформления заказа воспользуйтесь кнопкой «Заказать бота»."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ **О нас**\n\n"
        "Мы — команда разработчиков, специализирующаяся на создании Telegram-ботов для бизнеса.\n"
        "Наш ведущий специалист имеет высшее техническое образование и успешно окончил\n"
        "**очный курс программирования на Python от МФТИ (Московского физико-технического института)**,\n"
        "что подтверждено соответствующим сертификатом. Является Junior-программистом Python.\n\n"
        "Мы гарантируем высокое качество работ, соблюдение согласованных сроков\n"
        "и индивидуальный подход к каждому проекту.\n"
        "Для сотрудничества воспользуйтесь кнопкой «Заказать бота» или напишите нам напрямую."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 **Оформление заявки**\n\n"
        "Просим вас описать требования к будущему боту в одном сообщении:\n"
        "- цель создания бота и сфера деятельности;\n"
        "- необходимый функционал (запись, портфолио, админ-панель и т.п.);\n"
        "- предполагаемый бюджет;\n"
        "- контактные данные (Telegram, телефон).\n\n"
        "Дополнительно укажите, требуется ли интеграция рекламных блоков\n"
        "или обязательная подписка на ваш Telegram-канал – мы реализуем это.\n\n"
        "Ответ будет направлен вам в течение 12 часов.\n\n"
        "После отправки заявки вы получите подтверждение."
    )
    context.user_data['in_order'] = True
    return WAITING_ORDER

async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🆕 **Новая заявка**\n"
             f"👤 Клиент: {user.full_name} (ID: {user.id})\n"
             f"📩 Текст заявки:\n{text}"
    )

    await update.message.reply_text(
        "✅ Ваша заявка принята. Мы свяжемся с вами в ближайшее время (обычно в течение 12 часов).\n"
        "Для возврата в главное меню нажмите /start",
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
        text=f"💬 Сообщение от {user.full_name} (ID: {user.id}):\n{update.message.text}"
    )
    await update.message.reply_text(
        "✅ Ваше сообщение передано менеджеру. Ответ будет направлен вам в течение 12 часов."
    )

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
            await update.message.reply_text("⚠️ Не удалось определить адресата.")
    else:
        await update.message.reply_text(
            "ℹ️ Для ответа клиенту нажмите «Ответить» на его сообщении в этом чате."
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
        "Диалог отменён. Вы возвращены в главное меню.",
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

    print("🚀 Бот успешно запущен и готов к работе.")
    app.run_polling()

if __name__ == "__main__":
    main()
