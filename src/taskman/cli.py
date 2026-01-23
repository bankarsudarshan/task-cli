from argparse import ArgumentParser
from pathlib import Path

from . import task

taskman_dir = Path("~/taskman-test").expanduser().resolve()
tasks_file = taskman_dir / "tasks.json"
archived_file = taskman_dir / "archived.json"

taskman_dir.mkdir(parents=True, exist_ok=True)


def main():
    parser = ArgumentParser(
        prog="taskman",
        description="A simple CLI-based task manager with priorities, due dates, and Google Calendar integration.",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="l1_subparser",
        required=True,
        help="Available task management commands",
    )

    # ---------------- ADD ----------------
    parser_add = subparsers.add_parser(
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
    parser_add.set_defaults(func=task.add)

    # ---------------- UPDATE ----------------
    parser_update = subparsers.add_parser(
        "update",
        help="Update an existing task",
        description="Update task fields such as description, priority, status, or due date.",
    )
    parser_update.add_argument(
        "id",
        type=int,
        help="ID of the task to update",
    )
    parser_update.add_argument(
        "-d",
        "--description",
        type=str,
        help="New task description",
    )
    parser_update.add_argument(
        "-p",
        "--priority",
        type=str,
        choices=["low", "medium", "high"],
        help="Update task priority",
    )
    parser_update.add_argument(
        "-s",
        "--status",
        type=str,
        choices=["todo", "in-progress", "done"],
        help="Update task status",
    )
    parser_update.add_argument(
        "--due",
        type=str,
        help="Update due date/time (YYYY-MM-DD HH:MM)",
    )
    parser_update.set_defaults(func=task.update)

    # ---------------- DELETE ----------------
    parser_delete = subparsers.add_parser(
        "delete",
        help="Delete a task",
        description="Remove a task permanently using its ID.",
    )
    parser_delete.add_argument(
        "id",
        type=int,
        help="ID of the task to delete",
    )
    parser_delete.set_defaults(func=task.delete)

    # ---------------- LIST ----------------
    parser_list = subparsers.add_parser(
        "list",
        help="List tasks",
        description="List tasks filtered by status, priority, and sorting options.",
    )
    parser_list.add_argument(
        "tasks_type",
        type=str,
        choices=["in-progress", "todo", "done", "all"],
        default="all",
        nargs="*",
        help="Filter tasks by status (default: all)",
    )
    parser_list.add_argument(
        "-p",
        "--priority",
        type=str,
        choices=["low", "medium", "high"],
        help="Filter tasks by priority",
    )
    parser_list.add_argument(
        "-sb",
        "--sort-by",
        type=str,
        choices=["id", "created_at", "updated_at", "priority", "status"],
        default="id",
        help="Sort tasks by a specific field (default: id)",
    )
    parser_list.add_argument(
        "-o",
        "--order",
        type=str,
        choices=["asc", "desc"],
        default="asc",
        help="Sort order (default: asc)",
    )
    parser_list.set_defaults(func=task.list_tasks)

    # list_subparsers = parser_list.add_subparsers(
    #     dest="l2_subparser_list",
    #     description="More granular commands on top of list command",
    # )

    # parser_list_archived = list_subparsers.add_parser(
    #     "archived",
    #     help="List done tasks",
    #     description="List done / archived tasks",
    # )
    # parser_list_archived.add_argument(
    #     "tasks_type",
    #     type=str,
    #     choices=["in-progress", "todo", "done", "all"],
    #     default="all",
    #     nargs="?",
    #     help="Filter tasks by status (default: all)",
    # )
    # parser_list_archived.add_argument(
    #     "-p",
    #     "--priority",
    #     type=str,
    #     choices=["low", "medium", "high"],
    #     help="Filter tasks by priority",
    # )
    # parser_list_archived.add_argument(
    #     "-sb",
    #     "--sort-by",
    #     type=str,
    #     choices=["id", "created_at", "updated_at", "priority", "status"],
    #     default="id",
    #     help="Sort tasks by a specific field (default: id)",
    # )
    # parser_list_archived.add_argument(
    #     "-o",
    #     "--order",
    #     type=str,
    #     choices=["asc", "desc"],
    #     default="asc",
    #     help="Sort order (default: asc)",
    # )

    # parser_list_archived.set_defaults(func=task.list_tasks)

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

    # ---------------- MARK IN PROGRESS ----------------
    parser_mark_in_progress = subparsers.add_parser(
        "mark-in-progress",
        help="Mark a task as in-progress",
        description="Set task status to 'in-progress' using its ID.",
    )
    parser_mark_in_progress.add_argument(
        "id",
        help="ID of the task",
    )
    parser_mark_in_progress.set_defaults(func=task.mark_in_progress)

    # ---------------- CLEAR ----------------
    parser_clear = subparsers.add_parser(
        "clear",
        help="Clear tasks",
        description="Delete tasks by status or clear all tasks.",
    )
    parser_clear.add_argument(
        "tasks_type",
        type=str,
        choices=["in-progress", "todo", "done", "all"],
        default="all",
        nargs="?",
        help="Type of tasks to clear (default: all)",
    )
    parser_clear.set_defaults(func=task.clear_tasks)

    # ---------------- SEARCH ----------------
    parser_search = subparsers.add_parser(
        "search",
        help="Search tasks",
        description="Search tasks by keyword in the description.",
    )
    parser_search.add_argument(
        "keyword",
        type=str,
        help="Keyword to search for",
    )
    parser_search.set_defaults(func=task.search_tasks)

    # ---------------- GOOGLE CALENDAR ----------------
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

    args = parser.parse_args()
    print(args)

    result = args.func(args, tasks_file)

    # if args.l1_subparser == "mark-done":
    #     result = args.func(args, tasks_file, archived_file)
    # elif args.l1_subparser == "list" and args.l2_subparser_list == "archived":
    #     result = args.func(args, archived_file)
    # else:
    #     result = args.func(args, tasks_file)

    print(result)


if __name__ == "__main__":
    main()
