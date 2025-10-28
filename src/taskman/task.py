import json
from datetime import datetime
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

def add(args, filename):
    new_task = {
        "id": -1,
        "description": args.task,
        "status": "todo",
        "createdAt": str(datetime.now()),
        "updatedAt": str(datetime.now())
    }
    tasks = load_file(filename)
    id = -1
    if len(tasks) == 0:
        id = 1
    else:
        id = int(max(tasks)) + 1

    new_task["id"] = id
    tasks[id] = new_task
    save_file(tasks, filename)
    return f"Task added (ID:{id})"

def update(args, filename):
    tasks = load_file(filename)
    if len(tasks) == 0:
        print(f"No task with (ID:{args.id})")
        return
    id = str(args.id)
    if id not in tasks:
        print(f"No task with (ID:{args.id})")
        return
    else:
        tasks[id]["description"] = args.new_desc
    save_file(tasks, filename)
    return f"Task updated (ID:{id})"

def delete(args, filename):
    tasks = load_file(filename)
    id = args.id
    if id not in tasks:
        print(f"No task with (ID:{id})")
        return
    else:
        del tasks[id]
    save_file(tasks, filename)
    return f"Task deleted (ID:{id})"

def list_tasks(args, filename):
    tasks = load_file(filename)
    if len(tasks) == 0:
        print(f"No tasks added")
        return
    tasks_type = args.tasks_type
    new_tasks = {}
    if tasks_type != "all":
        for id, task in tasks.items():
            if task["status"] == tasks_type:
                new_tasks[id] = task
    else:
        new_tasks = tasks

    col_widths = [None, 40, None, None, None]
    return tabulate(
        new_tasks.values(), 
        headers="keys", 
        tablefmt="rounded_grid", 
        maxcolwidths=col_widths, 
        colalign=['center']*5
    )

def mark_done(args, filename):
    tasks = load_file(filename)
    id = args.id
    if len(tasks) == 0 or id not in tasks:
        print(f"No task with (ID:{id})")
        return
    else:
        tasks[id]['status'] = "done"
    save_file(tasks, filename)
    return f"Task marked as done (ID:{id})"

def mark_in_progress(args, filename):
    tasks = load_file(filename)
    id = args.id
    if len(tasks) == 0 or id not in tasks:
        print(f"No task with (ID:{id})")
        return
    else:
        tasks[id]['status'] = "in-progress"
    save_file(tasks, filename)
    return f"Task marked as in-progress (ID:{id})"

def clear_tasks(args, filename):
    tasks = load_file(filename)
    if len(tasks) == 0:
        return f"There are no tasks added"
    tasks_type = args.tasks_type
    new_tasks = {}
    result = f"Cleared tasks marked {tasks_type}"
    if tasks_type != "all":
        for id, task in tasks.items():
            if task["status"] != tasks_type:
                new_tasks[id] = task
    else:
        new_tasks = {}
        result = f"Cleared all tasks"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(new_tasks, f, indent='\t') # json.dumps() outputs a nice formated string
    return result