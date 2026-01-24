from enum import Enum

from tabulate import tabulate


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


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
