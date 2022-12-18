from typing import Union
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ConversationHandler, ContextTypes
import sqlite3 as sql
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ConversationHandler, ContextTypes
from .help import bot_help


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            d = dict()
            for i in range(len(res)):
                task = res[i][1]
                if type(task) != str:
                    await context.bot.send_photo(photo=task, chat_id=update.message.chat_id)
                    task = 'Изображение выше'
                ans += str(i + 1) + '. ' + task + '\n'
                d[str(i + 1)] = res[i][0]
            await context.bot.send_message(
                text=f"{ans}",
                chat_id=update.message.chat_id)
            context.user_data["tasks"] = d
            return 'is_access'
        else:
            await context.bot.send_message(
                text=f"У вас нет доступа к этой группе, поэтому редактировать вы ее не можете :(",
                chat_id=update.message.chat_id)
            return ConversationHandler.END


async def is_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_tasks = context.user_data["tasks"]
    num_task = update.message.text
    if num_task not in all_tasks.keys():
        await context.bot.send_message(text="Вы ввели неверный номер удаляемого задания, воспользуйтесь командой еще раз.", chat_id=update.message.chat_id)
        return ConversationHandler.END
    conn = sql.connect('database/study_bot.db')
    query_db = conn.cursor()
    query_db.execute(f"""DELETE FROM All_Tasks WHERE ID = "{all_tasks[num_task]}";""")
    conn.commit()
    conn.close()
    await context.bot.send_message(text="Задача была успешно удалена!", chat_id=update.message.chat_id)
    return ConversationHandler.END