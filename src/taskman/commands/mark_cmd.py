def register_mark_done(subparser, mark_done):
    pass


"""
# ---------------- MARK DONE ----------------
parser_mark_done = subparsers.add_parser(
    "mark-done",
    help="Mark a task as done",
    description="Set task status to 'done' using its ID.",
)
parser_mark_done.add_argument(
    "id",
    help="ID of the task",
)
parser_mark_done.set_defaults(func=task.mark_done)
"""


def register_mark_in_progress(subparser, mark_in_progress):
    parser_mark_in_progress = subparser.add_parser(
        "mark-in-progress",
        help="Mark a task as in-progress",
        description="Set task status to 'in-progress' using its ID.",
    )
    parser_mark_in_progress.add_argument(
        "id",
        type=int,
        help="ID of the task",
    )
    parser_mark_in_progress.set_defaults(func=mark_in_progress)
