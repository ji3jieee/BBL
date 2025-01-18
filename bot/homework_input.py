from datetime import datetime
from telegram.ext import CommandHandler

# Dictionary to store homework
homework_data = {}

# Command to add homework
def add_homework(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 2:
        update.message.reply_text("Usage: /add_homework <homework_name> <YYYY-MM-DD HH:MM>")
        return
    
    homework_name = context.args[0]
    homework_datetime = context.args[1]
    
    try:
        # Convert input date to datetime object
        homework_time = datetime.strptime(homework_datetime, "%Y-%m-%d %H:%M")
        homework_data[homework_name] = homework_time
        update.message.reply_text(f"Homework '{homework_name}' added with due date {homework_time.strftime('%Y-%m-%d %H:%M')}.")
    except ValueError:
        update.message.reply_text("Invalid date format! Use YYYY-MM-DD HH:MM.")

# Register the handler for /add_homework
dp.add_handler(CommandHandler("add_homework", add_homework))
