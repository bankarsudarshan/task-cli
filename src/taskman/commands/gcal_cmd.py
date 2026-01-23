"""
---------------- GOOGLE CALENDAR ----------------.
parser_gcal = subparsers.add_parser(
    "gcal",
    help="Google Calendar integration",
    description="Sync tasks with Google Calendar.",
)
gcal_subparsers = parser_gcal.add_subparsers(
    title="Google Calendar Commands",
    dest="gcal_command",
    required=True,
)

parser_gcal_add = gcal_subparsers.add_parser(
    "add",
    help="Export a task to Google Calendar",
    description="Create a Google Calendar event for a task with a due date.",
)
parser_gcal_add.add_argument(
    "id",
    type=int,
    help="ID of the task to export",
)
parser_gcal_add.set_defaults(func=task.gcal_add)

parser_gcal_sync = gcal_subparsers.add_parser(
    "sync",
    help="Sync all due tasks to Google Calendar",
    description="Export all tasks that have a due date to Google Calendar.",
)
parser_gcal_sync.set_defaults(func=task.gcal_sync)
"""
