from argparse import ArgumentParser
from pathlib import Path

from . import task

filename = Path('~/tasks.json').expanduser().resolve()


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('task', type=str)
    parser_add.set_defaults(func=task.add)

    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('id', type=int)
    parser_update.add_argument('new_desc', type=str)
    parser_update.set_defaults(func=task.update)

    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument('id')
    parser_delete.set_defaults(func=task.delete)

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('tasks_type', type=str, choices=['in-progress', 'todo', 'done', 'all'], default="all", nargs='?')
    parser_list.set_defaults(func=task.list_tasks)

    parser_mark_done = subparsers.add_parser('mark-done')
    parser_mark_done.add_argument('id')
    parser_mark_done.set_defaults(func=task.mark_done)

    parser_mark_in_progress = subparsers.add_parser('mark-in-progress')
    parser_mark_in_progress.add_argument('id')
    parser_mark_in_progress.set_defaults(func=task.mark_in_progress)

    parser_clear = subparsers.add_parser('clear')
    parser_clear.add_argument('tasks_type', type=str, choices=['in-progress', 'todo', 'done', 'all'], default="all", nargs='?')
    parser_clear.set_defaults(func=task.clear_tasks)

    args = parser.parse_args()
    result = args.func(args, filename)
    print(result)


if __name__ == "__main__":
    main()