# Task Reminder Bot

This is a simple Telegram bot that allows you to set reminders with customized due dates, priority, and descriptions. It sends you notifications when a task is due. The bot features an intuitive, user-friendly interface with inline buttons to select task priorities, due dates, and times.

## Features

- **Add Tasks**: Set tasks with a description, due date, and priority.
- **View Tasks**: View all the tasks you’ve created.
- **Mark Tasks as Done**: Mark tasks as completed.
- **Priority Management**: Set priority for tasks (Low, Medium, High, Critical).
- **Date/Time Selection**: Easily select due dates and times using inline buttons (Today, Tomorrow, Next Week, or choose a custom date).
- **Task Notifications**: Receive notifications when your task is due.
- **Task Management**: Edit or delete tasks when needed.

## Requirements

Before running the bot, make sure you have the following installed:
- Python 3.7+ (preferably Python 3.12)
- `pip` for installing dependencies

### Dependencies

The following Python packages are required:
- `python-telegram-bot`: Telegram API wrapper for Python.
- `apscheduler`: A simple and flexible task scheduling library.
- `dateparser`: For parsing human-readable dates and times.

To install the dependencies, run:

```bash
pip install -r requirements.txt
Setup Instructions
1. Create a Telegram Bot
Open Telegram and search for the BotFather bot.

Start a conversation with BotFather and use the /newbot command to create a new bot.

Follow the instructions to give your bot a name and username.

After successful creation, BotFather will give you a token. Save this token, as it will be used to interact with the Telegram API.

2. Clone the Repository
Clone the repository to your local machine:

bash
Copy
Edit
git clone https://github.com/hiddent3erminal/telegram-reminder-bot.git
cd telegram-reminder-bot
3. Set Up the Bot Token
In the main.py file, find the line where the bot token is set:

python
Copy
Edit
application = Application.builder().token("YOUR_BOT_TOKEN").build()
Replace "YOUR_BOT_TOKEN" with the token you received from BotFather.

4. Running the Bot
Once everything is set up, run the bot with the following command:

bash
Copy
Edit
python main.py
Your bot should now be up and running. You can start interacting with it on Telegram by searching for your bot by its username.

Bot Commands
The bot supports the following commands:

/start: Starts the bot and shows the main menu.

Add Task: Create a new task with a description, due date, and priority.

View Tasks: View all your created tasks.

Mark Task as Done: Mark a task as completed.

Help: Show the list of available commands.

How the Bot Works
Start Command: When you type /start, the bot will display a menu with options to add tasks, view tasks, and mark them as done.

Adding a Task: When you select Add Task, the bot will ask for a task description. Then, it will prompt you to select the task's priority (Low, Medium, High, Critical). After that, you'll select the due date for the task (Today, Tomorrow, Next Week, or Custom Date). Once everything is set, the bot will save your task and send a confirmation message.

Viewing Tasks: The View Tasks option allows you to see all the tasks you've created along with their due dates and priorities.

Marking Tasks as Done: You can mark a task as completed by selecting it from the list of tasks. The bot will update the task status.

Task Notifications: When a task is due, the bot will send you a notification to remind you.

Task Data Storage
Task data is stored in individual JSON files for each user. These files are named based on the user’s Telegram ID (e.g., user_id_tasks.json). The data includes task descriptions, due dates, and priorities.

Add Task: When a task is created, it is added to the user's JSON file.

View Tasks: All tasks are loaded from the user's JSON file and displayed.

Delete Task: Tasks can be deleted by removing the relevant data from the JSON file.

Mark Task as Done: Tasks can be marked as completed, updating the status in the JSON file.

Customization
Bot Name & Username: You can change the bot's name and username when creating it with BotFather.

Task Data Storage: The bot currently stores data in JSON files, but this can be adapted to use other databases (e.g., SQLite, MySQL, PostgreSQL) if desired.

Troubleshooting
Bot not responding: Ensure the bot token is correctly set in the main.py file.

Task not saved: Check if the user’s task file exists and is properly writable. Ensure the bot has permission to write to the folder where the tasks are stored.

Task not showing up: Verify that the task has been saved correctly in the user's JSON file. Check for any errors related to the file reading/writing process.