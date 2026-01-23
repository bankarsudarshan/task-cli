from datetime import datetime
from pathlib import Path

from tabulate import tabulate

from taskman.models import Metadata, Task, TasksFile


def load_file(filename: str) -> tuple[list[Task], Metadata]:
    path: Path = Path(filename)

    try:
        with path.open("r", encoding="utf-8") as f:
            json_str = f.read()
        tasks_data: TasksFile = TasksFile.model_validate_json(json_str)
    except Exception as exc:
        print(f"exception raised - {exc}")
        return ([], Metadata(last_tid=0, n_tasks=0))
    else:
        return tasks_data.tasks, tasks_data.metadata


def save_file(tasks_data: TasksFile, filename: str):
    path = Path(filename)

    try:
        json_str = tasks_data.model_dump_json(indent=2)
        with path.open("w", encoding="utf-8") as f:
            f.write(json_str)
    except Exception as exc:
        print(f"exception raised - {exc}")


def render_tasks_table(rows):
    """Render a list of tasks as a formatted table."""
    if not rows:
        return None

    date_fields = ["updated_at", "created_at", "due_at"]

    for row in rows:
        row["priority"] = row["priority"].name
        row["status"] = row["status"].name
        for date_field in date_fields:
            if row[date_field]:
                row[date_field] = row[date_field].strftime("%Y-%m-%d %H:%M")
            else:
                row[date_field] = "" if date_field == "updated_at" else "No due date"

    headers = rows[0].keys()

    # Description gets more width, others default
    col_widths = [
        40
        if k == "description"
        else 15
        if k in ("created_at", "updated_at", "due_at")
        else None
        for k in headers
    ]

    # Left-align description, center everything else
    col_align = ["left" if k == "description" else "center" for k in headers]

    return tabulate(
        rows,
        headers="keys",
        tablefmt="rounded_grid",
        maxcolwidths=col_widths,
        colalign=col_align,
    )
