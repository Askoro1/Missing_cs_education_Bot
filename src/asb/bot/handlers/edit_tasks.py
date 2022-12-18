from typing import Union
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ConversationHandler, ContextTypes
import sqlite3 as sql
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ConversationHandler, ContextTypes
from .help import bot_help


async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sql.connect('database/study_bot.db')
    query_db = conn.cursor()
    id = update.message.from_user.id
    message = update.message.text.split()
    if len(message) == 1:
        await context.bot.send_message(
            text=f"Недостаточно параметров для использования, пожалуйста, команду введите еще раз.",
            chat_id=update.message.chat_id)
        return ConversationHandler.END
    elif len(message) == 2:
        query_db.execute(
        f"""SELECT * FROM Groups WHERE GROUP_ID = "{message[1]}";""")
        res = query_db.fetchone()
        id = update.message.from_user.id
        if res is None:
            await context.bot.send_message(
                text=f"Такой группы не существует, пожалуйста, введите команду еще раз.",
                chat_id=update.message.chat_id)
            return ConversationHandler.END
        if res[1] == id:
            query_db.execute(
                f"""SELECT * FROM All_Tasks WHERE GROUP_ID = "{message[1]}";""")
            res = query_db.fetchall()
            ans = ''
            if res is None or len(res) == 0:
                await context.bot.send_message(
                    text=f"Эта группа уже пуста, тут нет задач, если хотите - добавьте их командой /add [название группы].",
                    chat_id=update.message.chat_id)
                return ConversationHandler.END
            list_tasks = dict()
            for i in range(len(res)):
                task = res[i][1]
                if type(task) != str:
                    await context.bot.send_photo(photo=task, chat_id=update.message.chat_id)
                    task = 'Изображение выше'
                ans += str(i + 1) + '. ' + task + '\n'
                list_tasks[str(i + 1)] = res[i][0]
            await context.bot.send_message(
                text=f"{ans}",
                chat_id=update.message.chat_id)
            context.user_data["tasks"] = list_tasks
            keyboard = [
                [
                    InlineKeyboardButton("Изменить условие", callback_data="Изменить условие"),
                    InlineKeyboardButton("Изменить решение", callback_data="Изменить решение"),
                    InlineKeyboardButton("Изменить ответ", callback_data="Изменить ответ"),
                    InlineKeyboardButton("Выйти из редактирования", callback_data="Выйти из редактирования")
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text("Что дальше?", reply_markup=reply_markup)
            return 'choose_tab'
        else:
            await context.bot.send_message(
                text=f"У вас нет доступа к этой группе, поэтому редактировать вы ее не можете :(",
                chat_id=update.message.chat_id)
            return ConversationHandler.END


async def check_keyboard_for_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "Изменить условие":
        return 'edit_condition'
    elif query.data == "Изменить решение":
        return 'edit_solution'
    elif query.data == "Изменить ответ":
        return 'edit_ans'
    elif query.data == "Выйти из редактирования":
        await context.bot.send_message(text="Вы вышли из режима редактирования задачи!", chat_id=query.message.chat_id)
        return ConversationHandler.END


async def edit_condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass