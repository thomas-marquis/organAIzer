from dataclasses import dataclass
import datetime as dt

@dataclass
class Note:
    id_: str
    title: str
    content: str
    created_at: dt.datetime
    updated_at: dt.datetime
    tags: list[str] | None = None