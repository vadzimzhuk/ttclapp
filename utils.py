#!/usr/bin/env python3
"""
Task Tracker CLI Application

A simple command line tool for task tracking with the following features:
- Task properties: id, title, state, note (all strings)
- States: O (open), X (completed)
- Commands: c (create), rm (remove), upd (update), done (complete), note (add note)
- Storage: CSV files (active.csv for open tasks, completed.csv for completed tasks)
"""

import os
import sys
import csv
import uuid
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from tabulate import tabulate  # For pretty table printing

# File paths for storage
DATA_DIR = Path.home() / '.task-tracker'
ACTIVE_TASKS_FILE = DATA_DIR / 'active.csv'
COMPLETED_TASKS_FILE = DATA_DIR / 'completed.csv'

# Task field definitions
TASK_FIELDS = ['id', 'title', 'state', 'note']

def ensure_data_dir() -> None:
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def ensure_files_exist() -> None:
    """Ensure CSV files exist with headers."""
    ensure_data_dir()
    
    for file_path in [ACTIVE_TASKS_FILE, COMPLETED_TASKS_FILE]:
        if not file_path.exists():
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=TASK_FIELDS)
                writer.writeheader()

def read_tasks(file_path: Path) -> List[Dict[str, str]]:
    """Read tasks from CSV file."""
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except Exception as e:
        print(f"Error reading tasks from {file_path}: {e}")
        return []

def write_tasks(file_path: Path, tasks: List[Dict[str, str]]) -> None:
    """Write tasks to CSV file."""
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=TASK_FIELDS)
            writer.writeheader()
            writer.writerows(tasks)
    except Exception as e:
        print(f"Error writing tasks to {file_path}: {e}")

def display_tasks(tasks: List[Dict[str, str]]) -> None:
    """Display tasks in a tabular format."""
    if not tasks:
        print("No tasks found.")
        return

    # Prepare table rows with formatted data
    table_data = []
    for task in tasks:
        # Truncate note if it's too long for display
        note = task['note']
        if len(note) > 40:  # Limit note length in table view
            note = note[:37] + "..."
        
        # Add row with formatted data
        table_data.append([
            task['id'],
            task['title'],
            'Open' if task['state'] == 'O' else 'Completed',
            note
        ])
    
    # Print table with headers
    print("\n" + tabulate(
        table_data,
        headers=['ID', 'Title', 'State', 'Note'],
        tablefmt='grid'
    ))

def create_task(title: str, note: str = "") -> None:
    """Create a new task."""
    # Validate required title
    if not title.strip():
        print("Error: Title is required")
        return
        
    task = {
        'id': str(uuid.uuid4())[:8],  # Using shortened UUID for better readability
        'title': title,
        'state': 'O',  # New tasks are always open
        'note': note
    }

    tasks = read_tasks(ACTIVE_TASKS_FILE)
    tasks.append(task)
    write_tasks(ACTIVE_TASKS_FILE, tasks)
    
    print(f"Task created with ID: {task['id']}")

def remove_task(task_id: str) -> None:
    """Remove a task by ID."""
    # Try to remove from active tasks
    active_tasks = read_tasks(ACTIVE_TASKS_FILE)
    initial_active_count = len(active_tasks)
    active_tasks = [task for task in active_tasks if task['id'] != task_id]
    
    if len(active_tasks) < initial_active_count:
        write_tasks(ACTIVE_TASKS_FILE, active_tasks)
        print(f"Task {task_id} has been removed.")
        return
    
    # If not found in active tasks, try completed tasks
    completed_tasks = read_tasks(COMPLETED_TASKS_FILE)
    initial_completed_count = len(completed_tasks)
    completed_tasks = [task for task in completed_tasks if task['id'] != task_id]
    
    if len(completed_tasks) < initial_completed_count:
        write_tasks(COMPLETED_TASKS_FILE, completed_tasks)
        print(f"Task {task_id} has been removed.")
        return
    
    print(f"No task found with ID: {task_id}")

def update_task(task_id: str, title: Optional[str] = None, note: Optional[str] = None) -> None:
    """Update a task by ID."""
    # Try to update in active tasks
    active_tasks = read_tasks(ACTIVE_TASKS_FILE)
    
    for task in active_tasks:
        if task['id'] == task_id:
            if title is not None:
                task['title'] = title
            if note is not None:
                task['note'] = note
            write_tasks(ACTIVE_TASKS_FILE, active_tasks)
            print(f"Task {task_id} has been updated.")
            return
    
    # Try to update in completed tasks
    completed_tasks = read_tasks(COMPLETED_TASKS_FILE)
    
    for task in completed_tasks:
        if task['id'] == task_id:
            if title is not None:
                task['title'] = title
            if note is not None:
                task['note'] = note
            write_tasks(COMPLETED_TASKS_FILE, completed_tasks)
            print(f"Task {task_id} has been updated.")
            return
    
    print(f"No task found with ID: {task_id}")

