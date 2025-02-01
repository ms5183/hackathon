import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


BOT_TOKEN = "BOT_TOKEN"
API = "API"
URL = "URL"
headers = {
    "Content-Type": "application/json",
    "Apikey": f"Api-key {API}"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="<b>Hello, I am the bot designed to help special people.</b>\n\nAsk me a question, I may help you.",
        parse_mode="HTML"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        payload = {"payload": user_input}
        response = requests.post(URL, headers=headers, json=payload)

        if response.ok:
            api_response = response.json()
            clean_text = api_response.get("text", "")
        else:
            clean_text = f"Error {response.status_code}: {response.text}"
    except Exception as e:
        clean_text = f"Server fetching error: {str(e)}"

    await update.message.reply_text(clean_text)


if __name__ == "__main__":
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot ready. Waiting for messages...")
    app_bot.run_polling()
