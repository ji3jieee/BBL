from typing import Final, List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime
import asyncio

TOKEN: Final = '7870019893:AAG4LYwPcWWdPystb2Ic5vHtyuej9kqtW_Y'
BOT_USERNAME: Final = '@SiaoMuggerBot'

##COMMANDS 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Eh mugger! What you grinding for today?🤔')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"😐Hello this kind of basic stuff also don't know?!😐\n\n"
    message += f"📃 /addtask to add tasks to your list\n"
    message += f"💢 /removetask to remove tasks from your list when you are done (don't slack hor) \n"
    message += f"🚫 /cancel if you need to cancel your task when adding halfway\n"
    message += f"📝 /showtasks to show all the tasks you have right now"
    await update.message.reply_text(message)

TASK_NAME, TASK_DUE_DATE, REMOVE_NAME = range(3)
# Dictionary to store tasks for each user (optional)
user_tasks = {}

async def addtask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"What's your task called?")
    return TASK_NAME

##FOLLOW UP FUNCTIONS
async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_name = update.message.text  # Get the task name
    context.user_data['task_name'] = task_name  # Store task name in user data
    await update.message.reply_text(f"Okay onz. Please input the due date of '{task_name}' in the format YYYY-MM-DD HH:MM!")
    return TASK_DUE_DATE

async def task_due_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    due_date_input = update.message.text
    task_name = context.user_data.get('task_name')  # Retrieve task name from user data
    
    try:
        # Parse the date and time input
        due_date = datetime.strptime(due_date_input, '%Y-%m-%d %H:%M')
        current_time = datetime.now()

        # Check if the due date is in the future
        if due_date <= current_time:
            await update.message.reply_text(
                "You add a task due *in the past* for what siol? The due date and time must be *in the future*! Please input a valid due date in the format 'YYYY-MM-DD HH:MM'.",
                parse_mode="Markdown"
            )
            return TASK_DUE_DATE
        
        # Store the task (optional)
        user_id = update.message.from_user.id
        user_tasks.setdefault(user_id, []).append({'task_name': task_name, 'due_date': due_date})

        # Confirm task creation
        await update.message.reply_text(f"Task '{task_name}' with due date '{due_date}' has been added! 🎉")
        
        # Schedule the reminder
        await schedule_reminder(update, user_id, task_name, due_date)
        
        return ConversationHandler.END
    except ValueError:
        # Handle invalid input
        await update.message.reply_text(
            "Wrong format la! Please use 'YYYY-MM-DD HH:MM' (e.g., '2025-01-20 14:30')."
        )
        return TASK_DUE_DATE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation."""
    await update.message.reply_text("Okay, I've canceled the current task setup. Take a break, king/queen!")
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

# Step 1: Handle /removetask command
async def removetasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_task_list = user_tasks.get(user_id, [])

    # Step 2: Check if there are tasks to remove
    if not user_task_list:
        await update.message.reply_text("You don't have any tasks to remove lol! Use /addtask to add one first.")
        return ConversationHandler.END

    # Step 3: List all tasks
    task_list_message = "Eh you better not be slacking! Here's your list of tasks:\n\n"
    for task in user_task_list:
        task_list_message += f"- {task['task_name']} (Due: {task['due_date']})\n"
    task_list_message += "\nWhich task do you want to remove? Please reply with the task name."

    await update.message.reply_text(task_list_message)
    return REMOVE_NAME

# Step 4: Handle task removal input
async def remove_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_task_list = user_tasks.get(user_id, [])
    task_name_to_remove = update.message.text.strip()  # Clean user input

    # Search for the task in the list
    task_to_remove = next((task for task in user_task_list if task['task_name'].lower() == task_name_to_remove.lower()), None)

    if task_to_remove:
        # Remove the task
        user_task_list.remove(task_to_remove)
        await update.message.reply_text(f"Okay, removed the task: '{task_to_remove['task_name']}'! ✅")

        # If no tasks left, clear user entry
        if not user_task_list:
            user_tasks.pop(user_id)

        return ConversationHandler.END
    else:
        # If task not found
        await update.message.reply_text("I couldn't find a task with that name! Please reply with an exact task name.")
        return REMOVE_NAME


async def schedule_reminder(update: Update, user_id: int, task_name: str, due_date: datetime):
    """Schedules the reminders for the given task."""
    now = datetime.now()
    time_to_due = (due_date - now).total_seconds()

    # Calculate wait times for 12 hours before and exactly at the due time
    twelve_hours_before = max(time_to_due - 43200, 0)  # 12 hours before
    due_time = max(time_to_due, 0)  # At the due time

    # Schedule the reminders
    if twelve_hours_before > 0:
        asyncio.create_task(send_reminder(update, task_name, twelve_hours_before, "12 hours"))
    if due_time > 0:
        asyncio.create_task(send_reminder(update, task_name, due_time, "now"))

async def send_reminder(update: Update, task_name: str, time_to_wait: float, reminder_type: str):
    """Waits for the specified time and sends the reminder."""
    await asyncio.sleep(time_to_wait)
    try:
        if reminder_type == "now":
            await update.message.reply_text(f"Reminder: Your task '{task_name}' is due now! Submit liao fasterfaster! ⏰")
        else:
            await update.message.reply_text(f"Reminder: Your task '{task_name}' is due in {reminder_type}! Faster start doing already! ⏰")
    except Exception as e:
        print(f"Error sending reminder: {e}")

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    
    # app.add_handler(CommandHandler('addtask', addtask_command))

    # Define the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('addtask', addtask_command), CommandHandler('removetask', removetasks_command)],  # Entry points for both add and remove tasks
        states={
            TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],
            TASK_DUE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_due_date)],
            REMOVE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_name)],  # Handling task removal
        },
        fallbacks=[CommandHandler('cancel', cancel)],  # Optional cancel handler
    )

    # Add conversation handler to the application
    app.add_handler(conversation_handler)
    app.add_handler(CommandHandler('showtasks', showtasks_command))

    # Polling
    print('Polling bot...')
    app.run_polling(poll_interval=3)