def add_note(task_id: str, additional_note: str) -> None:
    """Add a note to an existing task, preserving previous notes."""
    if not additional_note.strip():
        print("Error: Note content is required")
        return
        
    # Format with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    formatted_note = f"[{timestamp}] {additional_note}"
    
    # Try to find in active tasks
    active_tasks = read_tasks(ACTIVE_TASKS_FILE)
    
    for task in active_tasks:
        if task['id'] == task_id:
            # Add to existing note or set as new note
            current_note = task['note'].strip()
            if current_note:
                task['note'] = f"{current_note}\n{formatted_note}"
            else:
                task['note'] = formatted_note
            
            write_tasks(ACTIVE_TASKS_FILE, active_tasks)
            print(f"Note added to task {task_id}.")
            return
    
    # Try to find in completed tasks
    completed_tasks = read_tasks(COMPLETED_TASKS_FILE)
    
    for task in completed_tasks:
        if task['id'] == task_id:
            # Add to existing note or set as new note
            current_note = task['note'].strip()
            if current_note:
                task['note'] = f"{current_note}\n{formatted_note}"
            else:
                task['note'] = formatted_note
                
            write_tasks(COMPLETED_TASKS_FILE, completed_tasks)
            print(f"Note added to task {task_id}.")
            return
    
    print(f"No task found with ID: {task_id}")

def complete_task(task_id: str) -> None:
    """Mark a task as completed."""
    # Find the task in active tasks
    active_tasks = read_tasks(ACTIVE_TASKS_FILE)
    completed_task = None
    
    for i, task in enumerate(active_tasks):
        if task['id'] == task_id:
            completed_task = task
            completed_task['state'] = 'X'
            active_tasks.pop(i)
            break
    
    if completed_task is None:
        print(f"No active task found with ID: {task_id}")
        return
    
    # Write updated active tasks
    write_tasks(ACTIVE_TASKS_FILE, active_tasks)
    
    # Add to completed tasks
    completed_tasks = read_tasks(COMPLETED_TASKS_FILE)
    completed_tasks.append(completed_task)
    write_tasks(COMPLETED_TASKS_FILE, completed_tasks)
    
    print(f"Task {task_id} has been marked as completed.")

def list_tasks(show_completed: bool = False) -> None:
    """List tasks."""
    file_path = COMPLETED_TASKS_FILE if show_completed else ACTIVE_TASKS_FILE
    tasks = read_tasks(file_path)
    
    print(f"\n{'COMPLETED' if show_completed else 'ACTIVE'} TASKS:")
    display_tasks(tasks)

def show_task_details(task_id: str) -> None:
    """Show all details of a specific task, including full notes."""
    # Check active tasks first
    active_tasks = read_tasks(ACTIVE_TASKS_FILE)
    for task in active_tasks:
        if task['id'] == task_id:
            print("\nTASK DETAILS:")
            print(f"ID: {task['id']}")
            print(f"Title: {task['title']}")
            print(f"State: {'Open' if task['state'] == 'O' else 'Completed'}")
            print(f"Notes:\n{task['note']}" if task['note'] else "Notes: None")
            return
    
    # Check completed tasks if not found
    completed_tasks = read_tasks(COMPLETED_TASKS_FILE)
    for task in completed_tasks:
        if task['id'] == task_id:
            print("\nTASK DETAILS:")
            print(f"ID: {task['id']}")
            print(f"Title: {task['title']}")
            print(f"State: {'Open' if task['state'] == 'O' else 'Completed'}")
            print(f"Notes:\n{task['note']}" if task['note'] else "Notes: None")
            return
    
    print(f"No task found with ID: {task_id}")

def main() -> None:
    """Main CLI entry point."""
    # Ensure data files exist
    ensure_files_exist()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create task command
    create_parser = subparsers.add_parser("c", help="Create a new task")
    create_parser.add_argument("title", help="Task title")
    create_parser.add_argument("--note", "-n", help="Task note (optional)")
    
    # Remove task command
    remove_parser = subparsers.add_parser("rm", help="Remove a task")
    remove_parser.add_argument("id", help="Task ID to remove")
    
    # Update task command
    update_parser = subparsers.add_parser("upd", help="Update a task")
    update_parser.add_argument("id", help="Task ID to update")
    update_parser.add_argument("--title", "-t", help="New task title")
    
    # Complete task command
    complete_parser = subparsers.add_parser("done", help="Mark a task as completed")
    complete_parser.add_argument("id", help="Task ID to complete")
    
    # Add note command
    note_parser = subparsers.add_parser("note", help="Add a note to a task")
    note_parser.add_argument("id", help="Task ID")
    note_parser.add_argument("text", help="Note text")
    
    # List tasks command
    list_parser = subparsers.add_parser("ls", help="List tasks")
    list_parser.add_argument("--completed", "-c", action="store_true", help="Show completed tasks")
    list_parser.add_argument("--all", "-a", action="store_true", help="Show all tasks")
    
    # View task details command
    view_parser = subparsers.add_parser("view", help="View detailed information about a task")
    view_parser.add_argument("id", help="Task ID to view")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "c":
        create_task(args.title, args.note or "")
    elif args.command == "rm":
        remove_task(args.id)
    elif args.command == "upd":
        update_task(args.id, args.title)
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "note":
        add_note(args.id, args.text)
    elif args.command == "ls":
        if args.all:
            list_tasks(False)
            list_tasks(True)
        else:
            list_tasks(args.completed)
    elif args.command == "view":
        show_task_details(args.id)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()