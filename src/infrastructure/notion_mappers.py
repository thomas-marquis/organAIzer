

from

def render_page_to_markdown(page: dict) -> str:
    return page["properties"]["Name"]["title"][0]["plain_text"]