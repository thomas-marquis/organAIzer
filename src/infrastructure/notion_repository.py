from typing import Final

from notion_client import AsyncClient

from src.common import get_logger
from src.domain import Note, NoteRepository, NoteContent
from .notion_mappers import map_notion_page_to_note
from .notion_renderers import NotionBlockRenderer
from .notion_types import NotionBlock

logger = get_logger()


class NotionNoteRepository(NoteRepository):
    def __init__(self, api_key: str) -> None:
        self._client: Final = AsyncClient(auth=api_key)
        self._renderer: Final = NotionBlockRenderer(api_key)

    async def search_notes(self, query: str, limit: int = 10) -> list[Note]:
        try:
            response = await self._client.search(
                query=query,
                page_size=limit,
                filter={"property": "object", "value": "page"}
            )

            return [map_notion_page_to_note(page) for page in response["results"]]
        except Exception as e:
            logger.error(f"Error searching notes: {e}")
            return []

    async def get_note_by_id(self, note_id: str) -> Note | None:
        try:
            page = await self._client.pages.retrieve(page_id=note_id)
            return map_notion_page_to_note(page)
        except Exception as e:
            logger.error(f"Error getting note by ID: {e}")
            return None

    async def get_note_content(self, note_id: str) -> NoteContent:
        try:
            blocks = await self._fetch_all_blocks(note_id)
            rendered_parts = []
            for block in blocks:
                rendered_parts.append(await self._renderer.render(block))

            return NoteContent(note_id=note_id, markdown="\n\n".join(rendered_parts))
        except Exception as e:
            logger.error(f"Error getting note content: {e}")
            return NoteContent(note_id=note_id, markdown="")

    async def _fetch_all_blocks(self, block_id: str) -> list[NotionBlock]:
        """Fetch all blocks for a given block ID, handling pagination"""
        blocks: list[NotionBlock] = []
        cursor: str | None = None
        while True:
            response = await self._client.blocks.children.list(
                block_id=block_id,
                start_cursor=cursor
            )
            blocks.extend(response["results"])
            if not response["has_more"]:
                break
            cursor = response["next_cursor"]
        return blocks
