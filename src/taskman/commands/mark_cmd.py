def register(subparser, service):
    parser = subparser.add_parser(
        "mark",
        help="Mark a task as done",
        description="Set task status to 'done' using its ID.",
    )
    parser.add_argument(
        "id",
        type=int,
        help="ID of the task",
    )
    parser.add_argument(
        "status",
        type=str,
        choices=["todo", "in-progress", "done"],
        nargs="?",
        help="Change the status of task",
    )
    parser.set_defaults(func=lambda args: run(args, service))


def run(args, service):
    tid: int = service.mark(tid=args.id, status=args.status)
    if tid is None:
        return f"Could not mark the task as {args.status} (ID:{args.id})"
    return f"Task marked as done (ID:{tid})"
