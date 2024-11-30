import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# OpenAI API kalitini o'rnating
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Telegram API tokenini o'rnating
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

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

def main():
    # Updaterni yaratish
    updater = Updater(TELEGRAM_API_TOKEN)

    # Dispatcher obyekti
    dispatcher = updater.dispatcher

    # Komandalar va xabarlarni qayta ishlash
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
