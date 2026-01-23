from argparse import ArgumentParser
from pathlib import Path

from taskman import task
from taskman.commands import (
    add_cmd,
    delete_cmd,
    list_cmd,
    mark_cmd,
    search_cmd,
    update_cmd,
)

taskman_dir = Path("~/taskman-test").expanduser().resolve()
tasks_file = taskman_dir / "tasks.json"
archived_file = taskman_dir / "archived.json"

taskman_dir.mkdir(parents=True, exist_ok=True)


def main():
    parser = ArgumentParser(
        prog="taskman",
        description="A simple CLI-based task manager with priorities, due dates, and Google Calendar integration.",
    )

    subparser = parser.add_subparsers(
        title="Commands",
        dest="l1_subparser",
        required=True,
        help="Available task management commands",
    )

    # ---------------- ADD ----------------
    add_cmd.register(subparser, task.add)

    # ---------------- UPDATE ----------------
    update_cmd.register(subparser, task.update)

    # ---------------- DELETE & CLEAR ----------------
    delete_cmd.register(subparser, task.delete)
    delete_cmd.register_clear(subparser, task.clear_tasks)

    # ---------------- LIST ----------------
    list_cmd.register(subparser, task.list_tasks)

    # ---------------- MARK ----------------
    mark_cmd.register_mark_in_progress(subparser, task.mark_in_progress)

    # ---------------- SEARCH ----------------
    search_cmd.register(subparser, task.search_tasks)

    args = parser.parse_args()
    result: str = args.func(args, tasks_file)

    print(result)


if __name__ == "__main__":
    main()
