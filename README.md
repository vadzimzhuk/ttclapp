# Python Task Tracker CLI

A simple command line task tracking application built with Python.

## Features

- Track tasks with ID, title, state, and notes
- Commands for creating, removing, updating, completing tasks, and adding notes
- Separate storage for active and completed tasks
- Easily extensible for future AI integrations

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/python-task-tracker.git
cd python-task-tracker
```

2. Make the script executable:
```
chmod +x task_tracker.py
```

3. (Optional) Create a symbolic link to make it available system-wide:
```
sudo ln -s $(pwd)/task_tracker.py /usr/local/bin/task-tracker
```

## Usage

### Commands

- `task-tracker c <title> [--note <note>]` - Create a new task
- `task-tracker rm <id>` - Remove a task by ID
- `task-tracker upd <id> [--title <title>]` - Update a task's title
- `task-tracker done <id>` - Mark a task as completed
- `task-tracker note <id> <text>` - Add a note to a task (with timestamp)
- `task-tracker ls [options]` - List tasks
  - Options:
    - `-c, --completed` - Show completed tasks
    - `-a, --all` - Show all tasks (both active and completed)

### Examples

```bash
# Create a new task
task-tracker c "Buy groceries" --note "Need milk and eggs"

# Remove a task with ID 'a1b2c3d4'
task-tracker rm a1b2c3d4

# Update the title of a task
task-tracker upd a1b2c3d4 --title "Buy groceries and cleaning supplies"

# Add a note to an existing task
task-tracker note a1b2c3d4 "Don't forget to buy bread too"

# Mark a task as completed
task-tracker done a1b2c3d4

# List all active tasks
task-tracker ls

# List completed tasks
task-tracker ls --completed

# List all tasks
task-tracker ls --all
```

## Data Storage

Tasks are stored in CSV files:
- Active tasks: `~/.task-tracker/active.csv`
- Completed tasks: `~/.task-tracker/completed.csv`

## Note Format

When you add notes using the `note` command, they are automatically timestamped and appended to any existing notes. The format is:

```
[YYYY-MM-DD HH:MM] Your note text
```

Multiple notes are separated by newlines, creating a chronological history of notes for each task.

## Extending with AI Integration

This application is designed to be easily extensible. To add AI integration:

1. Install an AI SDK:
```
pip install openai
```

2. Create a new module for AI features
3. Import and use the AI module in the existing commands or create new ones

## License

MIT
