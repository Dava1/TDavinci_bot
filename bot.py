import os
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from games import harry_vs_tom


def load_env(path: Path = Path(__file__).with_name(".env")) -> None:
    """Load KEY=value lines from .env into os.environ (real env vars win)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("BOT_TOKEN is not set. Put BOT_TOKEN=<your token> in .env (see .env.example).")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(harry_vs_tom.start_text(update, context))

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
harry_vs_tom.register(app)

app.run_polling()
