from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from taskman.utils import TaskPriority, TaskStatus


class Task(BaseModel):
    id: int = -1
    description: str
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    due_at: datetime | None = None


class Metadata(BaseModel):
    last_tid: Annotated[int, Field(ge=0)]
    n_tasks: Annotated[int, Field(ge=0)]


class TasksFile(BaseModel):
    tasks: list[Task]
    metadata: Metadata
