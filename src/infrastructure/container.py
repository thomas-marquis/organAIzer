from dependency_injector.providers import Singleton, Provider, Configuration
from dependency_injector.containers import DeclarativeContainer
from langchain.chat_models import BaseChatModel

from langchain_mistralai import ChatMistralAI

from .notion_repository import NotionNoteRepository
from .todoist_repository import TodoistTaskRepository

from src.domain import NoteRepository, TaskRepository


class InfrastructureContainer(DeclarativeContainer):
    config = Configuration()

    mistral_llm: Provider[BaseChatModel] = Singleton(
        ChatMistralAI,
        mistral_api_key=config.mistral.api_key.required(),
        model=config.mistral.model.required(),
        temperature=config.mistral.temperature,
    )

    notion: Provider[NoteRepository] = Singleton(
        NotionNoteRepository,
        api_key=config.notion.api_key.required(),
    )

    todoist: Provider[TaskRepository] = Singleton(
        TodoistTaskRepository,
        api_key=config.todoist.api_key.required(),
    )

