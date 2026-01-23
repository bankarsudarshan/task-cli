def register(subparser, delete_task):
    parser_delete = subparser.add_parser(
        "delete",
        help="Delete a task",
        description="Remove a task permanently using its ID.",
    )
    parser_delete.add_argument(
        "id",
        type=int,
        help="ID of the task to delete",
    )
    parser_delete.set_defaults(func=delete_task)


def register_clear(subparser, clear_tasks):
    parser_clear = subparser.add_parser(
        "clear",
        help="Clear tasks",
        description="Delete tasks by status or clear all tasks.",
    )
    parser_clear.add_argument(
        "tasks_status",
        type=str,
        choices=["in-progress", "todo", "done", "all"],
        help="Type of tasks to clear",
    )
    parser_clear.set_defaults(func=clear_tasks)
