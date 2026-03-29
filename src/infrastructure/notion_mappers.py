from datetime import datetime
from typing import Any

from src.domain.entities.note import Note
from .notion_types import NotionPage


def map_notion_page_to_note(page: NotionPage) -> Note:
    """Convert Notion page to domain Note entity"""
    properties = page["properties"]

    return Note(
        id_=page["id"],
        title=extract_title(properties),
        created_at=datetime.fromisoformat(page["created_time"].replace("Z", "+00:00")),
        updated_at=datetime.fromisoformat(page["last_edited_time"].replace("Z", "+00:00")),
        tags=extract_tags(properties)
    )


def extract_title(properties: dict[str, Any]) -> str:
    """Extract title from Notion page properties"""
    for prop_data in properties.values():
        if prop_data["type"] == "title":
            title_list = prop_data.get("title", [])
            if title_list:
                return "".join([rt["plain_text"] for rt in title_list])
    return "Untitled"


def extract_tags(properties: dict[str, Any]) -> list[str]:
    """Extract tags from Notion page properties
    
    The tag keeps track of the original source property (e.g. "prop_name=value").
    """
    tags: list[str] = []
    for prop_name, prop_data in properties.items():
        prop_type = prop_data["type"]

        match prop_type:
            case "multi_select":
                for item in prop_data["multi_select"]:
                    tags.append(f"{prop_name}={item['name']}")
            case "select":
                select_item = prop_data.get("select")
                if select_item:
                    tags.append(f"{prop_name}={select_item['name']}")
            case "status":
                status_item = prop_data.get("status")
                if status_item:
                    tags.append(f"{prop_name}={status_item['name']}")
            case "checkbox":
                tags.append(f"{prop_name}={prop_data['checkbox']}")
            case "people":
                for person in prop_data["people"]:
                    name = person.get("name")
                    if name:
                        tags.append(f"{prop_name}={name}")
            case "rich_text":
                if prop_name.lower() == "tags":
                    for rt in prop_data["rich_text"]:
                        tags.append(rt["plain_text"])
                else:
                    text = "".join([rt["plain_text"] for rt in prop_data["rich_text"]])
                    if text:
                        tags.append(f"{prop_name}={text}")
            case "created_by":
                user = prop_data.get("created_by")
                if user and "name" in user:
                    tags.append(f"{prop_name}={user['name']}")
            case "last_edited_by":
                user = prop_data.get("last_edited_by")
                if user and "name" in user:
                    tags.append(f"{prop_name}={user['name']}")

    return tags
