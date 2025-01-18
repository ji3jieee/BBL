# from telegram import ParseMode
# from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue
# from datetime import datetime, timedelta

# # Function to send reminder
# def send_reminder(context: CallbackContext) -> None:
#     job = context.job
#     update = job.context
#     homework_name = job.context["homework_name"]
#     update.message.reply_text(f"Reminder: The homework '{homework_name}' is due soon!")

# # Schedule reminder function
# def schedule_reminder(update: Update, context: CallbackContext) -> None:
#     if len(context.args) != 2:
#         update.message.reply_text("Usage: /set_reminder <homework_name> <days_before_due>")
#         return
    
#     homework_name = context.args[0]
#     days_before_due = int(context.args[1])

#     if homework_name not in homework_data:
#         update.message.reply_text(f"Homework '{homework_name}' not found.")
#         return
    
#     homework_time = homework_data[homework_name]
#     reminder_time = homework_time - timedelta(days=days_before_due)
    
#     context.job_queue.run_once(send_reminder, reminder_time, context={"homework_name": homework_name, "update": update})

#     update.message.reply_text(f"Reminder set for {homework_name} {days_before_due} days before the due date.")

# # Register the handler for /set_reminder
# dp.add_handler(CommandHandler("set_reminder", schedule_reminder))
