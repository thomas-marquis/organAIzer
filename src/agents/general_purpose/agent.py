from typing import Final, AsyncIterator

from deepagents import create_deep_agent
from langchain.chat_models import BaseChatModel

from src.domain import TasksService, TaskRepository, NoteRepository
from .tools import get_tasks_by_todolist, search_notes, \
    get_note_content, get_todolists_structure_tree, ToolContext

main_prompt = """
You are an expert in personal organisation and performance.

You have access to your client todo list, note taking system, mails and calendar.

Your primary goal is to help him to get more organized and efficient and to set priorities.
"""


class GPAgent:
    def __init__(self, llm: BaseChatModel, task_service: TasksService, task_repository: TaskRepository,
                 note_repository: NoteRepository) -> None:
        self._llm: Final = llm
        self._task_service: Final = task_service
        self._task_repository: Final = task_repository
        self._note_repository: Final = note_repository
        self._agent: Final = create_deep_agent(
            model=self._llm,
            system_prompt=main_prompt,
            tools=[
                get_todolists_structure_tree,
                get_tasks_by_todolist,
                search_notes,
                get_note_content,
            ],
        )

    async def run(self, message: str) -> AsyncIterator[str]:
        async for evt in self._agent.astream({
            "messages": [
                {"role": "user", "content": message},
            ],
        }, context=ToolContext(task_service=self._task_service, task_repository=self._task_repository,
                               note_repository=self._note_repository)):
            yield evt
        # return res["messages"][-1].content
