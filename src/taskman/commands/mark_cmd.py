from taskman.client import get_full_id, request


def register(subparser):
    parser = subparser.add_parser(
        "mark",
        help="Update task status",
        description="Set task status (todo, in-progress, done).",
    )
    parser.add_argument(
        "id",
        type=str,  # ✅ UUID
        help="Task ID",
    )
    parser.add_argument(
        "status",
        type=str,
        choices=["todo", "in-progress", "done"],
        help="New status",
    )
    parser.set_defaults(func=run)


def run(args):
    short_id = args.id
    status = args.status

    # short-id support
    task_id = get_full_id(short_id)

    try:
        request(
            "PUT",
            f"/tasks/{task_id}",
            json={"status": status},
        )
    except SystemExit:
        return f"❌ Failed to mark task as {status}"

    return f"✅ Task marked as {status} (ID: {task_id[:8]})"
