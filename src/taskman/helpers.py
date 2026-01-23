import json
from pathlib import Path

from tabulate import tabulate


def load_file(filename: str):
    path: Path = Path(filename)

    if not path.is_file():
        path.touch()
        return {}

    if path.stat().st_size == 0:
        return {}

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_file(tasks: dict, filename: str):
    path = Path(filename)
    with path.open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent="2")


def render_tasks_table(rows):
    """
    Render a list of tasks as a formatted table.

    Automatically adapts column widths and alignment based on data.
    """
    if not rows:
        return None

    headers = rows[0].keys()

    # Description gets more width, others default
    col_widths = [
        40
        if k == "description"
        else 15
        if k in ("createdAt", "updatedAt", "dueAt")
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
