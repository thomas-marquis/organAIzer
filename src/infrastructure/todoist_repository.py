from typing import Final
import asyncio

from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Project, Task as TodoistTask, Label as TodoistLabel, Section

from src.domain import Task, Todolist, TaskRepository, TaskLabel, TechnicalError
from src.common import get_logger


logger = get_logger()

class TodoistTaskRepository(TaskRepository):
    def __init__(self, api_key: str) -> None:
        self._api: Final = TodoistAPIAsync(api_key)
        self._cached_labels_by_id: dict[str, TaskLabel] = {}
        self._cached_labels_by_name: dict[str, TaskLabel] = {}

    async def get_all_todolists(self) -> list[Todolist]:
        projects_it = await self._api.get_projects()
        projects: list[Project] = []
        async for projects_batch in projects_it:
            projects.extend(projects_batch)

        return self._build_todolists_tree(projects)

    async def get_all_labels(self) -> list[TaskLabel]:
        labels_it = await self._api.get_labels()
        labels: list[TodoistLabel] = []
        async for label_batch in labels_it:
            labels.extend(label_batch)
        res = [TaskLabel(id_=label.id, name=label.name) for label in labels]

        self._cached_labels_by_id = {label.id_: label for label in res}
        self._cached_labels_by_name = {label.name: label for label in res}

        return res

    async def list_tasks_by_todolist_id(self, list_id: str) -> list[Task]:
        try:
            labels, tasks_it = await asyncio.gather(
                self.get_all_labels(),
                self._api.get_tasks(project_id=list_id),
            )

            tasks: list[TodoistTask] = []
            async for tasks_batch in tasks_it:
                tasks.extend(tasks_batch)
        except Exception as e:
            raise TechnicalError(f"Error fetching tasks and labels by list id: {e}")

        label_map: dict[str, TaskLabel] = {label.name: label for label in labels}
        section_ids: list[str] = [id_ for task in tasks if (id_ := task.section_id)]

        try:
            coros = [self._api.get_section(section_id=id_) for id_ in section_ids]
            sections: tuple[Section] = await asyncio.gather(*coros)
            section_by_id = {section.id: section for section in sections}
        except Exception as e:
            logger.error(f"Error fetching sections: {e}. Skipping...")
            section_by_id = {}

        def make_title(task: TodoistTask) -> str:
            if task.section_id:
                return f"{section_by_id[task.section_id].name}: {task.content}"
            return task.content

        def get_labels(task: TodoistTask) -> list[TaskLabel]:
            return [label for label_name in (task.labels or []) if (label := label_map.get(label_name))]

        return [Task(
            id_=task.id,
            title=make_title(task),
            description=task.description,
            created_at=task.created_at,
            due_date=task.due,
            completed=task.is_completed,
            labels=get_labels(task),
        ) for task in tasks]

    async def get_todolist_by_id(self, list_id: str) -> Todolist:
        project, all_lists = await asyncio.gather(
            self._api.get_project(project_id=list_id),
            self.get_all_todolists(),
        )
        return self._build_single_todolist_tree(project, all_lists)

    async def get_task_by_id(self, task_id: str) -> Task | None:
        try:
            task = await self._api.get_task(task_id)
        except Exception as e:
            logger.error(e)
            raise TechnicalError(f"Error fetching task by id: {e}")

        async def get_section() -> Section | None:
            if not task.section_id:
                return None
            try:
                return await self._api.get_section(section_id=task.section_id)
            except Exception as e:
                logger.error(f"Error fetching section for task {task_id}: {e}. Skippin...")
                return None

        async def get_labels() -> list[TaskLabel]:
            if not task.labels:
                return []
            coros = [self._get_label_by_name(label_name) for label_name in task.labels]
            raw_labels = await asyncio.gather(*coros)
            return [TaskLabel(id_=raw_label.id, name=raw_label.name) for raw_label in raw_labels if raw_label]

        try:
            section, labels = await asyncio.gather(get_section(), get_labels())
        except TechnicalError as e:
            raise e
        except Exception as e:
            logger.error(e)
            raise TechnicalError(f"Error fetching section and labels for task {task_id}: {e}.")

        if section:
            title = f"{section.name}: {task.content}"
        else:
            title = task.content

        return Task(
            id_=task.id,
            title=title,
            description=task.description,
            created_at=task.created_at,
            due_date=task.due,
            completed=task.is_completed,
            labels=labels,
        )

    async def _get_label_by_id(self, label_id: str) -> TaskLabel:
        if label_id in self._cached_labels_by_id:
            return self._cached_labels_by_id[label_id]
        try:
            label = await self._api.get_label(label_id)
            self._cached_labels_by_id[label_id] = TaskLabel(id_=label.id, name=label.name)
            return self._cached_labels_by_id[label_id]
        except Exception as e:
            logger.error(e)
            raise TechnicalError(f"Error fetching label by id: {e}")

    async def _get_label_by_name(self, label_name: str) -> TaskLabel:
        if label_name in self._cached_labels_by_name:
            return self._cached_labels_by_name[label_name]
        try:
            label = await self._api.get_label(label_name)
            self._cached_labels_by_name[label_name] = TaskLabel(id_=label.id, name=label.name)
            return self._cached_labels_by_name[label_name]
        except Exception as e:
            logger.error(e)
            raise TechnicalError(f"Error fetching label by name: {e}")

    @staticmethod
    def _build_todolists_tree(projects: list[Project]) -> list[Todolist]:
        lists_map: dict[str, Todolist] = {}
        root_lists: list[Todolist] = []

        for project in projects:
            todolist = _map_project_to_todolist(project)
            lists_map[todolist.id_] = todolist

        # we need a second iteration in case the parent is located after the child in the original list
        for project in projects:
            curr_list = lists_map[project.id]
            if (parent_id := project.parent_id) and parent_id in lists_map:
                lists_map[parent_id].sub_todolists.append(curr_list)
            else:
                root_lists.append(curr_list)

        return root_lists

    @staticmethod
    def _build_single_todolist_tree(project: Project, all_task_lists: list[Todolist]) -> Todolist:
        def lookup(list_id: str, sub_tree_roots: list[Todolist]) -> Todolist | None:
            for root_list in sub_tree_roots:
                if root_list.id == list_id:
                    return root_list
                result = lookup(list_id, root_list.sub_todolists)
                if result:
                    return result
            return None

        target_list = lookup(project.id, all_task_lists)
        if not target_list:
            raise TechnicalError(f"Project {project.id} not found in the Todoist project tree, which is not supposed to happen.")

        return target_list


def _map_project_to_todolist(project: Project) -> Todolist:
    return Todolist(
        id_=str(project.id),
        name=project.name,
        archived=project.is_archived,
    )
