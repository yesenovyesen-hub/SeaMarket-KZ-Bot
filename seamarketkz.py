# ==========================================
# 1. IMPORTS
# ==========================================
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==========================================
# 2. CONFIGURATION
# ==========================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваш токен
BOT_TOKEN = "8774317260:AAG1bbjiOj-Er2YpStSWZDNUaqYftGRPEdo"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден!")

# ==========================================
# 3. URLS
# ==========================================
MVP_URL = "https://yesenovyesen-hub.github.io/SeaMarket-KZ/"
FINAL_URL = "https://yesenovyesen-hub.github.io/SeaMarketKZ-final-version-/"

def main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🌊 Открыть MVP", url=MVP_URL)],
        [InlineKeyboardButton("🚀 Открыть финальную версию", url=FINAL_URL)],
        [InlineKeyboardButton("✅ Подтвердить оформление заказа", callback_data="confirm_order")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ==========================================
# 4. /START
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("User started the bot")
    text = (
        "🌊 **Добро пожаловать в SeaMarket KZ!**\n\n"
        "Это Telegram-проводник нашего проекта.\n\n"
        "Здесь вы можете:\n"
        "• открыть MVP-версию;\n"
        "• открыть финальную версию;\n"
        "• перейти к оформлению заказа."
    )
    await update.message.reply_text(
        text,
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

# ==========================================
# 5. /HELP
# ==========================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "🌊 **SeaMarket KZ**\n\n"
        "Используйте /start, чтобы открыть главное меню.\n\n"
        "Через бота можно:\n"
        "• открыть MVP;\n"
        "• открыть финальную версию;\n"
        "• перейти к оформлению заказа."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ==========================================
# 6. /ABOUT
# ==========================================
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "🌊 **SeaMarket KZ**\n\n"
        "Онлайн-сервис морских продуктов и товаров с доставкой по Казахстану.\n\n"
        "Рыба • морепродукты • еда • аксессуары • рыбалка"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Открыть финальную версию", url=FINAL_URL)]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

# ==========================================
# 7. /SITE
# ==========================================
async def site_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌊 MVP", url=MVP_URL)],
        [InlineKeyboardButton("🚀 Финальная версия", url=FINAL_URL)]
    ])
    await update.message.reply_text(
        "Выберите интересующую вас версию сайта SeaMarket KZ:",
        reply_markup=keyboard
    )

# ==========================================
# 8. /ORDER
# ==========================================
async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "✅ **Переход к оформлению заказа**\n\n"
        "Для оформления заказа используйте финальную версию SeaMarket KZ."
    )
    # В дальнейшем сюда можно добавить интеграцию с backend/payment API.
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Открыть финальную версию", url=FINAL_URL)]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

# ==========================================
# 9. /CANCEL
# ==========================================
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Действие отменено.")

# ==========================================
# 10. CALLBACK HANDLERS
# ==========================================
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    text = (
        "✅ **Оформление заказа подтверждено!**\n\n"
        "Для продолжения перейдите в финальную версию SeaMarket KZ."
    )
    # В дальнейшем сюда можно добавить интеграцию с backend/payment API.
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Перейти к оформлению", url=FINAL_URL)]
    ])
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

# ==========================================
# 11. ERROR HANDLER
# ==========================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
        )

# ==========================================
# 12. MAIN
# ==========================================
def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("site", site_command))
    application.add_handler(CommandHandler("order", order_command))
    application.add_handler(CommandHandler("cancel", cancel_command))

    application.add_handler(CallbackQueryHandler(confirm_order, pattern="^confirm_order$"))
    application.add_error_handler(error_handler)

    print("🌊 SeaMarket KZ Bot started")
    application.run_polling()

if __name__ == "__main__":
    main()