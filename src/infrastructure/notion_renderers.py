from .notion_types import NotionBlock, NotionRichText


class NotionBlockRenderer:
    @staticmethod
    def render_rich_text(rt: NotionRichText) -> str:
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
    def render_paragraph(block: NotionBlock) -> str:
        assert block["type"] == "paragraph"
        rich_text = block["paragraph"]["rich_text"]
        return "".join([NotionBlockRenderer.render_rich_text(rt) for rt in rich_text])
