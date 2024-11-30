from dotenv import load_dotenv
import openai
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# .env faylini yuklash
load_dotenv()

# API kalitlarini atrof-muhitdan olish
openai.api_key = os.getenv("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")
TELEGRAM_API_TOKEN = os.getenv("8102841815:AAEWQ-fDSvn4O1ilGhIfqxzd8QSztzjCQyc")

# OpenAI modelidan foydalanish (async)
async def generate_openai_response(prompt: str) -> str:
    try:
        response = await openai.Completion.create(
            engine="text-davinci-003",  # yoki boshqa modelni tanlang
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# Foydalanuvchidan kelgan xabarni qayta ishlash
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Foydalanuvchidan kelgan xabar
    print(f"Foydalanuvchidan xabar: {user_message}")
    
    # OpenAI'dan javob olish
    openai_response = await generate_openai_response(user_message)
    
    # OpenAI javobini foydalanuvchuga yuborish
    await update.message.reply_text(openai_response)

# /start komandasi
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Salom! Men OpenAI yordamida ishlovchi botman. Savollarni berishingiz mumkin.")

def main():
    # Applicationni yaratish
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Komandalar va xabarlarni qayta ishlash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    asyncio.run(application.run_polling())

if __name__ == '__main__':
    main()


