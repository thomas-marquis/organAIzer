import asyncio
from typing import Final, Coroutine, Any

from ..repositories import TaskRepository
from ..entities.tasks import Task, Todolist
from ..exceptions import InvalidInputError

class TasksService:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository: Final = task_repository

    async def get_tasks_from_todolist(self, todolist: Todolist, recursive: bool = False, include_archived: bool = False) -> list[Task]:
        if not include_archived and todolist.archived:
            raise InvalidInputError("Cannot search archived task lists")

        tasks = await self._task_repository.list_tasks_by_todolist_id(todolist.id)
        if not recursive:
            return tasks

        coros: list[Coroutine[Any, Any, list[Task]]] = []
        for sub_list in todolist.sub_todolists:
            if not include_archived and sub_list.archived:
                continue
            coros.append(self.get_tasks(sub_list, recursive=True, include_archived=include_archived))

        task_batches = await asyncio.gather(*coros)
        return [task for batch in task_batches for task in batch if include_archived and task.archived]