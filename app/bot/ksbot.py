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

MAIN_MENU, GREETING, SEARCH_USER, SHOW_USER_INFO = range(4)

users = [
    {"first_name": "Иван", "last_name": "Иванов", "age": 25, "city": "Москва"},
    {"first_name": "Семен", "last_name": "Семенов", "age": 30, "city": "Санкт-Петербург"},
    {"first_name": "Петр", "last_name": "Петров", "age": 35, "city": "Новосибирск"},
    {"first_name": "Алексей", "last_name": "Алексеев", "age": 40, "city": "Екатеринбург"},
    {"first_name": "Дмитрий", "last_name": "Дмитриев", "age": 45, "city": "Казань"},
]

main_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Приветствие", callback_data="/greet")],
    [InlineKeyboardButton("Информация о пользователях", callback_data="/user_info")],
])

search_user_keyboard = InlineKeyboardMarkup([
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
        await query.edit_message_text("Введите имя или фамилию пользователя:", reply_markup=search_user_keyboard)
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
    await update.message.reply_text(f"Здравствуй, мой новый друг {user_name}!")
    await update.message.reply_text("Выберите действие:", reply_markup=main_menu_keyboard)
    return MAIN_MENU


async def search_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_query = update.message.text

    found_users = [
        (index, user) for index, user in enumerate(users)
        if search_query.lower() in user["first_name"].lower() or
        search_query.lower() in user["last_name"].lower()
    ]

    if found_users:
        keyboard = [
            [InlineKeyboardButton(
                f"{user['first_name']} {user['last_name']}", callback_data=f"user_{index}")]
            for index, user in found_users
        ]
        keyboard.append(
            [InlineKeyboardButton("Отмена", callback_data="/cancel")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Найденные пользователи:",
            reply_markup=reply_markup,
        )
        return SHOW_USER_INFO
    else:
        await update.message.reply_text(
            "Такого пользователя нет. Введите имя или фамилию пользователя:",
            reply_markup=search_user_keyboard,
        )
        return SEARCH_USER


async def show_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_index = int(query.data.split("_")[1])
    user = users[user_index]

    user_info = (
        f"Информация о пользователе:\n\n"
        f"Имя: {user['first_name']}\n"
        f"Фамилия: {user['last_name']}\n"
        f"Возраст: {user['age']}\n"
        f"Город: {user['city']}"
    )

    await query.edit_message_text(user_info)
    await query.message.reply_text("Выберите действие:", reply_markup=main_menu_keyboard)
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
            SEARCH_USER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_user),
                CallbackQueryHandler(main_menu)
            ],
            SHOW_USER_INFO: [CallbackQueryHandler(show_user_info, pattern="^user_")],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()