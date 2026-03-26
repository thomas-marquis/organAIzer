from typing import Iterator, Final

from deepagents import create_deep_agent
from langchain_core.chat_models import BaseChatModel
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings

from src.agent.tools import get_todoist_structure_tree, get_tasks_by_project, search_notion_pages, \
    get_notion_page_content

main_prompt = """
You are an expert in personal organisation and performence.

You have access to your client todo list, note taking system, mails and calendar.

Your primary goal is to help him to get more oganized and efficient and to set priorites.
"""



class AgentImpl:
    def __init__(self, llm: BaseChatModel) -> None:
        self._llm: Final = llm
        self._agent: Final = create_deep_agent(
            model=self._llm,
            system_prompt=main_prompt,
            tools=[
                get_todoist_structure_tree,
                get_tasks_by_project,
                search_notion_pages,
                get_notion_page_content,
            ]
        )

    def run(self, message: str) -> Iterator[str]:
        for evt in self._agent.stream({
            "messages": [
                {"role": "user", "content": message},
            ],
        }):
            yield evt
        # return res["messages"][-1].content