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

#SHOWING ALL THE TASKS 
async def showtasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Identify the user
    user_task_list = user_tasks.get(user_id, [])  # Retrieve the user's tasks

    if not user_task_list:
        await update.message.reply_text("You have no tasks at the moment! Nabei take a break lah siao mugger.")
        return

    # Sort tasks by due date
    sorted_tasks = sorted(user_task_list, key=lambda x: x['due_date'])
    task_list = "\n".join(
        f"{i+1}. {task['task_name']} - Due: {task['due_date'].strftime('%Y-%m-%d %H:%M')}"
        for i, task in enumerate(sorted_tasks)
    )
    await update.message.reply_text(f"Haha why you haven't finish, here are your tasks by due date:\n{task_list}")


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
    app.add_handler(CommandHandler('showtasks', showtasks_command))

    # Polling
    print('Polling bot...')
    app.run_polling(poll_interval=3)
