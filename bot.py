import os
import json
import time
import random
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8735885260:AAE90mvgQ2C2GRVAsAz-eq5tT-U8GSKS5xM")
API_KEY = os.getenv("7040060dda99619908324b34bafcff9f72bde4b4")

ADMIN_ID = "7428574557"

START_LINKS = [
    "https://sepaste.com/eardbbd1",
    "https://sepaste.com/eardbvdbd2",
    "https://sepaste.com/dhdhhd3",
    "https://sepaste.com/dhdhhdhe4",
    "https://sepaste.com/dhdhhdhe4dvv",
    "https://sepaste.com/Dbdbxvgddvdv",
    "https://sepaste.com/Dbdbxvgddvdvbfb",
    "https://sepaste.com/Dbdbxvgd",
    "https://sepaste.com/Dbdbxvgddvdvbfbdggd",
    "https://sepaste.com/Dbdbxvgddvdvbfb",
    "https://sepaste.com/Dbdbxvgddv78",
    "https://sepaste.com/Dbdbxvgddv7",
    "https://sepaste.com/Dbdbxvgddv78cdhsed"
]

DATA_FILE = "data.json"

# =====================
# DATA SYSTEM
# =====================
def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# =====================
# START
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    data = load_data()

    if user_id not in data:
        data[user_id] = {"balance": 0}

    save_data(data)

    link = random.choice(START_LINKS)

    await update.message.reply_text(
        f"💰 ইনকাম করতে নিচের লিংকে চাপ দাও 👇\n\n{link}"
    )

# =====================
# BALANCE
# =====================
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    data = load_data()

    bal = data.get(user_id, {}).get("balance", 0)
    await update.message.reply_text(f"💰 Balance: ${bal}")

# =====================
# SHORT LINK (ASYNC SAFE)
# =====================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if not url.startswith("http"):
        await update.message.reply_text("❌ Valid link দাও")
        return

    try:
        api_url = f"https://shrinkearn.com/api?api={API_KEY}&url={url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()

        short_link = data.get("shortenedUrl")

        if short_link:
            await update.message.reply_text(f"🔗 {short_link}")
        else:
            await update.message.reply_text("❌ Error")
    except:
        await update.message.reply_text("⚠️ Server busy, আবার চেষ্টা করো")

# =====================
# RUN
# =====================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
