from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Provider, Dependency

from .services.tasks import TasksService
from .repositories import TaskRepository

class DomainContainer(DeclarativeContainer):
    task_repository: Provider[TaskRepository] = Dependency(instance_of=TaskRepository)

    task_service: Provider[TasksService] = Singleton(TasksService, task_repository=task_repository)