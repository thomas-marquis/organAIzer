from datetime import datetime
from typing import Final

from notion_client import AsyncClient

from src.common import get_logger
from ..domain import Note, NoteRepository, NoteContent

logger = get_logger()


class NotionNoteRepository(NoteRepository):
    def __init__(self, api_key: str) -> None:
        self._client: Final = AsyncClient(auth=api_key)

    async def search_notes(self, query: str, limit: int = 10) -> list[Note]:
        try:
            response = await self._client.search(
                query=query,
                page_size=limit,
                filter={"property": "object", "value": "page"}
            )

            notes = []
            for page in response["results"]:
                note = self._convert_notion_page(page)
                # Get the content for each note
                note.content = self._get_page_content(page["id"])
                notes.append(note)

            return notes
        except Exception as e:
            logger.error(f"Error searching notes: {e}")
            return []

    async def get_note_by_id(self, note_id: str) -> Note | None:
        try:
            page = await self._client.pages.retrieve(page_id=note_id)
            note = self._convert_notion_page(page)
            note.content = self._get_page_content(note_id)
            return note
        except Exception as e:
            logger.error(f"Error getting note by ID: {e}")
            return None

    async def get_note_content(self, note_id: str) -> NoteContent:
        pass

    def _map_page_to_note(self, page: dict) -> Note:
        """Convert Notion page to domain Note entity"""
        return Note(
            id_=page["id"],
            title=self._extract_title(page["properties"]),
            created_at=datetime.fromisoformat(page["created_time"]),
            updated_at=datetime.fromisoformat(page["last_edited_time"]),
            tags=self._extract_tags(page["properties"])
        )

    def _get_page_content(self, page_id: str) -> str:
        """Get the content of a Notion page in markdown format"""
        try:
            blocks = self._client.blocks.children.list(block_id=page_id)
            content_parts = []

            for block in blocks["results"]:
                content_parts.append(self._block_to_markdown(block))

            return "\n".join(content_parts)
        except Exception as e:
            logger.error(f"Error getting page content: {e}")
            return ""

    @staticmethod
    def _block_to_markdown(block: dict) -> str:
        """Convert Notion block to markdown"""
        block_type = block["type"]

        match block_type:
            case "paragraph":
                text = ""
                for rich_text in block["paragraph"]["rich_text"]:
                    text += rich_text["text"]["content"]
                return text

            case "heading_1":
                text = ""
                for rich_text in block["heading_1"]["rich_text"]:
                    text += rich_text["text"]["content"]
                return f"# {text}"

            case "heading_2":
                text = ""
                for rich_text in block["heading_2"]["rich_text"]:
                    text += rich_text["text"]["content"]
                return f"## {text}"

            case "heading_3":
                text = ""
                for rich_text in block["heading_3"]["rich_text"]:
                    text += rich_text["text"]["content"]
                return f"### {text}"

            case "bulleted_list_item":
                text = ""
                for rich_text in block["bulleted_list_item"]["rich_text"]:
                    text += rich_text["text"]["content"]
                return f"- {text}"

            case "numbered_list_item":
                text = ""
                for rich_text in block["numbered_list_item"]["rich_text"]:
                    text += rich_text["text"]["content"]
                return f"1. {text}"

            case "to_do":
                text = ""
                for rich_text in block["to_do"]["rich_text"]:
                    text += rich_text["text"]["content"]
                checked = "x" if block["to_do"]["checked"] else " "
                return f"- [{checked}] {text}"

            case _:
                return ""

    @staticmethod
    def _extract_title(properties: dict) -> str:
        """Extract title from Notion page properties"""
        for prop_name, prop_data in properties.items():
            if prop_data["type"] == "title":
                if prop_data["title"]:
                    return prop_data["title"][0]["text"]["content"]
        return "Untitled"

    @staticmethod
    def _extract_tags(properties: dict) -> list[str]:
        """Extract tags from Notion page properties"""
        tags: list[str] = []
        for prop_name, prop_data in properties.items():
            match prop_data:
                case {"type": "multi_select", "multi_select": items}:
                    tags.extend([option["name"] for option in items])
                case _ if prop_name.lower() == "tags" and prop_data.get("type") == "rich_text":
                    tags.extend([text["text"]["content"] for text in prop_data["rich_text"] if text.get("text")])
        return tags
