import argparse

from taskman.commands import (
    add_cmd,
    # delete_cmd,
    # list_cmd,
    # mark_cmd,
    # update_cmd,
)


def main():
    parser = argparse.ArgumentParser(
        prog="taskman",
        description="A Task Manager CLI",
    )
    subparser = parser.add_subparsers(dest="command", help="Available commands")

    add_cmd.register(subparser)
    # list_cmd.register(subparser)
    # update_cmd.register(subparser)
    # delete_cmd.register(subparser)
    # mark_cmd.register(subparser)

    args = parser.parse_args()

    if hasattr(args, "func"):
        result = args.func(args)
        if result:
            print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
