import pytest
from typing import Any
from unittest.mock import AsyncMock

from src.infrastructure.notion_renderers import NotionBlockRenderer


def _base_block(block_type: str) -> Any:
    return {
        "object": "block",
        "id": "123",
        "created_time": "2021-03-16T16:36:00.000Z",
        "last_edited_time": "2021-03-16T16:36:00.000Z",
        "parent": {"type": "page_id", "page_id": "456"},
        "has_children": False,
        "in_trash": False,
        "type": block_type,
    }


@pytest.mark.asyncio
async def test_render_paragraph_complex() -> None:
    # Given
    block: Any = {
        **_base_block("paragraph"),
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "Normal ", "link": None},
                    "plain_text": "Normal ",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": "bold", "link": None},
                    "plain_text": "bold",
                    "annotations": {"bold": True}
                },
                {
                    "type": "text",
                    "text": {"content": "link", "link": {"url": "https://example.com"}},
                    "plain_text": "link",
                    "annotations": {}
                }
            ],
            "color": "default"
        }
    }
    renderer = NotionBlockRenderer("fake_key")

    # When
    result = await renderer.render(block)

    # Then
    assert result == "Normal **bold**[link](https://example.com)"


@pytest.mark.asyncio
async def test_render_headings() -> None:
    h1: Any = {
        **_base_block("heading_1"),
        "heading_1": {"rich_text": [
            {"type": "text", "text": {"content": "Title", "link": None}, "plain_text": "Title", "annotations": {}}],
            "color": "default", "is_toggleable": False}
    }
    h2: Any = {
        **_base_block("heading_2"),
        "heading_2": {"rich_text": [
            {"type": "text", "text": {"content": "Subtitle", "link": None}, "plain_text": "Subtitle",
             "annotations": {}}], "color": "default", "is_toggleable": False}
    }
    h3: Any = {
        **_base_block("heading_3"),
        "heading_3": {"rich_text": [
            {"type": "text", "text": {"content": "Section", "link": None}, "plain_text": "Section", "annotations": {}}],
            "color": "default", "is_toggleable": False}
    }

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(h1) == "# Title"
    assert await renderer.render(h2) == "## Subtitle"
    assert await renderer.render(h3) == "### Section"


@pytest.mark.asyncio
async def test_render_lists() -> None:
    bullet: Any = {
        **_base_block("bulleted_list_item"),
        "bulleted_list_item": {"rich_text": [
            {"type": "text", "text": {"content": "Item", "link": None}, "plain_text": "Item", "annotations": {}}],
            "color": "default"}
    }
    numbered: Any = {
        **_base_block("numbered_list_item"),
        "numbered_list_item": {"rich_text": [
            {"type": "text", "text": {"content": "Item", "link": None}, "plain_text": "Item", "annotations": {}}],
            "color": "default"}
    }

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(bullet) == "- Item"
    assert await renderer.render(numbered) == "1. Item"


@pytest.mark.asyncio
async def test_render_todo() -> None:
    todo_not_done: Any = {
        **_base_block("to_do"),
        "to_do": {"rich_text": [
            {"type": "text", "text": {"content": "Task", "link": None}, "plain_text": "Task", "annotations": {}}],
            "checked": False, "color": "default"}
    }
    todo_done: Any = {
        **_base_block("to_do"),
        "to_do": {"rich_text": [
            {"type": "text", "text": {"content": "Task", "link": None}, "plain_text": "Task", "annotations": {}}],
            "checked": True, "color": "default"}
    }

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(todo_not_done) == "- [ ] Task"
    assert await renderer.render(todo_done) == "- [x] Task"


@pytest.mark.asyncio
async def test_render_code() -> None:
    code: Any = {
        **_base_block("code"),
        "code": {
            "rich_text": [
                {"type": "text", "text": {"content": "print('hello')", "link": None}, "plain_text": "print('hello')",
                 "annotations": {}}],
            "language": "python",
            "caption": []
        }
    }
    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(code) == "```python\nprint('hello')\n```"


@pytest.mark.asyncio
async def test_render_quote_and_callout() -> None:
    quote: Any = {
        **_base_block("quote"),
        "quote": {"rich_text": [
            {"type": "text", "text": {"content": "Quote", "link": None}, "plain_text": "Quote", "annotations": {}}],
            "color": "default"}
    }
    callout: Any = {
        **_base_block("callout"),
        "callout": {
            "rich_text": [
                {"type": "text", "text": {"content": "Note", "link": None}, "plain_text": "Note", "annotations": {}}],
            "icon": {"type": "emoji", "emoji": "💡"},
            "color": "default"
        }
    }

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(quote) == "> Quote"
    assert await renderer.render(callout) == "> 💡 Note"


