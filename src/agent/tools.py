import os
from functools import lru_cache

from notion_client import Client
from todoist_api_python.api import TodoistAPI


@lru_cache
def notion_client() -> Client:
    return Client(auth=os.environ["NOTION_TOKEN"])


@lru_cache
def todoist_client() -> TodoistAPI:
    return TodoistAPI(os.environ["TODOIST_TOKEN"])


def get_todoist_structure_tree() -> dict:
    """
    Get the list of the projects in Todoist and all the labels defined by the user.
    """

    todoist = todoist_client()

    projects_paginator = todoist.get_projects()
    projects = [p for page in projects_paginator for p in page]
    nodes = {p.id: {"id": p.id, "name": p.name, "children": []} for p in projects}

    root = {"id": "root", "name": "/", "children": []}

    labels = todoist.get_labels(limit=100)

    # Link nodes to their parents
    for p in projects:
        node = nodes[p.id]
        match p.parent_id:
            case str(parent_id) if parent_id in nodes:
                nodes[parent_id]["children"].append(node)
            case str(_) | None:
                root["children"].append(node)

    return {
        "projects_tree": root,
        "labels": [label.name for label in list(labels)[0]],
    }


def get_tasks_by_project(project_id: str) -> list[dict]:
    """Returns a list of tasks in a project."""
    todoist = todoist_client()
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
    notion = notion_client()
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


class SearchNotesTool:
    def __init__(self):
        pass

    def __call__(self):
        pass
