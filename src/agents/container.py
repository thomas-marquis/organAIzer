from dependency_injector.providers import Singleton, Provider, Dependency
from dependency_injector.containers import DeclarativeContainer
from langchain.chat_models import BaseChatModel

from .general_purpose import GPAgent
from src.domain import TasksService, TaskRepository


class AgentContainer(DeclarativeContainer):
    llm: Provider[BaseChatModel] = Dependency(instance_of=BaseChatModel)

    task_service: Provider[TasksService] = Dependency(instance_of=TasksService)
    task_repository: Provider[TaskRepository] = Dependency(instance_of=TaskRepository)

    general_purpose_agent: Provider[GPAgent] = Singleton(
        GPAgent,
        llm=llm,
        task_service=task_service,
        task_repository=task_repository,
    )