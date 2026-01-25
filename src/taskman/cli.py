import argparse

from taskman.commands import (
    add_cmd,
    delete_cmd,
    list_cmd,
    mark_cmd,
    update_cmd,
)
from taskman.core.repositories import FileRepository
from taskman.core.services import CLIService


def main():
    tasks_file = "tasks.json"
    archives_file = "archived.json"

    repo = FileRepository(tasks_file)
    archive_repo = FileRepository(archives_file)

    service = CLIService(repo, archive_repo)

    parser = argparse.ArgumentParser(
        prog="taskman",
        description="A Task Manager CLI",
    )
    subparser = parser.add_subparsers(dest="command", help="Available commands")

    add_cmd.register(subparser, service)
    list_cmd.register(subparser, service)
    update_cmd.register(subparser, service)
    delete_cmd.register(subparser, service)
    mark_cmd.register(subparser, service)

    args = parser.parse_args()

    if hasattr(args, "func"):
        result = args.func(args)
        if result:
            print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
