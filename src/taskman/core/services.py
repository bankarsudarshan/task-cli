from datetime import datetime

from taskman.core.repositories import FileRepository
from taskman.utils import TaskPriority, TaskStatus


class CLIService:
    def __init__(self, repo: FileRepository, archive_repo: FileRepository):
        self.repo: FileRepository = repo
        self.archive_repo: FileRepository = archive_repo

    def add(self, description: str, status: str, priority: str, due_at: str) -> str:
        tid = self.repo.add_task(
            description=description,
            status=status,
            priority=priority,
            due_at=due_at,
        )
        return tid

    def update(
        self,
        tid: int,
        description: str,
        priority: str,
        status: str,
        due_at: str,
    ) -> str:
        if not tid:
            return None
        if not any([description, priority, status, due_at]):
            return None

        updates: dict = {}
        if description is not None:
            updates["description"] = description
        if priority is not None:
            updates["priority"] = TaskPriority(priority.lower())
        if status is not None:
            updates["status"] = TaskStatus(status.lower())
        if due_at is not None:
            updates["due_at"] = datetime.strptime(due_at, "%Y-%m-%d %H:%M")  # noqa: DTZ007
        updates["updated_at"] = datetime.now()  # noqa: DTZ005

        return self.repo.update_task(tid, updates)

    def delete(self, tid: int) -> int | None:
        return self.repo.delete_task_by_tid(tid)

    def get_tasks(self, filters: dict):
        tasks = self.repo.get_all_tasks()
        if len(tasks) == 0:
            return []

        filtered = []
        for task_pydantic_model in tasks:
            task = task_pydantic_model.model_dump()

            # filter by status
            if (
                filters["tasks_type"] != "all"
                and filters["tasks_type"] != task["status"]
            ):
                continue

            # filter by priority if requested
            if (
                filters["priority"] is not None
                and filters["priority"] != task["priority"]
            ):
                continue

            filtered.append(task)

        if len(filtered) != 0:
            # sorting
            field: str = filters["sort_by"]
            reverse: bool = filters["order"] == "desc"
            if field == "priority":
                priority_order = {"high": 0, "medium": 1, "low": 2}
                filtered.sort(
                    key=lambda t: priority_order.get(t.get("priority"), 3),
                    reverse=reverse,
                )
            elif field == "status":
                status_order = {"todo": 0, "in-progress": 1, "done": 2}
                filtered.sort(
                    key=lambda t: status_order.get(t.get("status"), 3),
                    reverse=reverse,
                )
            elif field in ("updated_at", "due_at"):
                tasks_with_field = [task for task in filtered if task.get(field)]
                tasks_with_field.sort(key=lambda t: t.get(field), reverse=reverse)
                tasks_without_field = [task for task in filtered if not task.get(field)]
                filtered = tasks_with_field + tasks_without_field

            else:
                filtered.sort(
                    key=lambda t: t.get(filters["sort_by"], ""),
                    reverse=reverse,
                )

        return filtered

    def __mark_done(self, tid: int) -> int | None:
        task = self.repo.get_task_by_tid(tid)
        print(f"task to be marked retrieved - {task}")
        if not task:
            return None

        self.repo.delete_task_by_tid(tid)
        task.status = TaskStatus.DONE
        task.updated_at = datetime.now()  # noqa: DTZ005
        return self.archive_repo.add_task(task=task)

    def __mark_in_progress(self, tid: int) -> int | None:
        return self.repo.update_task(tid, {"status": TaskStatus.IN_PROGRESS})

    def mark(self, tid: int, status: str) -> int | None:
        if status == "done":
            return self.__mark_done(tid)
        return self.__mark_in_progress(tid)

    def clear_tasks(self, task_status: str):
        if task_status == "all":
            return self.repo.delete_all()

        return self.repo.delete_multiple_by_task_status(task_status)

    def search_tasks(self, keyword):
        matches = self.repo.search_tasks(keyword)
        if not matches:
            return None

        return matches, len(matches)
