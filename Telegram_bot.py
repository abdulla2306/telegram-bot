import os
import openai
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging

# OpenAI API kaliti va Telegram API tokenini to'g'ridan-to'g'ri kiritish
openai.api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Flask ilovasi
app = Flask(__name__)

# Flask endpoint'lari
@app.route('/')
def home():
    return "Salom! Flask serveri ishlamoqda."

# OpenAI modelidan foydalanish
def generate_openai_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # yoki boshqa modelni tanlang
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# Telegram botda foydalanuvchidan kelgan xabarni qayta ishlash
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Foydalanuvchidan kelgan xabar
    print(f"Foydalanuvchidan xabar: {user_message}")
    
    # OpenAI'dan javob olish
    openai_response = generate_openai_response(user_message)
    
    # OpenAI javobini foydalanuvchuga yuborish
    await update.message.reply_text(openai_response)

# /start komandasi
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Salom! Men OpenAI yordamida ishlovchi botman. Savollarni berishingiz mumkin.")

# Webhookni sozlash
def set_webhook():
    WEBHOOK_URL = f'https://telegram-bot-ef1y.onrender.com/{TELEGRAM_API_TOKEN}'
    set_webhook_url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url={WEBHOOK_URL}'
    response = requests.get(set_webhook_url)
    print(f"Webhook sozlash javobi: {response.text}")  # So'rovning natijasi

# Webhookni o'rnatish
set_webhook()

# Webhook URLni sozlash
@app.route(f'/{TELEGRAM_API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, None)
    application.process_update(update)
    return 'OK', 200

def main():
    # Applicationni yaratish
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Komandalar va xabarlarni qayta ishlash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhookni sozlash
    PORT = int(os.getenv('PORT', '5000'))  # Render platformasida portni 5000 deb belgilash mumkin
    application.run_webhook(
        listen="0.0.0.0",  # Butun tizim bo'ylab tinglash
        port=PORT,  # Portni o'zgaruvchidan olish
        url_path=TELEGRAM_API_TOKEN,  # Tokenni url_path sifatida ishlatish
        webhook_url=f'https://telegram-bot-ef1y.onrender.com/{TELEGRAM_API_TOKEN}'  # Render URL
    )

if __name__ == '__main__':
    # Flask serverini ishga tushurish
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
    main()