@pytest.mark.asyncio
async def test_render_divider_and_bookmark() -> None:
    divider: Any = {**_base_block("divider"), "divider": {}}
    bookmark: Any = {
        **_base_block("bookmark"),
        "bookmark": {"url": "https://example.com", "caption": [
            {"type": "text", "text": {"content": "Example", "link": None}, "plain_text": "Example", "annotations": {}}]}
    }

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(divider) == "---"
    assert await renderer.render(bookmark) == "[Example](https://example.com)"


@pytest.mark.asyncio
async def test_render_media() -> None:
    image: Any = {
        **_base_block("image"),
        "image": {
            "type": "external",
            "external": {"url": "https://example.com/image.png"},
            "caption": [{"type": "text", "text": {"content": "Caption", "link": None}, "plain_text": "Caption",
                         "annotations": {}}]
        }
    }
    video: Any = {
        **_base_block("video"),
        "video": {
            "type": "file",
            "file": {"url": "https://example.com/video.mp4", "expiry_time": "never"},
            "caption": []
        }
    }

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(image) == "![Caption](https://example.com/image.png)"
    assert await renderer.render(video) == "[Video: https://example.com/video.mp4](https://example.com/video.mp4)"


@pytest.mark.asyncio
async def test_render_table_row() -> None:
    row: Any = {
        **_base_block("table_row"),
        "table_row": {
            "cells": [
                [{"type": "text", "text": {"content": "A1", "link": None}, "plain_text": "A1", "annotations": {}}],
                [{"type": "text", "text": {"content": "B1", "link": None}, "plain_text": "B1", "annotations": {}}]
            ]
        }
    }
    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(row) == "| A1 | B1 |"


@pytest.mark.asyncio
async def test_render_table_with_children() -> None:
    table: Any = {
        **_base_block("table"),
        "table": {
            "table_width": 2,
            "has_column_header": True,
            "has_row_header": False
        }
    }
    rows: list[Any] = [
        {
            **_base_block("table_row"),
            "table_row": {
                "cells": [
                    [{"type": "text", "text": {"content": "Header 1", "link": None}, "plain_text": "Header 1",
                      "annotations": {}}],
                    [{"type": "text", "text": {"content": "Header 2", "link": None}, "plain_text": "Header 2",
                      "annotations": {}}]
                ]
            }
        },
        {
            **_base_block("table_row"),
            "table_row": {
                "cells": [
                    [{"type": "text", "text": {"content": "Cell 1", "link": None}, "plain_text": "Cell 1",
                      "annotations": {}}],
                    [{"type": "text", "text": {"content": "Cell 2", "link": None}, "plain_text": "Cell 2",
                      "annotations": {}}]
                ]
            }
        }
    ]

    expected = (
        "| Header 1 | Header 2 |\n"
        "| --- | --- |\n"
        "| Cell 1 | Cell 2 |"
    )

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(table, children=rows) == expected


@pytest.mark.asyncio
async def test_render_table_fetching_children(mocker: Any) -> None:
    table: Any = {
        **_base_block("table"),
        "id": "table_123",
        "table": {
            "table_width": 2,
            "has_column_header": True,
            "has_row_header": False
        }
    }
    rows: list[Any] = [
        {
            **_base_block("table_row"),
            "table_row": {
                "cells": [
                    [{"type": "text", "text": {"content": "A1", "link": None}, "plain_text": "A1", "annotations": {}}],
                    [{"type": "text", "text": {"content": "B1", "link": None}, "plain_text": "B1", "annotations": {}}]
                ]
            }
        }
    ]

    renderer = NotionBlockRenderer("fake_key")

    # Mock the client call
    mock_list = AsyncMock(return_value={"results": rows})
    mocker.patch.object(renderer._client.blocks.children, "list", mock_list)

    result = await renderer.render(table)

    expected = (
        "| A1 | B1 |\n"
        "| --- | --- |"
    )
    assert result == expected
    mock_list.assert_called_once_with(block_id="table_123")


@pytest.mark.asyncio
async def test_render_others() -> None:
    equation: Any = {**_base_block("equation"), "equation": {"expression": "E=mc^2"}}
    child_page: Any = {**_base_block("child_page"), "child_page": {"title": "Page"}}
    embed: Any = {**_base_block("embed"), "embed": {"url": "https://example.com"}}

    renderer = NotionBlockRenderer("fake_key")
    assert await renderer.render(equation) == "$$E=mc^2$$"
    assert await renderer.render(child_page) == "[[Page]]"
    assert await renderer.render(embed) == "<https://example.com>"
