from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

TOKEN = "8735885260:AAGcke4yXK9FV1jqqYiTStxwDpDy2b_1Fnw"
API_KEY = "7040060dda99619908324b34bafcff9f72bde4b4"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "http" in url:
        api = f"https://zshrink.com/api?api={API_KEY}&url={url}"
        res = requests.get(api).text
        await update.message.reply_text(f"🔗 Short link:\n{res}")
    else:
        await update.message.reply_text("❌ Send a valid link")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("Bot running...")
app.run_polling()
