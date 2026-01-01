import json
import os

from tabulate import tabulate


def load_file(filename):
    if not os.path.isfile(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            pass
        return {}
    
    elif os.stat(filename).st_size == 0:
        return {}
    
    tasks = None
    with open(filename, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    return tasks


def save_file(tasks, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent="\t")


def render_tasks_table(rows):
    """
    Render a list of task dictionaries as a formatted table.
    Automatically adapts column widths and alignment based on data.
    """
    if not rows:
        return None

    headers = rows[0].keys()

    # Description gets more width, others default
    col_widths = [40 if k == "description" 
                  else 20 if k in ("createdAt", "updatedAt") 
                  else None 
                  for k in headers]

    # Left-align description, center everything else
    col_align = ["left" if k == "description" 
                 else "center" for k in headers]

    return tabulate(
        rows,
        headers="keys",
        tablefmt="rounded_grid",
        maxcolwidths=col_widths,
        colalign=col_align,
    )