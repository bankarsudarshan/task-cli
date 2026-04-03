from taskman.client import request


def register(subparser):
    parser = subparser.add_parser(
        "update",
        help="Update an existing task",
        description="Update task fields such as description, status, or due date.",
    )
    parser.add_argument(
        "id",
        type=str,
        help="ID of the task to update",
    )
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        help="New task description",
    )
    parser.add_argument(
        "-s",
        "--status",
        type=str,
        choices=["todo", "in-progress", "done"],
        help="Update task status",
    )
    parser.add_argument(
        "--due",
        type=str,
        help="Update due date/time (YYYY-MM-DD HH:MM)",
    )
    parser.set_defaults(func=run)


def run(args):
    task_id = args.id
    update_data = {}

    if args.description:
        update_data["description"] = args.description

    if args.status:
        update_data["status"] = args.status

    if args.due:
        update_data["due_at"] = args.due

    # No fields provided
    if not update_data:
        return "⚠️ Nothing to update"

    try:
        request(
            "PUT",
            f"/tasks/{task_id}",
            json=update_data,
        )
    except SystemExit:
        return "❌ Failed to update task"

    return f"✏️ Task updated (ID: {task_id[:8]})"
