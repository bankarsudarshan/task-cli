from taskman.client import CLIClient


def register(subparser, service: CLIClient):
    parser_update = subparser.add_parser(
        "update",
        help="Update an existing task",
        description="Update task fields such as description, priority, status, or due date.",
    )
    parser_update.add_argument(
        "id",
        type=int,
        help="ID of the task to update",
    )
    parser_update.add_argument(
        "-d",
        "--description",
        type=str,
        help="New task description",
    )
    parser_update.add_argument(
        "-p",
        "--priority",
        type=str,
        choices=["low", "medium", "high"],
        help="Update task priority",
    )
    parser_update.add_argument(
        "-s",
        "--status",
        type=str,
        choices=["todo", "in-progress", "done"],
        help="Update task status",
    )
    parser_update.add_argument(
        "--due",
        type=str,
        help="Update due date/time (YYYY-MM-DD HH:MM)",
    )
    parser_update.set_defaults(func=lambda args: run(args, service))


def run(args, service: CLIClient):
    tid = service.update(
        args.id,
        args.description,
        args.priority,
        args.status,
        args.due,
    )
    if not tid:
        return "Task not updated"
    return f"Task updated (ID:{tid})"
