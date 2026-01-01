import json
from datetime import datetime

from taskman import gcal
from taskman.helpers import load_file, save_file, render_tasks_table


def add(args, filename):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    new_task = {
        "id": -1,
        "description": args.task,
        "status": args.status,  
        "priority": args.priority,
        "createdAt": now,
        "updatedAt": now,
        "dueAt": args.due,
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

    task_id = str(args.id)
    if task_id not in tasks:
        print(f"No task with (ID:{args.id})")
        return
        
    task = tasks[task_id]
    changed = False

    if args.description is not None:
        task["description"] = args.description
        changed = True

    if args.priority is not None:
        task["priority"] = args.priority
        changed = True

    if args.status is not None:
        task["status"] = args.status
        changed = True

    if args.due is not None:
        task["dueAt"] = args.due
        changed = True

    if not changed:
        return f"No fields to update for (ID:{args.id})"

    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    save_file(tasks, filename)
    return f"Task updated (ID:{task_id})"

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
        print("No tasks added")
        return

    tasks_type = args.tasks_type
    priority_filter = args.priority
    sort_by = args.sort_by

    filtered = []

    for task_id, task in tasks.items():
        # filter by status
        if tasks_type != "all" and task.get("status") != tasks_type:
            continue
        
        # filter by priority if requested
        if priority_filter is not None and task["priority"] != priority_filter:
            continue

        # Create a copy with formatted dueAt
        display_task = task.copy()
        display_task["dueAt"] = task.get("dueAt") or "No due date"
        filtered.append(display_task)
    
    if not filtered:
        if priority_filter is not None:
            print(f"No tasks with status '{tasks_type}' and priority '{priority_filter}'")
        else:
            print(f"No tasks with status '{tasks_type}'")
        return

    # sorting
    order = args.order
    reverse = (order == "desc")

    if sort_by == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        filtered.sort(
            key=lambda t: priority_order.get(t.get("priority"), 3),
            reverse=reverse,
        )
    elif sort_by == "status":
        status_order = {"todo": 0, "in-progress": 1, "done": 2}
        filtered.sort(
            key=lambda t: status_order.get(t.get("status"), 3),
            reverse=reverse,
        )
    else:
        filtered.sort(
            key=lambda t: t.get(sort_by, ""),
            reverse=reverse,
        )

    return render_tasks_table(filtered)

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

def search_tasks(args, filename):
    tasks = load_file(filename)
    if len(tasks) == 0:
        return "No tasks added"

    keyword = args.keyword.lower()
    matches = []

    for task_id, task in tasks.items():
        if keyword in task["description"].lower():
            display_task = task.copy()
            display_task["dueAt"] = task.get("dueAt") or "No due date"
            matches.append(display_task)

    if not matches:
        return f"No tasks found containing: {args.keyword}"

    return render_tasks_table(matches)

def gcal_add(args, filename):
    tasks = load_file(filename)
    task_id = str(args.id)

    if task_id not in tasks:
        return f"No task with (ID:{args.id})"

    task = tasks[task_id]

    if not task.get("dueAt"):
        return f"Task (ID:{args.id}) has no dueAt set"

    gcal.create_event_for_task(task)
    return f"Task (ID:{args.id}) exported to Google Calendar"


def gcal_sync(args, filename):
    tasks = load_file(filename)
    due_tasks = [t for t in tasks.values() if t.get("dueAt")]

    if not due_tasks:
        return "No tasks with dueAt to sync"

    for task in due_tasks:
        gcal.create_event_for_task(task)

    return f"Synced {len(due_tasks)} tasks to Google Calendar"
