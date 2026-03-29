from src.domain import Todolist, TaskLabel, Task, Note, NoteContent


def render_todolists(task_lists: list[Todolist]) -> str:
    return _render_subb_task_lists(task_lists)


def render_task_labels(labels: list[TaskLabel]) -> str:
    return "\n".join([f"- Id: {label.id_}; Name: {label.name}" for label in labels])


def render_tasks(tasks: list[Task]) -> str:
    return "\n".join([_render_task(task) for task in tasks])


def render_note(note: Note) -> str:
    res = f"- Id: {note.id_}; Title: {note.title}; Created at: {note.created_at.strftime('%Y-%m-%d')}"
    if note.tags:
        res += f"; Tags: {','.join(note.tags)}"

    return res


def render_notes(notes: list[Note]) -> str:
    return "\n".join([render_note(note) for note in notes])


def render_note_content(content: NoteContent) -> str:
    if not content.markdown:
        return "<note is empty>"
    return content.markdown


def _render_task(task: Task) -> str:
    res = f"- [{'x' if task.completed else ' '}] {task.title} (created at: {task.created_at.strftime('%Y-%m-%d')}; id={task.id_})"
    if task.due_date:
        res += f"; Due date: {task.due_date.strftime('%Y-%m-%d')}"
    if task.labels:
        res += f"; Labels: {','.join([label.name for label in task.labels])}"
    if task.description:
        res += f"; Description: {task.description}"
    return res


def _render_subb_task_lists(sub_task_lists: list[Todolist], indent_level: int = 0) -> str:
    reprs: list[str] = []
    for task_list in sub_task_lists:
        current = f"- Id: {task_list.id_}; Name: {task_list.name}; Is active: {'no' if task_list.archived else 'yes'}"
        if indent_level > 0:
            current = "    " * indent_level + current
        if task_list.sub_todolists:
            current += f"; Sub-lists:\n{_render_subb_task_lists(task_list.sub_todolists, indent_level + 1)}"
        reprs.append(current)
    return "\n".join(reprs)
