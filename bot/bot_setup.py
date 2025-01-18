from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Bot Token from BotFather
TOKEN = "YOUR_BOT_TOKEN"

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the Homework Reminder Bot! 🎓\n"
        "Use /add_homework <homework_name> <YYYY-MM-DD HH:MM> to add your homework."
    )

# Command to display help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "This bot helps you keep track of your homework submissions!\n"
        "Use /add_homework <homework_name> <YYYY-MM-DD HH:MM> to add your homework.\n"
        "Use /view_homework to view your upcoming homework and deadlines."
    )

def main() -> None:
    # Create Updater and Dispatcher
    updater = Updater(TOKEN)

    # Get dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
