from __future__ import annotations

from dataclasses import dataclass, field
import datetime as dt


@dataclass
class Task:
    id_: str
    title: str
    description: str
    created_at: dt.datetime
    due_date: dt.datetime | None = None
    completed: bool = False
    labels: list[TaskLabel] = field(default_factory=list)


@dataclass
class Todolist:
    id_: str
    name: str
    sub_todolists: list[Todolist] = field(default_factory=list)
    archived: bool = False



@dataclass
class TaskLabel:
    id_: str
    name: str