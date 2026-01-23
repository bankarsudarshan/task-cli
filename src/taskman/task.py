from datetime import datetime
from zoneinfo import ZoneInfo

from taskman import gcal
from taskman.helpers import load_file, render_tasks_table, save_file


def add(args, tasks_file):
    now = datetime.now(tz=ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M")

    new_task = {
        "id": -1,
        "description": args.task,
        "status": args.status,
        "priority": args.priority,
        "createdAt": now,
        "updatedAt": now,
        "dueAt": args.due,
    }
    tasks = load_file(tasks_file)
    tid = -1
    tid = 1 if len(tasks) == 0 else max(int(tid) for tid in tasks) + 1

    new_task["id"] = tid
    tasks[tid] = new_task
    save_file(tasks, tasks_file)
    return f"Task added (ID:{tid})"


def update(args, tasks_file):
    tasks = load_file(tasks_file)
    if len(tasks) == 0:
        print(f"No task with (ID:{args.id})")
        return None

    task_id = str(args.id)
    if task_id not in tasks:
        print(f"No task with (ID:{args.id})")
        return None

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

    task["updatedAt"] = datetime.now(tz="Asia/Kolkata").strftime("%Y-%m-%d %H:%M")

    save_file(tasks, tasks_file)
    return f"Task updated (ID:{task_id})"


def delete(args, tasks_file):
    tasks = load_file(tasks_file)
    tid = args.tid
    if tid not in tasks:
        print(f"No task with (ID:{tid})")
        return None
    del tasks[tid]
    save_file(tasks, tasks_file)
    return f"Task deleted (ID:{tid})"


def list_tasks(args, tasks_file):
    tasks = load_file(tasks_file)
    if len(tasks) == 0:
        print("No tasks added")
        return None

    tasks_type = args.tasks_type
    priority_filter = args.priority
    sort_by = args.sort_by

    filtered = []

    for task in tasks.values():
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
            print(
                f"No tasks with status '{tasks_type}' and priority '{priority_filter}'",
            )
        else:
            print(f"No tasks with status '{tasks_type}'")
        return None

    # sorting
    order = args.order
    reverse = order == "desc"

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


def mark_done(args, tasks_file, archived_file):
    tasks = load_file(tasks_file)
    tid = args.tid
    if len(tasks) == 0 or tid not in tasks:
        print(f"No task with (ID:{tid})")
        return None
    task = tasks[tid]
    del tasks[tid]
    save_file(tasks, tasks_file)
    archived = load_file(archived_file)
    archived[tid] = task
    save_file(archived, archived_file)

    return f"Task marked as done (ID:{tid})"


def mark_in_progress(args, tasks_file):
    tasks = load_file(tasks_file)
    tid = args.tid
    if len(tasks) == 0 or tid not in tasks:
        print(f"No task with (ID:{tid})")
        return None
    tasks[tid]["status"] = "in-progress"
    save_file(tasks, tasks_file)
    return f"Task marked as in-progress (ID:{tid})"


def clear_tasks(args, tasks_file):
    tasks = load_file(tasks_file)
    if len(tasks) == 0:
        return "There are no tasks added"
    tasks_type = args.tasks_type
    new_tasks = {}
    result = f"Cleared tasks marked {tasks_type}"
    if tasks_type != "all":
        new_tasks = {
            tid: task for tid, task in tasks.items() if task["status"] != tasks_type
        }
    else:
        new_tasks = {}
        result = "Cleared all tasks"

    save_file(new_tasks, tasks_file)
    return result


def search_tasks(args, tasks_file):
    tasks = load_file(tasks_file)
    if len(tasks) == 0:
        return "No tasks added"

    keyword = args.keyword.lower()
    matches = []

    for task in tasks.values():
        if keyword in task["description"].lower():
            display_task = task.copy()
            display_task["dueAt"] = task.get("dueAt") or "No due date"
            matches.append(display_task)

    if not matches:
        return f"No tasks found containing: {args.keyword}"

    return render_tasks_table(matches)


def gcal_add(args, tasks_file):
    tasks = load_file(tasks_file)
    task_id = str(args.id)

    if task_id not in tasks:
        return f"No task with (ID:{args.id})"

    task = tasks[task_id]

    if not task.get("dueAt"):
        return f"Task (ID:{args.id}) has no dueAt set"

    gcal.create_event_for_task(task)
    return f"Task (ID:{args.id}) exported to Google Calendar"


def gcal_sync(tasks_file):
    tasks = load_file(tasks_file)
    due_tasks = [t for t in tasks.values() if t.get("dueAt")]

    if not due_tasks:
        return "No tasks with dueAt to sync"

    for task in due_tasks:
        gcal.create_event_for_task(task)

    return f"Synced {len(due_tasks)} tasks to Google Calendar"
