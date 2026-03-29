from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Dependency, Provider

from src.agents.general_purpose import GPAgent


class ControllerContainer(DeclarativeContainer):
    config = Configuration()

    general_purpose_agent: Provider[GPAgent] = Dependency(instance_of=GPAgent)