from typing import Optional, Union
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    ForceReply
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ConversationHandler, ContextTypes
import sqlite3 as sql
from .help import *


async def all_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(text="Введите название группы, задания которой вы хотите посмотреть.",
                                  chat_id=update.message.chat_id)
    return "input_group"


async def get_all_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    conn = sql.connect('database/study_bot.db')
    query_db = conn.cursor()
    query_db.execute(
        f"""SELECT * FROM All_Tasks WHERE GROUP_ID = "{message}";""")
    res = query_db.fetchall()
    if res is None or len(res) == 0:
        await context.bot.sendMessage(
            text="Такой группы не существует, создайте ее, если хотите!", chat_id=update.message.chat_id)
        keyboard = [
            [
                InlineKeyboardButton("Выйти к списку команд", callback_data="Выйти к списку команд")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Что дальше?", reply_markup=reply_markup)
        return 'what_to_do'
    for i in range(len(res)):
        answer = res[i][2]
        solution = res[i][3]
        task = res[i][1]
        if type(task) != str:
            await context.bot.send_photo(photo=task, chat_id=update.message.chat_id)
            task = 'Изображение выше'
        if type(answer) != str:
            await context.bot.send_photo(photo=answer, chat_id=update.message.chat_id)
            answer = 'Изображение выше'
        if type(solution) != str:
            await context.bot.send_photo(photo=solution, chat_id=update.message.chat_id)
            solution = 'Изображение выше'
        ans = str(i + 1) + '. ' + task + '\n Ответ: ' + answer + '\n Решение: ' + solution + '\n'
        await context.bot.send_message(
            text=f"{ans}",
            chat_id=update.message.chat_id)
    keyboard = [
        [
            InlineKeyboardButton("Выйти к списку команд", callback_data="Выйти к списку команд")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Что дальше?", reply_markup=reply_markup)
    return 'what_to_do'


async def what_to_do(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Union[int, str]:
    query = update.callback_query
    if query.data == "Выйти к списку команд":
        await bot_help(update, context)
        return ConversationHandler.END