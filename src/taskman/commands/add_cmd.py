from taskman.client import request


def register(subparser):
    parser = subparser.add_parser(
        "add",
        help="Add a new task",
        description="Create a new task with description, priority, status, and optional due date.",
    )
    parser.add_argument(
        "description",
        type=str,
        help="Task description (wrap in quotes if it contains spaces)",
    )
    parser.add_argument(
        "-s",
        "--status",
        type=str,
        choices=["todo", "in-progress", "done"],
        default="todo",
        nargs="?",
        help="Initial status of the task (default: todo)",
    )
    parser.add_argument(
        "-d",
        "--due",
        type=str,
        default=None,
        help="Due date/time in format YYYY-MM-DD HH:MM",
    )

    parser.set_defaults(func=lambda args: run(args))


def run(args):
    # The command's job is just to extract args and call the client
    response = request(
        "POST",
        "/tasks",
        json={
            "description": args.description,
            "status": args.status,
            "due_at": args.due,
        },
    )

    _ = response.json()
    return "✅ Task created."
