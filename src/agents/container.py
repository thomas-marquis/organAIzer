from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Provider, Dependency
from langchain.chat_models import BaseChatModel

from src.domain import TasksService, TaskRepository, NoteRepository
from .general_purpose import GPAgent


class AgentContainer(DeclarativeContainer):
    llm: Provider[BaseChatModel] = Dependency(instance_of=BaseChatModel)  # type: ignore[type-abstract]

    task_service: Provider[TasksService] = Dependency(instance_of=TasksService)
    task_repository: Provider[TaskRepository] = Dependency(instance_of=TaskRepository)  # type: ignore[type-abstract]
    note_repository: Provider[NoteRepository] = Dependency(instance_of=NoteRepository)  # type: ignore[type-abstract]

    general_purpose_agent: Provider[GPAgent] = Singleton(
        GPAgent,
        llm=llm,
        task_service=task_service,
        task_repository=task_repository,
        note_repository=note_repository,
    )
