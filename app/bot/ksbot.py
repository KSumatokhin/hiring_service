from conf import TOKEN
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, ContextTypes, ConversationHandler,
    CallbackQueryHandler, MessageHandler, filters
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

MAIN_MENU, GREETING, SEARCH_USER = range(3)

users = [
    {"first_name": "Иван", "last_name": "Иванов"},
    {"first_name": "Семен", "last_name": "Семенов"},
    {"first_name": "Петр", "last_name": "Петров"},
    {"first_name": "Алексей", "last_name": "Алексеев"},
    {"first_name": "Дмитрий", "last_name": "Дмитриев"},
]

# Выносим клавиатуру в отдельную переменную
main_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Приветствие", callback_data="/greet")],
    [InlineKeyboardButton("Информация о пользователях",
                          callback_data="/user_info")],
    [InlineKeyboardButton("Отмена", callback_data="/cancel")],
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Выберите действие:", reply_markup=main_menu_keyboard)
    return MAIN_MENU


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    command = query.data

    if command == "/greet":
        await query.edit_message_text("Как вас зовут?")
        return GREETING
    elif command == "/user_info":
        await query.edit_message_text("Введите имя или фамилию пользователя:")
        return SEARCH_USER
    elif command == "/cancel":
        await query.edit_message_text(
            "Действие отменено. Возвращаемся в главное меню.",
            reply_markup=main_menu_keyboard,
        )
        return MAIN_MENU
    else:
        await query.edit_message_text(
            "Неизвестная команда. Возвращаемся в главное меню.",
            reply_markup=main_menu_keyboard,
        )
        return MAIN_MENU


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name = update.message.text
    await update.message.reply_text(
        f"Здравствуй, мой новый друг {user_name}!",
        reply_markup=main_menu_keyboard,
    )
    return MAIN_MENU


async def search_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_query = update.message.text
    found_users = [
        user for user in users
        if search_query.lower() in user["first_name"].lower() or
        search_query.lower() in user["last_name"].lower()
    ]

    if found_users:
        user_info = "\n".join([f"{user['first_name']} {user['last_name']}"
                              for user in found_users])
        await update.message.reply_text(
            f"Найденные пользователи:\n\n{user_info}",
            reply_markup=main_menu_keyboard,
        )
    else:
        await update.message.reply_text(
            "Такого пользователя нет.",
            reply_markup=main_menu_keyboard,
        )

    return MAIN_MENU


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Пожалуйста, выберите действие из предложенных кнопок.",
        reply_markup=main_menu_keyboard,
    )
    return MAIN_MENU


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(main_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text),
            ],
            GREETING: [MessageHandler(filters.TEXT & ~filters.COMMAND, greeting)],
            SEARCH_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_user)],
        },
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()