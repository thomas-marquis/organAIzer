from src.infrastructure.notion_renderers import NotionBlockRenderer
from src.infrastructure.notion_types import NotionParagraphBlock


def test_render_paragraph_complex() -> None:
    # Given
    block: NotionParagraphBlock = {
        "object": "block",
        "id": "123",
        "created_time": "2021-03-16T16:36:00.000Z",
        "last_edited_time": "2021-03-16T16:36:00.000Z",
        "parent": {"type": "page_id", "page_id": "456"},
        "has_children": False,
        "in_trash": False,
        "type": "paragraph",
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
                    "text": {"content": " and ", "link": None},
                    "plain_text": " and ",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": "italic", "link": None},
                    "plain_text": "italic",
                    "annotations": {"italic": True}
                },
                {
                    "type": "text",
                    "text": {"content": " with ", "link": None},
                    "plain_text": " with ",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": "strikethrough", "link": None},
                    "plain_text": "strikethrough",
                    "annotations": {"strikethrough": True}
                },
                {
                    "type": "text",
                    "text": {"content": " and ", "link": None},
                    "plain_text": " and ",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": "code", "link": None},
                    "plain_text": "code",
                    "annotations": {"code": True}
                },
                {
                    "type": "text",
                    "text": {"content": " and ", "link": None},
                    "plain_text": " and ",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": "link", "link": {"url": "https://example.com"}},
                    "plain_text": "link",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": " and ", "link": None},
                    "plain_text": " and ",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": "combined", "link": None},
                    "plain_text": "combined",
                    "annotations": {"bold": True, "italic": True, "underline": True}
                }
            ],
            "color": "default"
        }
    }

    # When
    result = NotionBlockRenderer.render_paragraph(block)

    # Then
    assert result == "Normal **bold** and *italic* with ~~strikethrough~~ and `code` and [link](https://example.com) and <u>***combined***</u>"


def test_render_paragraph() -> None:
    # Given
    block: NotionParagraphBlock = {
        "object": "block",
        "id": "123",
        "created_time": "2021-03-16T16:36:00.000Z",
        "last_edited_time": "2021-03-16T16:36:00.000Z",
        "parent": {"type": "page_id", "page_id": "456"},
        "has_children": False,
        "in_trash": False,
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "Hello ", "link": None},
                    "plain_text": "Hello ",
                    "annotations": {}
                },
                {
                    "type": "text",
                    "text": {"content": "world!", "link": None},
                    "plain_text": "world!",
                    "annotations": {"bold": True}
                }
            ],
            "color": "default"
        }
    }

    # When
    result = NotionBlockRenderer.render_paragraph(block)

    # Then
    assert result == "Hello world!"
