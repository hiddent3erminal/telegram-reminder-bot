import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import dateparser

# Load tasks from a user's JSON file
def load_tasks(user_id):
    try:
        with open(f'{user_id}_tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

# Save tasks to a user's JSON file
def save_tasks(user_id, tasks):
    with open(f'{user_id}_tasks.json', 'w') as file:
        json.dump(tasks, file)

# Add a task to the user's JSON file
def add_task(user_id, task_desc, due_date_str, priority="Medium"):
    tasks = load_tasks(user_id)
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "task": task_desc,
        "due_date": due_date_str,
        "priority": priority,
        "completed": False
    }
    tasks.append(task)
    save_tasks(user_id, tasks)

# Mark a task as completed
def mark_completed(user_id, task_id):
    tasks = load_tasks(user_id)
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    save_tasks(user_id, tasks)

# Delete a task
def delete_task(user_id, task_id):
    tasks = load_tasks(user_id)
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(user_id, tasks)

# Get a string representation of tasks
def format_tasks(tasks):
    if not tasks:
        return "No tasks found."

    task_list = []
    for task in tasks:
        status = "✅" if task["completed"] else "❌"
        task_list.append(f"{status} {task['id']}. {task['task']} \nDue: {task['due_date']} | Priority: {task['priority']}")

    return "\n".join(task_list)

# Handle reminders
def send_reminder(context: CallbackContext):
    task_id = context.job.context['task_id']
    task_desc = context.job.context['task_desc']
    chat_id = context.job.context['chat_id']
    context.bot.send_message(chat_id=chat_id, text=f"⏰ Reminder: {task_desc}")

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Add Task", callback_data='add_task')],
        [InlineKeyboardButton("View Tasks", callback_data='view_tasks')],
        [InlineKeyboardButton("Mark Task as Done", callback_data='mark_done')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Task Reminder Bot! Please choose an option:", reply_markup=reply_markup)

# Callback for inline buttons
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'add_task':
        await query.edit_message_text("Please enter the task description:")
        context.user_data['adding_task'] = True

    elif query.data == 'view_tasks':
        user_id = query.from_user.id
        tasks = load_tasks(user_id)
        task_list = format_tasks(tasks)
        await query.edit_message_text(f"Your tasks:\n{task_list}")

    elif query.data == 'mark_done':
        user_id = query.from_user.id
        tasks = load_tasks(user_id)
        if not tasks:
            await query.edit_message_text("No tasks available to mark as done.")
            return

        keyboard = [
            [InlineKeyboardButton(f"{task['id']}. {task['task']}", callback_data=f"done_{task['id']}")]
            for task in tasks if not task['completed']
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select a task to mark as done:", reply_markup=reply_markup)

    elif query.data == 'help':
        await query.edit_message_text("Here are the available commands:\n- Add Task\n- View Tasks\n- Mark Task as Done\n- Help")

    elif query.data == 'priority':
        # Ask for priority selection
        keyboard = [
            [InlineKeyboardButton("Low", callback_data='priority_low')],
            [InlineKeyboardButton("Medium", callback_data='priority_medium')],
            [InlineKeyboardButton("High", callback_data='priority_high')],
            [InlineKeyboardButton("Critical", callback_data='priority_critical')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Please choose the priority for your task:", reply_markup=reply_markup)

    elif query.data.startswith('priority_'):
        priority = query.data.split('_')[1]
        context.user_data['priority'] = priority
        await query.edit_message_text(f"Priority set to {priority.capitalize()}. Now, select the due date:")

        keyboard = [
            [InlineKeyboardButton("Today", callback_data='due_today')],
            [InlineKeyboardButton("Tomorrow", callback_data='due_tomorrow')],
            [InlineKeyboardButton("Next Week", callback_data='due_next_week')],
            [InlineKeyboardButton("Choose Date", callback_data='due_custom')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select a date:", reply_markup=reply_markup)

    elif query.data.startswith('due_'):
        due_option = query.data.split('_')[1]
        now = datetime.now()
        if due_option == 'today':
            due_date = now
        elif due_option == 'tomorrow':
            due_date = now + timedelta(days=1)
        elif due_option == 'next_week':
            due_date = now + timedelta(weeks=1)
        else:
            await query.edit_message_text("Please enter the due date and time (e.g., 2025-03-28 14:30):")
            context.user_data['waiting_for_date'] = True
            return

        task_desc = context.user_data.get('task_desc')
        priority = context.user_data.get('priority', 'Medium')
        add_task(query.from_user.id, task_desc, due_date.strftime("%Y-%m-%d %H:%M"), priority)
        await query.edit_message_text(f"Task '{task_desc}' added successfully! 📅 Due: {due_date.strftime('%Y-%m-%d %H:%M')}")
        context.user_data.clear()

# Handle text input for task description and due date
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if 'adding_task' in context.user_data and context.user_data['adding_task']:
        context.user_data['task_desc'] = update.message.text
        context.user_data['adding_task'] = False

        # Show priority selection
        keyboard = [
            [InlineKeyboardButton("Low", callback_data='priority_low')],
            [InlineKeyboardButton("Medium", callback_data='priority_medium')],
            [InlineKeyboardButton("High", callback_data='priority_high')],
            [InlineKeyboardButton("Critical", callback_data='priority_critical')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please choose the task priority:", reply_markup=reply_markup)

    elif 'waiting_for_date' in context.user_data and context.user_data['waiting_for_date']:
        due_date_str = update.message.text
        try:
            due_date = dateparser.parse(due_date_str)
            if not due_date:
                raise ValueError

            task_desc = context.user_data['task_desc']
            priority = context.user_data.get('priority', 'Medium')
            add_task(user_id, task_desc, due_date.strftime("%Y-%m-%d %H:%M"), priority)

            await update.message.reply_text(f"Task '{task_desc}' added successfully! 📅 Due: {due_date.strftime('%Y-%m-%d %H:%M')}")
            context.user_data.clear()

        except ValueError:
            await update.message.reply_text("Invalid date format. Please try again.")

# Main function to run the bot
def main() -> None:
    application = Application.builder().token("Enter Your Bot Token").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))  # Corrected to button_handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
