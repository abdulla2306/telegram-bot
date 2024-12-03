import os
import openai
import requests
import json
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
from dotenv import load_dotenv  # dotenv kutubxonasini import qilamiz

# .env faylini yuklash
load_dotenv()

# OpenAI API kaliti va Telegram API tokenini o'zgaruvchilardan olish
openai.api_key = os.getenv('OPENAI_API_KEY')  # .env faylidan yoki tizimdan o'qiladi
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')  # .env faylidan yoki tizimdan o'qiladi
PORT = os.getenv('PORT', 10000)  # default qiymat 10000
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Webhook URL .env faylidan o'qiladi

# Flask ilovasi
app = Flask(__name__)

# Telegram botni sozlash
application = None  # Global variable to hold the application object

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
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Foydalanuvchidan kelgan xabar
    print(f"Foydalanuvchidan xabar: {user_message}")
    
    # OpenAI'dan javob olish
    openai_response = generate_openai_response(user_message)
    
    # OpenAI javobini foydalanuvchuga yuborish
    update.message.reply_text(openai_response)

# /start komandasi
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Salom! Men OpenAI yordamida ishlovchi botman. Savollarni berishingiz mumkin.")

# Webhookni sozlash
def set_webhook():
    # Telegram bot tokeni va webhook URL'si
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
    WEBHOOK_URL = f'https://{os.getenv("WEBHOOK_URL")}/{TELEGRAM_BOT_TOKEN}'
    
    # Webhookni sozlash URL'si
    set_webhook_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}'
    response = requests.get(set_webhook_url)
    print(f"Webhook sozlash javobi: {response.text}")  # So'rovning natijasi

# Webhook URLni sozlash
@app.route(f'/{TELEGRAM_API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')  # Webhookdan kelgan JSON ma'lumotlari
    update = Update.de_json(json.loads(json_str), None)  # JSONni Python obyektiga aylantirish
    if application:
        application.process_update(update)  # Application ni ishlatish
    return 'OK', 200

def main():
    global application  # Global qilish
    # Applicationni yaratish
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Komandalar va xabarlarni qayta ishlash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhookni o'rnatish
    set_webhook()

if __name__ == '__main__':
    # Flask serverini ishga tushurish va Telegram botni sozlash
    main()

    # Flask serverini ishga tushirish
    app.run(host="0.0.0.0", port=int(PORT))  # Portni .env faylidan olish



