from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Salom! Men Telegram botiman.')

# /help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Yordam kerakmi? /start deb yozing yoki boshqa buyruqlarni sinab ko\'ring.')

def main():
    # Tokenni botFather'dan olgan token bilan almashtiring
    token = '8102841815:AAEWQ-fDSvn4O1ilGhIfqxzd8QSztzjCQyc'

    # Application ob'ektini yaratamiz
    application = Application.builder().token(token).build()

    # /start komandasini qo'shamiz
    application.add_handler(CommandHandler("start", start))

    # /help komandasini qo'shamiz
    application.add_handler(CommandHandler("help", help_command))

    # Botni ishga tushiramiz
    application.run_polling()

if name == 'main':
    main()