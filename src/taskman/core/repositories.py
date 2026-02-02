import copy
from datetime import datetime

from pydantic import ValidationError

from taskman.config import settings
from taskman.core.models import Metadata, Task, TasksFile
from taskman.utils import TaskPriority, TaskStatus


class FileRepository:
    def __init__(self, filename: str):
        self.path = settings.database_path / filename
        self.tasks: list[Task] = []
        self.metadata: Metadata = Metadata(last_tid=0, n_tasks=0)
        self.__load_all()  # Load on init

    def __read_file(self):
        with self.path.open("r", encoding="utf-8") as f:
            json_str = f.read()
        if json_str == "":
            raise FileNotFoundError
        return json_str

    def __load_file(self) -> tuple[list[Task], Metadata]:
        try:
            json_str = self.__read_file()
            tasks_data: TasksFile = TasksFile.model_validate_json(json_str)
        except FileNotFoundError:
            return ([], Metadata(last_tid=0, n_tasks=0))
        except ValidationError as exc:
            print(f"Exception occured.\n{exc}")
        else:
            return tasks_data.tasks, tasks_data.metadata

    def __load_all(self):
        self.tasks, self.metadata = self.__load_file()

    def __save_file(self):
        tasks_data = TasksFile(tasks=self.tasks, metadata=self.metadata)
        json_str = tasks_data.model_dump_json(indent=2)
        with self.path.open("w", encoding="utf-8") as f:
            f.write(json_str)

    def _add_task_in_file(self, task: Task) -> int:
        self.tasks.append(task)
        self.metadata.last_tid = task.id
        self.metadata.n_tasks += 1
        self.__save_file()
        return task.id

    def add_task(
        self,
        description: str | None = None,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        due_at: datetime | None = None,
        task: Task | None = None,
    ) -> int:
        task_data = [description, status, priority, due_at]
        if task and any(task_data):
            raise ValueError(
                "task bhi de diya, aur naya task banane ke liye information bhi. \
                dono me se ek hi de sakte ho",
            )
        if task:
            return self._add_task_in_file(task)

        tid = self.metadata.last_tid + 1
        new_task = Task(
            id=tid,
            description=description,
            status=status,
            priority=priority,
            due_at=due_at,
        )
        return self._add_task_in_file(new_task)

    def __get_tidx(self, tid: int) -> int | None:
        return next((idx for idx, t in enumerate(self.tasks) if t.id == tid), None)

    def get_task_by_tid(self, tid) -> Task | None:
        return next((t for t in self.tasks if t.id == tid), None)

    def get_all_tasks(self) -> list[Task]:
        return copy.deepcopy(self.tasks)

    def update_task(self, tid, update_data) -> int | None:
        tidx = self.__get_tidx(tid)

        if tidx is None:
            return None

        task = self.tasks[tidx]
        self.tasks[tidx] = task.model_copy(update=update_data)

        self.__save_file()
        return tid

    def delete_task_by_tid(self, tid) -> int | None:
        tidx = self.__get_tidx(tid)
        if tidx is None:
            return None

        del self.tasks[tidx]

        if self.metadata.last_tid == tid:
            self.metadata.last_tid -= 1
        self.metadata.n_tasks -= 1

        self.__save_file()
        return tid

    def delete_multiple_by_task_status(self, status_filter: TaskStatus) -> int | None:
        if len(self.tid_s) == 0:
            return None

        filtered = [task for task in self.tasks if task.status != status_filter]

        n_deleted = len(self.tid_s) - len(filtered)

        self.tasks = filtered
        self.metadata.n_tasks = len(filtered)
        self.metadata.last_tid = filtered[-1].tid if len(filtered) > 0 else 0
        self.__save_file()
        return n_deleted

    def delete_all(self):
        self.tasks = []
        self.metadata.n_tasks = 0
        self.metadata.last_tid = 0
        self.__save_file()
        return len(self.tid_s)

    def search_tasks(self, keyword: str) -> list[Task]:
        if len(self.tid_s) == 0:
            return []

        keyword = keyword.lower()

        return [task for task in self.tasks if keyword in task.description.lower()]
