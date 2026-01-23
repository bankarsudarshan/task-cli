def register(subparser, add_task):
    parser_add = subparser.add_parser(
        "add",
        help="Add a new task",
        description="Create a new task with description, priority, status, and optional due date.",
    )
    parser_add.add_argument(
        "task",
        type=str,
        help="Task description (wrap in quotes if it contains spaces)",
    )
    parser_add.add_argument(
        "-p",
        "--priority",
        type=str,
        choices=["low", "medium", "high"],
        default="medium",
        nargs="?",
        help="Priority of the task (default: medium)",
    )
    parser_add.add_argument(
        "-s",
        "--status",
        type=str,
        choices=["todo", "in-progress", "done"],
        default="todo",
        nargs="?",
        help="Initial status of the task (default: todo)",
    )
    parser_add.add_argument(
        "--due",
        type=str,
        default=None,
        help="Due date/time in format YYYY-MM-DD HH:MM",
    )
    parser_add.set_defaults(func=add_task)
