from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler



TOKEN: Final = '7422447247:AAEYU7q2QSFL7wk96lnIk8ilMMy-Mwry90g'
BOT_USERNAME: Final = '@WinLiaoBot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Siao eh, win liao lor. What bot you want use today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"Come come come take a look at our bots!\n\n"
    message += f"@SiaoMuggerBot: Come do your work mugger! Keep track of your tasks here.\n"
    message += f"@glugglugbot: Track your drinking water intake! Singapore so hot you not thirsty meh?!\n"
    message += f"@GotNewsLiaoBot: Time to get serious. Know your news today!\n"
    message += f"@BaeLiaoBot: Feeling single but don't wanna mingle? Chat with our charismatic bot now!"   
    await update.message.reply_text(message)  

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"Having fun or not? What bot do you want to see next? \n"
    message += f"https://forms.gle/94yo79JApiKVQDCw5"
    await update.message.reply_text(message)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('feedback', feedback_command))

    # Polling
    print('Polling bot...')
    app.run_polling(poll_interval=3)