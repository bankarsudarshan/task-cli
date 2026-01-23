from datetime import datetime
from typing import Any

from taskman import gcal
from taskman.helpers import load_file, render_tasks_table, save_file
from taskman.models import Metadata, Task, TaskPriority, TasksFile, TaskStatus


def add(args, tasks_file) -> str:
    new_task = Task(
        description=args.task,
        status=args.status,
        priority=args.priority,
        due_at=args.due,
    )

    tasks_data = load_file(tasks_file)
    (tasks, metadata) = (
        tasks_data if tasks_data else ([], Metadata(n_tasks=0, last_tid=1))
    )

    tid: int = metadata.last_tid + 1
    new_task.id = tid
    tasks.append(new_task)
    metadata.last_tid = tid
    metadata.n_tasks += 1

    save_file(
        TasksFile(tasks=tasks, metadata=metadata),
        tasks_file,
    )
    return f"Task added (ID:{tid})"


def update(args, tasks_file) -> str:
    tasks, _ = load_file(tasks_file)
    tid_s = [task.id for task in tasks]
    tid: int = args.id

    if len(tid_s) == 0 or tid not in tid_s:
        return f"No task with (ID:{tid})"

    if not any([args.description, args.priority, args.status, args.due]):
        return f"No fields to update for (ID:{args.id})"

    updates: dict[str, Any] = {}
    if args.description is not None:
        updates["description"] = args.description
    if args.priority is not None:
        updates["priority"] = TaskPriority(args.priority.lower())
    if args.status is not None:
        updates["status"] = TaskStatus(args.status.lower())
    if args.due is not None:
        updates["due_at"] = datetime.strptime(args.due, "%Y-%m-%d %H:%M")  # noqa: DTZ007
    updates["updated_at"] = datetime.now()  # noqa: DTZ005

    task = tasks[tid_s.index(tid)]
    tasks[tid_s.index(tid)] = task.model_copy(update=updates)

    save_file(
        TasksFile(tasks=tasks, metadata=_),
        tasks_file,
    )
    return f"Task updated (ID:{tid})"


def delete(args, tasks_file) -> str:
    tasks, metadata = load_file(tasks_file)
    tid_s = [task.id for task in tasks]
    tid: int = args.id

    if tid not in tid_s:
        return f"No task with (ID:{tid})"

    del tasks[tid_s.index(tid)]

    if metadata.last_tid == tid:
        metadata.last_tid -= 1
    metadata.n_tasks -= 1

    save_file(
        TasksFile(tasks=tasks, metadata=metadata),
        tasks_file,
    )
    return f"Task deleted (ID:{tid})"


def list_tasks(args, tasks_file) -> str:
    tasks, _ = load_file(tasks_file)
    if len(tasks) == 0:
        return "No tasks added"

    task_filters = [task_type.upper() for task_type in args.tasks_type]
    priority_filter = args.priority
    sort_by = args.sort_by

    filtered = []

    for task_model in tasks:
        task = task_model.model_dump()

        # filter by status
        for task_type in task_filters:
            if task_type != "all" and task.get("status") != task_type:
                continue

        # filter by prioprintrity if requested
        if priority_filter is not None and task["priority"] != priority_filter:
            continue

        filtered.append(task)

    if not filtered:
        if priority_filter is not None:
            return f"No tasks with status '{task_filters}' and priority '{priority_filter}'"
        return f"No tasks with status '{task_filters}'"

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


"""
def mark_done(args, tasks_file, archived_file):
    tasks, _ = load_file(tasks_file)
    tid_s = [task.id for task in tasks]
    tid = args.tid

    if len(tasks) == 0 or tid not in tid_s:
        return f"No task with (ID:{tid})"

    delete_idx = tid_s.index(tid)
    task = tasks[delete_idx]
    del tasks[delete_idx]
    save_file(TasksFile(tasks=tasks, metadata=_), tasks_file)

    archived_tasks, metadata = load_file(archived_file)
    archived_tid_s = [task.id for task in archived_tasks]
    insert_idx = next(
        (idx for idx, archived_tid in enumerate(archived_tid_s) if archived_tid >= tid),
        metadata.n_tasks,
    )
    archived_tasks.insert(insert_idx-1, task)
    save_file(archived, archived_file)

    return f"Task marked as done (ID:{tid})"
"""


def mark_in_progress(args, tasks_file):
    tasks, _ = load_file(tasks_file)
    tid_s = [task.id for task in tasks]
    tid = args.id

    if len(tid_s) == 0 or tid not in tid_s:
        return f"No task with (ID:{tid})"

    tasks[tid_s.index(tid)].status = TaskStatus("in-progress")
    tasks[tid_s.index(tid)].updated_at = datetime.now()  # noqa: DTZ005

    save_file(
        TasksFile(tasks=tasks, metadata=_),
        tasks_file,
    )
    return f"Task marked as in-progress (ID:{tid})"


def clear_tasks(args, tasks_file):
    tasks, _ = load_file(tasks_file)
    tasks_status = args.tasks_status

    if len(tasks) == 0:
        return "There are no tasks added"

    new_tasks = []
    if tasks_status == "all":
        result = "Cleared all tasks"
    else:
        new_tasks = [task for task in tasks if task.status != tasks_status]
        result = f"Cleared tasks marked {tasks_status}"

    save_file(
        TasksFile(tasks=new_tasks, metadata=_),
        tasks_file,
    )
    return result


def search_tasks(args, tasks_file):
    tasks, _ = load_file(tasks_file)
    keyword = args.keyword.lower()

    if len(tasks) == 0:
        return "No tasks added"

    matches = []
    for task in tasks:
        if keyword in task.description.lower():
            matches.append(task)

    if not matches:
        return f"No tasks found containing: {args.keyword}"

    return render_tasks_table(matches)


def gcal_add(args, tasks_file):
    tasks = load_file(tasks_file)
    task_id = str(args.id)

    if task_id not in tasks:
        return f"No task with (ID:{args.id})"

    task = tasks[task_id]

    if not task.get("due_at"):
        return f"Task (ID:{args.id}) has no due_at set"

    gcal.create_event_for_task(task)
    return f"Task (ID:{args.id}) exported to Google Calendar"


def gcal_sync(tasks_file):
    tasks = load_file(tasks_file)
    due_tasks = [t for t in tasks.values() if t.get("due_at")]

    if not due_tasks:
        return "No tasks with due_at to sync"

    for task in due_tasks:
        gcal.create_event_for_task(task)

    return f"Synced {len(due_tasks)} tasks to Google Calendar"
