from typing import Iterator

from deepagents import create_deep_agent
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings

from src.agent.tools import get_todoist_structure_tree, get_tasks_by_project, search_notion_pages, \
    get_notion_page_content

main_prompt = """
You are an expert in personal organisation and performence.

You have access to your client todo list, note taking system, mails and calendar.

Your primary goal is to help him to get more oganized and efficient and to set priorites.
"""



class Agent:
    def __init__(self, mistral_api_key: str) -> None:
        self._llm = ChatMistralAI(
            mistral_api_key=mistral_api_key,
            model="mistral-large-latest",
            temperature=0.1,
        )
        self._agent = create_deep_agent(
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