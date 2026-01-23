def register(subparser, list_tasks):
    parser_list = subparser.add_parser(
        "list",
        help="List tasks",
        description="List tasks filtered by status, priority, and sorting options.",
    )
    parser_list.add_argument(
        "tasks_type",
        type=str,
        choices=["in-progress", "todo", "done", "all"],
        default="all",
        nargs="?",
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
    parser_list.set_defaults(func=list_tasks)


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
