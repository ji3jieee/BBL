from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime

TOKEN: Final = '7870019893:AAG4LYwPcWWdPystb2Ic5vHtyuej9kqtW_Y'
BOT_USERNAME: Final = '@SiaoMuggerBot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! What mugging tasks do you have today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Use this command to do whatever')

TASK_NAME, TASK_DUE_DATE = range(2)
# Dictionary to store tasks for each user (optional)
user_tasks = {}

async def addtask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please input the name of your task.')
    return TASK_NAME

async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_name = update.message.text  # Get the task name
    context.user_data['task_name'] = task_name  # Store task name in user data
    await update.message.reply_text(f"Okay, got it! Please input the due date of '{task_name}' in the format YYYY-MM-DD HH:MM!")
    return TASK_DUE_DATE

async def task_due_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    due_date_input = update.message.text
    task_name = context.user_data.get('task_name')  # Retrieve task name from user data
    
    try:
        # Parse the date and time input
        due_date = datetime.strptime(due_date_input, '%Y-%m-%d %H:%M')
        # Store the task (optional)
        user_id = update.message.from_user.id
        user_tasks.setdefault(user_id, []).append({'task_name': task_name, 'due_date': due_date})
        
        # Confirm task creation
        await update.message.reply_text(f"Task '{task_name}' with due date '{due_date}' has been added! 🎉")
        return ConversationHandler.END
    except ValueError:
        # Handle invalid input
        await update.message.reply_text(
            "Invalid date format! Please use 'YYYY-MM-DD HH:MM' (e.g., '2025-01-20 14:30')."
        )
        return TASK_DUE_DATE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation."""
    await update.message.reply_text("Okay, I've canceled the current task setup. Let me know if you need anything else!")
    return ConversationHandler.END

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('addtask', addtask_command))

    # Define the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('addtask', addtask_command)],
        states={
            TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],
            TASK_DUE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_due_date)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],  # Optional cancel handler
    )

    # Add conversation handler to the application
    app.add_handler(conversation_handler)

    # Polling
    print('Polling bot...')
    app.run_polling(poll_interval=3)


# if __name__ == '__main__':
#     print('starting bot')
#     app = Application.builder().token(TOKEN).build()

#     #commands
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('help', help_command))
#     app.add_handler(CommandHandler('addtask', addtask_command))  

#     #messages
#     # app.add_handler(MessageHandler(filters.TEXT, handle_message))

#     #errors
#     # app.add_error_handler(error)

#     #polls the bot
#     print('polling bot...')
#     app.run_polling(poll_interval=3)




##Adding homework handling

# HOMEWORK_NAME, DATE_TIME, REMINDER_COUNT, REMINDER_TIME = range(4)
# homework_tasks = {}
# async def add_homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Please enter the name of your task.")
#     return HOMEWORK_NAME

# async def homework_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data['homework_name'] = update.message.text
#     await update.message.reply_text(f"Got it! Homework name: {update.message.text}. Now, please enter the submission date and time (e.g., 2025-01-20 15:00).")
#     return DATE_TIME

# async def homework_date_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         context.user_data['submission_time'] = datetime.datetime.strptime(update.message.text, "%Y-%m-%d %H:%M")
#         await update.message.reply_text(f"Got it! Submission time: {context.user_data['submission_time']}. How many reminders would you like to set?")
#         return REMINDER_COUNT
#     except ValueError:
#         await update.message.reply_text("Invalid format. Please enter the date and time in the format YYYY-MM-DD HH:MM.")
#         return DATE_TIME

# async def reminder_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         context.user_data['reminder_count'] = int(update.message.text)
#         await update.message.reply_text(f"Got it! You want {context.user_data['reminder_count']} reminders. How many days/hours before submission do you want the first reminder?")
#         return REMINDER_TIME
#     except ValueError:
#         await update.message.reply_text("Please enter a valid number for the reminders.")
#         return REMINDER_COUNT

# async def reminder_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         reminder_time = int(update.message.text)
#         context.user_data['reminder_time'] = reminder_time
#         homework_name = context.user_data['homework_name']
#         submission_time = context.user_data['submission_time']
#         reminder_count = context.user_data['reminder_count']
#         reminder_time = context.user_data['reminder_time']

#         # Save the task in homework_tasks (can be used to schedule future reminders)
#         homework_tasks[homework_name] = {
#             'submission_time': submission_time,
#             'reminder_count': reminder_count,
#             'reminder_time': reminder_time
#         }

#         await update.message.reply_text(f"Homework task '{homework_name}' added successfully!\n"
#                                        f"Submission time: {submission_time}\n"
#                                        f"Reminders: {reminder_count} reminder(s) at {reminder_time} hours/days before submission.")
#         return ConversationHandler.END
#     except ValueError:
#         await update.message.reply_text("Please enter a valid number for the reminder time.")
#         return REMINDER_TIME

# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('The task has been cancelled.')
#     return ConversationHandler.END

# async def add_homework_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Let\'s add a homework task!')
#     return await add_homework(update, context)

# conversation_handler = ConversationHandler(
#     entry_points=[CommandHandler('add_homework', add_homework_command)],
#     states={
#         HOMEWORK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, homework_name)],
#         DATE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, homework_date_time)],
#         REMINDER_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, reminder_count)],
#         REMINDER_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reminder_time)],
#     },
#     fallbacks=[CommandHandler('cancel', cancel)],
# )





if __name__ == '__main__':
    print('starting bot')
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    #app.add_handler(CommandHandler('add', add_homework))
    app.add_handler(CommandHandler('addhomework', add_homework_command))  
    # app.add_handler(CommandHandler('task name', homework_name))
    # app.add_handler(CommandHandler('due date', homework_date_time))
    # app.add_handler(CommandHandler('help', reminder_count))
    # app.add_handler(CommandHandler('custom', custom_command))

    #messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    # app.add_error_handler(error)

    #polls the bot
    print('polling bot...')
    app.run_polling(poll_interval=3)
