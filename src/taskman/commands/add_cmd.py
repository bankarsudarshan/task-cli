def register(subparser, service):
    parser = subparser.add_parser(
        "add",
        help="Add a new task",
        description="Create a new task with description, priority, status, and optional due date.",
    )
    parser.add_argument(
        "task",
        type=str,
        help="Task description (wrap in quotes if it contains spaces)",
    )
    parser.add_argument(
        "-p",
        "--priority",
        type=str,
        choices=["low", "medium", "high"],
        default="medium",
        nargs="?",
        help="Priority of the task (default: medium)",
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
        "--due",
        type=str,
        default=None,
        help="Due date/time in format YYYY-MM-DD HH:MM",
    )

    parser.set_defaults(func=lambda args: run(args, service))


def run(args, service):
    # The command's job is just to extract args and call the service
    tid = service.add(
        description=args.task,
        priority=args.priority,
        status=args.status,
        due_at=args.due,
    )
    return f"Success: Task added with ID {tid}"
