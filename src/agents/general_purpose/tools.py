import asyncio
from dataclasses import dataclass

from langchain.tools import tool, ToolRuntime

from src.common import get_logger
from src.domain import NoteRepository, TaskRepository, TasksService
from . import renderers

logger = get_logger()


@dataclass
class ToolContext:
    note_repository: NoteRepository
    task_repository: TaskRepository
    task_service: TasksService


@tool(parse_docstring=True)
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

    return f"## Lists structure:\n{renderers.render_todolists(lists)}\n\n## Labels:\n{renderers.render_task_labels(labels)}"


@tool(parse_docstring=True)
async def get_tasks_by_todolist(
        runtime: ToolRuntime[ToolContext], todolist_id: str, recursive: bool = False,
) -> str:
    """Returns all the tasks contained in a todolist.

    The parameter `recursive` controls whether to include sub-todolists tasks or not.

    Args:
        todolist_id: The ID of the todolist to retrieve tasks from.
        recursive: Whether to include tasks from sub-todolists or not.
    """

    todolist = await runtime.context.task_repository.get_todolist_by_id(todolist_id)
    tasks = await runtime.context.task_service.get_tasks_from_todolist(todolist, recursive=recursive)
    return renderers.render_tasks(tasks)


@tool(parse_docstring=True)
async def get_note_content(runtime: ToolRuntime[ToolContext], note_id: str) -> str:
    """Returns the content of a note page in Markdown.

    Args:
        note_id: The ID of the note to retrieve content from.
    """

    content = await runtime.context.note_repository.get_note_content(note_id)
    return renderers.render_note_content(content)


@tool(parse_docstring=True)
async def search_notes(runtime: ToolRuntime[ToolContext], query: str, max_pages: int = 10) -> str:
    """Search for user's notes.


    A note is usually a Markdown document a user may write for himself/herself about miscellaneous topics.
    Call this tool multiple times with different queries to get different results.
    This function doesn't return the note Markdown content, only the metadata (among with, the note's title and ID).
    Call the tool `get_note_content` to get the content.

    Args:
        query: a few keywords to search for.
        max_pages: The maximum number of pages to return. Defaults to 10.
    """

    notes = await runtime.context.note_repository.search_notes(query, max_pages)
    return renderers.render_notes(notes)
