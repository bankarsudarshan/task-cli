def register(subparser, search_tasks):
    parser_search = subparser.add_parser(
        "search",
        help="Search tasks",
        description="Search tasks by keyword in the description.",
    )
    parser_search.add_argument(
        "keyword",
        type=str,
        help="Keyword to search for",
    )
    parser_search.set_defaults(func=search_tasks)
