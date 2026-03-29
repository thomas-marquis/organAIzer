from typing import Any, Final

from notion_client import AsyncClient

from .notion_types import NotionBlock, NotionRichText


class NotionBlockRenderer:
    def __init__(self, api_key: str) -> None:
        self._client: Final = AsyncClient(auth=api_key)

    @staticmethod
    async def render_rich_text(rt: NotionRichText) -> str:
        text = rt["plain_text"]
        annotations = rt.get("annotations", {})

        if annotations.get("code"):
            text = f"`{text}`"
        else:
            if annotations.get("bold"):
                text = f"**{text}**"
            if annotations.get("italic"):
                text = f"*{text}*"
            if annotations.get("strikethrough"):
                text = f"~~{text}~~"
            if annotations.get("underline"):
                text = f"<u>{text}</u>"

        link = rt["text"].get("link")
        if link and isinstance(link, dict) and "url" in link:
            text = f"[{text}]({link['url']})"

        return text

    @staticmethod
    async def _render_rich_text_list(rich_text: list[NotionRichText]) -> str:
        rendered = [await NotionBlockRenderer.render_rich_text(rt) for rt in rich_text]
        return "".join(rendered)

    async def render(self, block: NotionBlock, children: list[NotionBlock] | None = None) -> str:
        block_type = block["type"]
        method_name = f"render_{block_type}"
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if block_type == "table":
                return await method(block, children=children)
            return await method(block)
        return f"[Unsupported block type: {block_type}]"

    @staticmethod
    async def render_paragraph(block: NotionBlock) -> str:
        assert block["type"] == "paragraph"
        return await NotionBlockRenderer._render_rich_text_list(block["paragraph"]["rich_text"])

    @staticmethod
    async def render_heading_1(block: NotionBlock) -> str:
        assert block["type"] == "heading_1"
        return f"# {await NotionBlockRenderer._render_rich_text_list(block['heading_1']['rich_text'])}"

    @staticmethod
    async def render_heading_2(block: NotionBlock) -> str:
        assert block["type"] == "heading_2"
        return f"## {await NotionBlockRenderer._render_rich_text_list(block['heading_2']['rich_text'])}"

    @staticmethod
    async def render_heading_3(block: NotionBlock) -> str:
        assert block["type"] == "heading_3"
        return f"### {await NotionBlockRenderer._render_rich_text_list(block['heading_3']['rich_text'])}"

    @staticmethod
    async def render_bulleted_list_item(block: NotionBlock) -> str:
        assert block["type"] == "bulleted_list_item"
        return f"- {await NotionBlockRenderer._render_rich_text_list(block['bulleted_list_item']['rich_text'])}"

    @staticmethod
    async def render_numbered_list_item(block: NotionBlock) -> str:
        assert block["type"] == "numbered_list_item"
        # Note: Markdown handles numbering automatically if we use '1. ',
        # but Notion gives us the items one by one. To be simple we use '1. ' for all.
        return f"1. {await NotionBlockRenderer._render_rich_text_list(block['numbered_list_item']['rich_text'])}"

    @staticmethod
    async def render_to_do(block: NotionBlock) -> str:
        assert block["type"] == "to_do"
        checked = block["to_do"]["checked"]
        checkbox = "[x]" if checked else "[ ]"
        return f"- {checkbox} {await NotionBlockRenderer._render_rich_text_list(block['to_do']['rich_text'])}"

    @staticmethod
    async def render_toggle(block: NotionBlock) -> str:
        assert block["type"] == "toggle"
        # Toggle is not natively supported in standard Markdown, often rendered as a list item or detail tag
        return f"- {await NotionBlockRenderer._render_rich_text_list(block['toggle']['rich_text'])}"

    @staticmethod
    async def render_code(block: NotionBlock) -> str:
        assert block["type"] == "code"
        language = block["code"].get("language", "")
        code_text = "".join([rt["plain_text"] for rt in block["code"]["rich_text"]])
        return f"```{language}\n{code_text}\n```"

    @staticmethod
    async def render_quote(block: NotionBlock) -> str:
        assert block["type"] == "quote"
        return f"> {await NotionBlockRenderer._render_rich_text_list(block['quote']['rich_text'])}"

    @staticmethod
    async def render_callout(block: NotionBlock) -> str:
        assert block["type"] == "callout"
        icon = block["callout"].get("icon")
        icon_str = ""
        if icon:
            if icon["type"] == "emoji":
                icon_str = icon["emoji"] + " "
            elif icon["type"] == "external":
                icon_str = f"![icon]({icon['external']['url']}) "
            elif icon["type"] == "file":
                icon_str = f"![icon]({icon['file']['url']}) "

        return f"> {icon_str}{await NotionBlockRenderer._render_rich_text_list(block['callout']['rich_text'])}"

    @staticmethod
    async def render_divider(block: NotionBlock) -> str:
        assert block["type"] == "divider"
        return "---"

    @staticmethod
    async def render_bookmark(block: NotionBlock) -> str:
        assert block["type"] == "bookmark"
        url = block["bookmark"]["url"]
        caption = await NotionBlockRenderer._render_rich_text_list(block["bookmark"].get("caption", []))
        if caption:
            return f"[{caption}]({url})"
        return f"<{url}>"

    @staticmethod
    async def render_equation(block: NotionBlock) -> str:
        assert block["type"] == "equation"
        expression = block["equation"]["expression"]
        return f"$${expression}$$"

    @staticmethod
    async def _render_media(block_type: str, block_content: Any) -> str:
        url = ""
        if block_content["type"] == "external":
            url = block_content["external"]["url"]
        elif block_content["type"] == "file":
            url = block_content["file"]["url"]
        elif block_content["type"] == "file_upload":
            url = block_content["file_upload"].get("url", "")  # Notion API varies here

        caption = await NotionBlockRenderer._render_rich_text_list(block_content.get("caption", []))
        if block_type == "image":
            return f"![{caption}]({url})"
        elif block_type in ["video", "audio", "file", "pdf"]:
            return f"[{block_type.capitalize()}: {caption if caption else url}]({url})"
        return f"<{url}>"

    @staticmethod
    async def render_image(block: NotionBlock) -> str:
        assert block["type"] == "image"
        return await NotionBlockRenderer._render_media("image", block["image"])

    @staticmethod
    async def render_video(block: NotionBlock) -> str:
        assert block["type"] == "video"
        return await NotionBlockRenderer._render_media("video", block["video"])

    @staticmethod
    async def render_audio(block: NotionBlock) -> str:
        assert block["type"] == "audio"
        return await NotionBlockRenderer._render_media("audio", block["audio"])

    @staticmethod
    async def render_file(block: NotionBlock) -> str:
        assert block["type"] == "file"
        return await NotionBlockRenderer._render_media("file", block["file"])

    @staticmethod
    async def render_pdf(block: NotionBlock) -> str:
        assert block["type"] == "pdf"
        return await NotionBlockRenderer._render_media("pdf", block["pdf"])

    @staticmethod
    async def render_child_page(block: NotionBlock) -> str:
        assert block["type"] == "child_page"
        return f"[[{block['child_page']['title']}]]"

    @staticmethod
    async def render_child_database(block: NotionBlock) -> str:
        assert block["type"] == "child_database"
        return f"[[Database: {block['child_database']['title']}]]"

    @staticmethod
    async def render_embed(block: NotionBlock) -> str:
        assert block["type"] == "embed"
        return f"<{block['embed']['url']}>"

    @staticmethod
    async def render_link_preview(block: NotionBlock) -> str:
        assert block["type"] == "link_preview"
        return f"<{block['link_preview']['url']}>"

    @staticmethod
    async def render_link_to_page(block: NotionBlock) -> str:
        assert block["type"] == "link_to_page"
        page_id = block["link_to_page"].get("page_id") or block["link_to_page"].get("database_id")
        return f"[[{page_id}]]"

    async def render_table(self, block: NotionBlock, children: list[NotionBlock] | None = None) -> str:
        assert block["type"] == "table"

        if children is None:
            response = await self._client.blocks.children.list(block_id=block["id"])
            children = response.get("results", [])

        if not children:
            return ""

        rows = []
        has_column_header = block["table"].get("has_column_header", False)
        table_width = block["table"].get("table_width", 0)

        for i, child in enumerate(children):
            if child["type"] == "table_row":
                rows.append(await NotionBlockRenderer.render_table_row(child))
                if i == 0 and has_column_header:
                    separator = "| " + " | ".join(["---"] * table_width) + " |"
                    rows.append(separator)

        return "\n".join(rows)

    @staticmethod
    async def render_table_row(block: NotionBlock) -> str:
        assert block["type"] == "table_row"
        cells = block["table_row"]["cells"]
        rendered_cells = [await NotionBlockRenderer._render_rich_text_list(cell) for cell in cells]
        return "| " + " | ".join(rendered_cells) + " |"

    @staticmethod
    async def render_synced_block(block: NotionBlock) -> str:
        assert block["type"] == "synced_block"
        return "[Synced Block]"

    @staticmethod
    async def render_template(block: NotionBlock) -> str:
        assert block["type"] == "template"
        return await NotionBlockRenderer._render_rich_text_list(block["template"]["rich_text"])

    @staticmethod
    async def render_column_list(block: NotionBlock) -> str:
        assert block["type"] == "column_list"
        return "[Column List]"

    @staticmethod
    async def render_column(block: NotionBlock) -> str:
        assert block["type"] == "column"
        return "[Column]"

    @staticmethod
    async def render_breadcrumb(block: NotionBlock) -> str:
        assert block["type"] == "breadcrumb"
        return "[Breadcrumb]"

    @staticmethod
    async def render_table_of_contents(block: NotionBlock) -> str:
        assert block["type"] == "table_of_contents"
        return "[Table of Contents]"
