from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from games import harry_vs_tom

TOKEN = "7791922869:AAH4w6Zx-MCmVFc3OBDjEd6wJLomXrA6qJk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(harry_vs_tom.start_text(update, context))

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
harry_vs_tom.register(app)

app.run_polling()
