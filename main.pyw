from config import TOKEN
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler
from bots_commands import *

app = ApplicationBuilder().token(TOKEN).build()
filter_text = ['+', '-', '+1', '-1']

app.add_handler(CommandHandler("help", help_command))  # помощь
app.add_handler(CommandHandler("stat", stat_command))  # показать статистику(редко пользуются)
app.add_handler(MessageHandler(filters.Text(filter_text), callback=run))  # работа со списком
app.add_handler(CommandHandler("del", del_command))  # очистить список
app.add_handler(CommandHandler("add", add_goals))  # добавить голы в статистику
app.add_handler(CommandHandler("chg_name", change_name))  # поменять имя в списке
app.add_handler(CommandHandler("chg_limit_pl", change_limit_player))  # поменять лимит игроков списка

app.add_handler(CallbackQueryHandler(button))  # кнопки
# app.add_handler(MessageHandler(filters.TEXT, callback=log)) # логирование

# app.job_queue.run_repeating(tela_tela, interval=6000, first=18000) # теле тела тела

print('start')
app.run_polling(stop_signals=None)
