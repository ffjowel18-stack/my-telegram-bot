import os
import json
import random
import aiohttp

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# =========================
# ENV
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing!")
if not API_KEY:
    raise ValueError("API_KEY missing!")

ADMIN_ID = 7428574557

START_LINKS = [
    "https://sepaste.com/eardbbd1",
    "https://sepaste.com/eardbvdbd2",
    "https://sepaste.com/dhdhhd3",
    "https://sepaste.com/dhdhhdhe4",
    "https://sepaste.com/dhdhhdhe4dvv"
]

DATA_FILE = "data.json"

# =========================
# DATA SYSTEM
# =========================
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = str(update.message.from_user.id)
    data = load_data()

    if user_id not in data:
        data[user_id] = {"balance": 0}
        save_data(data)

    link = random.choice(START_LINKS)

    await update.message.reply_text(
        f"💰 ইনকাম করতে নিচের লিংকে চাপ দাও 👇\n{link}"
    )

# =========================
# BALANCE
# =========================
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = str(update.message.from_user.id)
    data = load_data()

    bal = data.get(user_id, {}).get("balance", 0)

    await update.message.reply_text(f"💰 তোমার ব্যালেন্স: {bal} টাকা")

# =========================
# SHORT LINK
# =========================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    url = update.message.text

    if not url or not url.startswith("http"):
        await update.message.reply_text("❌ সঠিক লিংক দাও")
        return

    try:
        api_url = f"https://shrinkearn.com/api?api={API_KEY}&url={url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=10) as resp:
                result = await resp.json()

        # multiple fallback keys
        short_link = (
            result.get("shortenedUrl")
            or result.get("shortened_url")
            or result.get("short")
        )

        if short_link:
            await update.message.reply_text(f"✅ Short Link:\n{short_link}")
        else:
            await update.message.reply_text("❌ Link convert হয় নাই")

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("⚠️ Error হইছে")

# =========================
# RUN
# =========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
