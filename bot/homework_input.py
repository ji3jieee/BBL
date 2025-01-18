# from typing import Final
# # from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram.ext import (
#     Updater,
#     CommandHandler,
#     MessageHandler,
#     ConversationHandler,
#     CallbackContext,
# )

# # Bot Token from BotFather
# TOKEN = "7870019893:AAG4LYwPcWWdPystb2Ic5vHtyuej9kqtW_Y"
# BOT_USERNAME: Final = '@SiaoMuggerBot'

# # Define conversation states
# HOMEWORK_NAME, SUBMISSION_DATE, REMINDER_COUNT, REMINDER_TIMING = range(4)

# # Start command handler
# def start(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(
#         "Welcome to the Homework Reminder Bot! 🎓\n\n"
#         "I can help you keep track of your homework deadlines and send timely reminders.\n"
#         "Use /addhomework to set up a reminder or /help for more options."
#     )

# # Help command handler
# def help_command(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(
#         "Here are the commands you can use:\n"
#         "/start - Start interacting with the bot\n"
#         "/addhomework - Add a new homework and set reminders\n"
#         "/help - Display this help message\n"
#         "/cancel - Cancel the current operation"
#     )

# # Add homework handler
# def add_homework(update: Update, context: CallbackContext) -> int:
#     update.message.reply_text(
#         "Please enter the name of your homework:",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     return HOMEWORK_NAME

# # Handle homework name input
# def homework_name(update: Update, context: CallbackContext) -> int:
#     context.user_data["homework_name"] = update.message.text
#     update.message.reply_text("Great! When is it due? (e.g., YYYY-MM-DD HH:MM)")
#     return SUBMISSION_DATE

# # Handle submission date input
# def submission_date(update: Update, context: CallbackContext) -> int:
#     context.user_data["submission_date"] = update.message.text
#     update.message.reply_text("How many reminders would you like to receive?")
#     return REMINDER_COUNT

# # Handle reminder count input
# def reminder_count(update: Update, context: CallbackContext) -> int:
#     context.user_data["reminder_count"] = int(update.message.text)
#     update.message.reply_text(
#         "How many days or hours before the deadline should I send each reminder?\n"
#         "(e.g., '2 days' or '3 hours')"
#     )
#     return REMINDER_TIMING

# # Handle reminder timing input and finish
# def reminder_timing(update: Update, context: CallbackContext) -> int:
#     context.user_data["reminder_timing"] = update.message.text
#     update.message.reply_text(
#         f"Got it! Here's a summary of your homework reminder:\n"
#         f"📚 Homework: {context.user_data['homework_name']}\n"
#         f"📅 Due: {context.user_data['submission_date']}\n"
#         f"🔔 {context.user_data['reminder_count']} reminders at "
#         f"{context.user_data['reminder_timing']} before the deadline.\n\n"
#         "You will be notified at the specified times. Use /addhomework to add more reminders!"
#     )
#     return ConversationHandler.END

# # Cancel command handler
# def cancel(update: Update, context: CallbackContext) -> int:
#     update.message.reply_text(
#         "Operation canceled. You can start over with /addhomework.",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     return ConversationHandler.END

# # Main function to set up command handlers
# def main():
#     # Replace 'YOUR_TOKEN' with the bot token from config.py
#     from bot.config import TOKEN
#     updater = Updater(TOKEN)

#     # Define conversation handler for adding homework
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("addhomework", add_homework)],
#         states={
#             HOMEWORK_NAME: [MessageHandler(Filters.text & ~Filters.command, homework_name)],
#             SUBMISSION_DATE: [MessageHandler(Filters.text & ~Filters.command, submission_date)],
#             REMINDER_COUNT: [MessageHandler(Filters.text & ~Filters.command, reminder_count)],
#             REMINDER_TIMING: [MessageHandler(Filters.text & ~Filters.command, reminder_timing)],
#         },
#         fallbacks=[CommandHandler("cancel", cancel)],
#     )

#     # Register handlers
#     updater.dispatcher.add_handler(CommandHandler("start", start))
#     updater.dispatcher.add_handler(CommandHandler("help", help_command))
#     updater.dispatcher.add_handler(conv_handler)
#     updater.dispatcher.add_handler(CommandHandler("cancel", cancel))

#     # Start the bot
#     updater.start_polling()
#     updater.idle()


# if __name__ == "__main__":
#     main()
