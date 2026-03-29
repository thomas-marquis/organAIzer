from abc import ABC, abstractmethod

from .entities.note import Note, NoteContent
from .entities.tasks import Task, Todolist, TaskLabel


class TaskRepository(ABC):
    @abstractmethod
    async def get_all_todolists(self) -> list[Todolist]:
        """Returns all the first-level task lists. each one can contains nested lists."""
        raise NotImplementedError()

    @abstractmethod
    async def get_todolist_by_id(self, list_id: str) -> Todolist:
        """Returns a task list by its ID"""
        raise NotImplementedError()

    @abstractmethod
    async def list_tasks_by_todolist_id(self, list_id: str) -> list[Task]:
        """Returns all tasks in a task list"""
        raise NotImplementedError()

    @abstractmethod
    async def get_task_by_id(self, task_id: str) -> Task | None:
        """Returns a task by its ID"""
        raise NotImplementedError()

    @abstractmethod
    async def get_all_labels(self) -> list[TaskLabel]:
        """Returns all labels that exist."""
        raise NotImplementedError()


class NoteRepository(ABC):
    @abstractmethod
    async def search_notes(self, query: str, limit: int = 10) -> list[Note]:
        raise NotImplementedError()

    @abstractmethod
    async def get_note_by_id(self, note_id: str) -> Note | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_note_content(self, note_id: str) -> NoteContent:
        raise NotImplementedError()
