# # Command to view all homework and deadlines
# def view_homework(update: Update, context: CallbackContext) -> None:
#     if not homework_data:
#         update.message.reply_text("You have no homework added.")
#         return

#     homework_list = "\n".join(
#         [f"{homework_name}: {homework_time.strftime('%Y-%m-%d %H:%M')}" for homework_name, homework_time in homework_data.items()]
#     )
#     update.message.reply_text(f"Your Homework:\n{homework_list}")

# # Register the handler for /view_homework
# dp.add_handler(CommandHandler("view_homework", view_homework))
