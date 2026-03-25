from taskman.client import CLIClient


def register(subparser, service: CLIClient):
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
    # parser_delete.add_argument(
    #     "--tasks-type",
    #     choices=["in-progress", "todo"],
    #     help="Delete tasks by status",
    # )
    parser_delete.set_defaults(func=lambda args: run_delete(args, service))


def run_delete(args, service: CLIClient):
    tid = service.delete(
        tid=args.id,
        # tasks_type=args.tasks_type,
    )
    if tid is None:
        return "Could not delete the task"
    return f"Task deleted (ID:{tid})"
