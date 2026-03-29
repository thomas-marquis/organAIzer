from src.domain import Todolist, TaskLabel


def render_task_lists(task_lists: list[Todolist]) -> str:
    return _render_subb_task_lists(task_lists)


def render_task_labels(labels: list[TaskLabel]) -> str:
    return "\n".join([f"- Id: {label.id_}; Name: {label.name}" for label in labels])


def _render_subb_task_lists(sub_task_lists: list[Todolist], indent_level: int = 0) -> str:
    reprs:  list[str] = []
    for task_list in sub_task_lists:
        current = f"- Id: {task_list.id_}; Name: {task_list.name}; Is active: {'no' if task_list.archived else 'yes'}"
        if indent_level > 0:
            current = "    " * indent_level + current
        if task_list.sub_todolists:
            current += f"; Sub-lists:\n{_render_subb_task_lists(task_list.sub_todolists, indent_level + 1)}"
        reprs.append(current)
    return "\n".join(reprs)

