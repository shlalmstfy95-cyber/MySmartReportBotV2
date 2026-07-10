from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
import requests


TOKEN = os.getenv("TELEGRAM_TOKEN") # Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بك في Smart ReportBot\n\n"
        "أرسل أي موضوع وسأكتب لك تقريرًا احترافيًا."
    )


def generate_report(topic):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": f"اكتب تقريرًا احترافيًا باللغة العربية عن {topic} مع مقدمة وعناوين وخاتمة."
            }
        ],
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري إنشاء التقرير...")

    try:
        report = generate_report(update.message.text)
        await update.message.reply_text(report)

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ:\n{e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
