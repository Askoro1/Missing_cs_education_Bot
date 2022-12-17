from typing import Union
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ConversationHandler, ContextTypes
import sqlite3 as sql
from .gen_tasks import send_task_message
from .help import bot_help

async def my_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sql.connect('database/study_bot.db')
    user_id = update.message.from_user.id
    query_db = conn.cursor()
    query_db.execute(
        f"""SELECT * FROM Students WHERE ID = "{user_id}" ORDER BY RANDOM() LIMIT 1;""")
    res = query_db.fetchone()
    success_solve = res[3]
    attempts = res[4]
    await context.bot.send_message(
        text=f"Вы решили правильно: {success_solve} задач \n"
             f"Вы пробовали решить: {attempts} задач",
        chat_id=update.message.chat_id)
    keyboard = [
        [
            InlineKeyboardButton("Выйти к списку команд", callback_data="Выйти к списку команд")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Что дальше?", reply_markup=reply_markup)
    return 'what_to_do'