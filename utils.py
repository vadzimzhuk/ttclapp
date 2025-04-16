#!/usr/bin/env python3
"""
utils for the main script
"""

from typing import Dict, List, Any
from tabulate import tabulate
from data import TASK_FIELDS

def display_tasks(tasks: List[Dict[str, str]]) -> None:
    """Display tasks in a tabular format."""
    if not tasks:
        print("No tasks found.")
        return

    table_data = []
    for task in tasks:
        # Truncate note if it's too long for display
        note = task['note']
        if len(note) > 40:  # Limit note length in table view
            note = note[:37] + "..."
        
        table_data.append([
            task['id'],
            task['title'],
            'Open' if task['state'] == 'O' else 'Completed',
            note
        ])
    
    # Print table with headers
    print("\n" + tabulate(
        table_data,
        headers=TASK_FIELDS,
        tablefmt='grid'
    ))