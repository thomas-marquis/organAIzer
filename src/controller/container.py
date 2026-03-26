from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Dependency, Provider

from src.agent import Agent


class ControllerContainer(DeclarativeContainer):
    config = Configuration()

    agent: Provider[Agent] = Dependency(instance_of=Agent)