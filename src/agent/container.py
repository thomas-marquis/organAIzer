from dependency_injector.providers import Singleton, Provider, Dependency
from dependency_injector.containers import DeclarativeContainer
from langchain.chat_models import BaseChatModel

from .agent import Agent


class AgentContainer(DeclarativeContainer):
    llm: Provider[BaseChatModel] = Dependency(instance_of=BaseChatModel)

    agent: Provider[Agent] =Singleton(
        Agent,
        llm=llm,
    )