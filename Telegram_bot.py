import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


# OpenAI API kalitini o'rnating
openai.api_key = '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'

# Telegram API tokenini o'rnating
TELEGRAM_API_TOKEN = '8102841815:AAEWQ-fDSvn4O1ilGhIfqxzd8QSztzjCQyc'

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

def main():
    # Applicationni yaratish
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Komandalar va xabarlarni qayta ishlash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
