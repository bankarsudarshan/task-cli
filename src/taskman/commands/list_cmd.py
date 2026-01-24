from taskman.core.services import CLIService
from taskman.utils import render_tasks_table


def register(subparser, service: CLIService):
    parser_list = subparser.add_parser(
        "list",
        help="List tasks",
        description="List tasks filtered by status, priority, and sorting options.",
    )
    parser_list.add_argument(
        "tasks_type",
        type=str,
        choices=["in-progress", "todo", "done", "all"],
        default="all",
        nargs="?",
        help="Filter tasks by status (default: all)",
    )
    parser_list.add_argument(
        "-p",
        "--priority",
        type=str,
        choices=["low", "medium", "high"],
        help="Filter tasks by priority",
    )
    parser_list.add_argument(
        "-sb",
        "--sort-by",
        type=str,
        choices=["id", "created_at", "updated_at", "priority", "status"],
        default="id",
        help="Sort tasks by a specific field (default: id)",
    )
    parser_list.add_argument(
        "-o",
        "--order",
        type=str,
        choices=["asc", "desc"],
        default="asc",
        help="Sort order (default: asc)",
    )
    parser_list.set_defaults(func=lambda args: run(args, service))


def run(args, service: CLIService):
    filters = {
        "tasks_type": args.tasks_type,
        "priority": args.priority,
        "sort_by": args.sort_by,
        "order": args.order,
    }
    tasks = service.get_tasks(filters)
    return render_tasks_table(tasks)
