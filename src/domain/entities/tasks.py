from __future__ import annotations

from dataclasses import dataclass, field
import datetime as dt

from ..exceptions import NotFoundError, InvalidInputError

@dataclass
class Task:
    id_: str
    title: str
    description: str
    created_at: dt.datetime
    due_date: dt.datetime | None = None
    labels: list[str] = field(default_factory=list)
    completed: bool = False

@dataclass
class TaskList:
    id_: str
    name: str
    # tasks: list[Task] = field(default_factory=list)
    sub_lists: list[TaskList] = field(default_factory=list)
    archived: bool = False

    # def get_by_id(self, task_id: str, recursive: bool = False, include_archived: bool = False) -> Task:
    #     if not include_archived and self.archived:
    #         raise InvalidInputError("Cannot search archived task lists")
    #
    #     if not recursive:
    #         for task in self.tasks:
    #             if task.id_ == task_id:
    #                 return task
    #     else:
    #         for sub_list in self.sub_lists:
    #             if not include_archived and sub_list.archived:
    #                 continue
    #             try:
    #                 return sub_list.get_by_id(task_id, recursive=True, include_archived=include_archived)
    #             except NotFoundError:
    #                 pass
    #     raise NotFoundError(f"Task with id {task_id} not found")