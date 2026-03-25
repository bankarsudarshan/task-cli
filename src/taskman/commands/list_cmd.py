from taskman.client import request
from taskman.utils import render_tasks_table


def register(subparser):
    parser = subparser.add_parser(
        "list",
        help="List tasks",
        description="List tasks with filters and sorting.",
    )
    parser.add_argument(
        "status",
        type=str,
        choices=["in-progress", "todo", "done", "all"],
        default="all",
        nargs="?",
        help="Filter tasks by status (default: all)",
    )
    parser.add_argument(
        "-sb",
        "--sort-by",
        type=str,
        choices=["id", "created_at", "updated_at", "due_at", "status"],
        default="id",
    )
    parser.add_argument(
        "-o",
        "--order",
        type=str,
        choices=["asc", "desc"],
        default="asc",
    )

    parser.set_defaults(func=run)


def run(args):
    params = {}

    if args.status != "all":
        params["status"] = args.status

    params["sort_by"] = args.sort_by
    params["order"] = args.order

    response = request(
        "GET",
        "/tasks/",
        params=params,
    )

    data = response.json()
    tasks = data.get("tasks", [])

    return render_tasks_table(tasks)
