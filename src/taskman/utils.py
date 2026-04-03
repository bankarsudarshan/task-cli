from datetime import datetime

from tabulate import tabulate


def _format_datetime(value, empty_text=""):
    if not value:
        return empty_text

    try:
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M")

        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(value)


def render_tasks_table(rows):
    if not rows:
        return "No tasks found."

    formatted_rows = []

    for row in rows:
        formatted_rows.append(
            {
                "id": str(row.get("id", ""))[:8],
                "description": row.get("description", ""),
                "status": str(row.get("status", "")).lower(),
                "created_at": _format_datetime(row.get("created_at")),
                "due_at": _format_datetime(
                    row.get("due_at") or row.get("due"),
                    "No due date",
                ),
            },
        )

    headers = [
        "id",
        "description",
        "status",
        "created_at",
        "due_at",
    ]

    # Convert dict → list (avoids tabulate header issues completely)
    table_data = [[row[h] for h in headers] for row in formatted_rows]

    col_widths = [10, 40, 12, 12, 17, 17, 17]
    col_align = ["center", "left", "center", "center", "center", "center", "center"]

    return tabulate(
        table_data,
        headers=headers,
        tablefmt="rounded_grid",
        maxcolwidths=col_widths,
        colalign=col_align,
    )
