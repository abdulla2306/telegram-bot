import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from flask import Flask, request

# OpenAI API kaliti va Telegram API tokenini to'g'ridan-to'g'ri kiritish
openai.api_key = os.getenv('OPENAI_API_KEY')  # xavfsiz saqlash uchun o'zgaruvchi orqali
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')  # Telegram tokenini o'zgaruvchi orqali

# Flask dasturini yaratish
app = Flask(__name__)

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

# Foydalanuvchidan kelgan xabarni qayta ishlash
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

@app.route(f'/{TELEGRAM_API_TOKEN}', methods=['POST'])
def webhook():
    # Telegramdan kelgan xabarni olish
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, None)

    # Telegram handlerlarni ishga tushirish
    application.process_update(update)
    
    return 'ok', 200

def main():
    # Applicationni yaratish
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Komandalar va xabarlarni qayta ishlash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Flask serverni ishga tushurish
    PORT = int(os.getenv('PORT', '5000'))  # Render platformasida portni 5000 deb belgilash mumkin
    app.run(host="0.0.0.0", port=PORT)

if __name__ == '__main__':
    main()



