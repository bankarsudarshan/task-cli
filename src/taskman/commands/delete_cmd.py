from taskman.client import get_full_id, request


def register(subparser):
    parser = subparser.add_parser(
        "delete",
        help="Delete a task",
        description="Remove a task permanently using its ID.",
    )

    parser.add_argument(
        "id",
        type=str,
        help="ID of the task to delete",
    )

    parser.set_defaults(func=run)


def run(args):
    task_id = get_full_id(args.id)  # short-id support
    print(task_id)
    try:
        request(
            "DELETE",
            f"/tasks/{task_id}",
        )
    except SystemExit:
        return "❌ Failed to delete task"

    return f"🗑️ Task deleted (ID: {task_id[:8]})"
