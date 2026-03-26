from abc import ABC, abstractmethod

from .entities.note import Note
from .entities.tasks import Task, TaskList


class TaskRepository(ABC):
    @abstractmethod
    async def get_all_task_lists(self) -> list[TaskList]:
        raise NotImplementedError()

    @abstractmethod
    async def get_task_list_by_id(self, list_id: str) -> TaskList:
        raise NotImplementedError()

    @abstractmethod
    async def list_tasks_by_list_id(self, list_id: str) -> list[Task]:
        raise NotImplementedError()

    @abstractmethod
    async def get_task_by_id(self, task_id: str) -> Task | None:
        raise NotImplementedError()


class NoteRepository(ABC):
    """Abstract base class for note repositories"""

    @abstractmethod
    async def search_notes(self, query: str, limit: int = 10) -> list[Note]:
        pass

    @abstractmethod
    async def get_note_by_id(self, note_id: str) -> Note | None:
        pass

    @abstractmethod
    async def get_all_notes(self) -> list[Note]:
        pass
