import asyncio
import os
from functools import lru_cache

from notion_client import Client
from todoist_api_python.api import TodoistAPI


from langchain.tools import tool, ToolRuntime

from dataclasses import dataclass
from src.domain import NoteRepository, TaskRepository, Task, TasksService
from src.common import get_logger
from . import renderers

logger = get_logger()



@dataclass
class ToolContext:
    note_repository: NoteRepository
    task_repository: TaskRepository
    task_service: TasksService


@tool
async def get_todolists_structure_tree(runtime: ToolRuntime[ToolContext]) -> str:
    """
    Return the structure of the user's todolists.
    A user may create multiple nested todolists, each one can contain both tasks and sub-lists.
    This tool returns only the list tree structure, not the tasks.
    Use the tool `get_tasks_from_list` to get the tasks for a specific list.
    """

    try:
        lists, labels = await asyncio.gather(
            runtime.context.task_repository.get_all_todolists(),
            runtime.context.task_repository.get_all_labels(),
        )
    except Exception as e:
        logger.error(e)
        return f"Error during tool execution: {e}"

    return f"## Lists structure:\n{renderers.render_task_lists(lists)}\n\n## Labels:\n{renderers.render_task_labels(labels)}"



def get_tasks_by_todolist(project_id: str, recursive: bool = False) -> list[Task]:
    """Returns all the tasks contained in a todolist.

    The parameter `recursive` controls whether to include sub-todolists tasks or not.
    """

    tasks = todoist.get_tasks(project_id=project_id)
    tasks = [
        {
            "title": task.content,
            "labels": task.labels,
        }
        for task
        in list(tasks)[0]]
    return tasks


def _read_content(content_data: dict) -> str:
    match content_data["type"]:
        case "text":
            return content_data["text"]["content"]
        case "equation":
            return content_data["equation"]["expression"]
        case "link_preview":
            return content_data["link_preview"]["url"]
        case "file":
            return content_data["file"]["url"]
        case "image":
            return content_data["image"]["url"]
        case "mention":
            mention_data = content_data["mention"]
            title = mention_data.get("title", "Link")
            href = mention_data.get("href", "#")
            description = mention_data.get("description", "")
            if description:
                title = f"{title} ({description})"
            return f"[{title}]({href})"


def _extract_from_rich_text(block_data: dict) -> str:
    rich_text = block_data["rich_text"]
    if not rich_text:
        return ""
    return "\n".join([_read_content(text_content) for text_content in rich_text])


def _get_block_content(block: dict) -> str:
    match block["type"]:
        case "paragraph":
            return _extract_from_rich_text(block["paragraph"])
        case "heading_1":
            return f"# {_extract_from_rich_text(block["heading_1"])}"
        case "heading_2":
            return f"## {_extract_from_rich_text(block['heading_2'])}"
        case "heading_3":
            return f"### {_extract_from_rich_text(block['heading_3'])}"
        case "bulleted_list_item":
            return f"- {_extract_from_rich_text(block['bulleted_list_item'])}"
        case "numbered_list_item":
            return block["numbered_list_item"]["text"][0]["plain_text"]
        case "to_do":
            return block["to_do"]["text"][0]["plain_text"]
    return ""


def get_notion_page_content(page_id: str) -> str:
    """Returns the content of a Notion page in Markdown."""
    notion = notion_client()
    response = notion.blocks.children.list(block_id=page_id)
    contents = [_get_block_content(block) for block in response["results"]]
    return "\n".join(contents)


def _get_title(properties: dict) -> str:
    try:
        for prop_name, prop_data in properties.items():
            if prop_data["type"] == "title":
                return prop_data["title"][0]["text"]["content"]
    except KeyError as e:
        print(f"No title found: KeyError({e})")
    return ""


def search_notion_pages(query: str, max_pages: int = 10) -> list[dict]:
    """Returns a list of pages matching the query."""
    response = notion.search(
        query=query,
        page_size=max_pages,
        filter={
            "property": "object",
            "value": "page",
        },
        sort={
            "timestamp": "last_edited_time",
            "direction": "descending",
        },
    )
    results = response["results"]
    return [
        {
            "page_id": res["id"],
            "created_at": res["created_time"],
            "updated_at": res["last_edited_time"],
            "title": _get_title(res["properties"]),
        }
        for res
        in results
    ]
