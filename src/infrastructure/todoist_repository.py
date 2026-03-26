import os
from functools import lru_cache
from typing import Final

from todoist_api_python.api import TodoistAPI

from ..domain.entities import Task, Project
from ..domain.repositories import TaskRepository, ProjectRepository


class TodoistTaskRepository(TaskRepository):
    def __init__(self, api_key: str) -> None:
        self._api: Final = TodoistAPI(api_key)


    def _convert_todoist_task(self, todoist_task) -> Task:
        """Convert Todoist task to domain Task entity"""
        return Task(
            id=str(todoist_task.id),
            title=todoist_task.content,
            description=todoist_task.description if hasattr(todoist_task, 'description') else None,
            due_date=todoist_task.due.datetime if hasattr(todoist_task.due, 'datetime') else None,
            priority=todoist_task.priority,
            labels=todoist_task.labels,
            project_id=str(todoist_task.project_id),
            completed=todoist_task.is_completed
        )

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks from Todoist"""
        try:
            tasks = self._api.get_tasks()
            return [self._convert_todoist_task(task) for task in tasks]
        except Exception as e:
            print(f"Error getting tasks from Todoist: {e}")
            return []

    def get_tasks_by_project(self, project_id: str) -> list[Task]:
        """Get tasks by project ID"""
        try:
            tasks = self._api.get_tasks(project_id=project_id)
            return [self._convert_todoist_task(task) for task in tasks]
        except Exception as e:
            print(f"Error getting tasks by project from Todoist: {e}")
            return []

    def get_task_by_id(self, task_id: str) -> Task | None:
        """Get task by ID"""
        try:
            task = self._api.get_task(task_id=task_id)
            return self._convert_todoist_task(task)
        except Exception as e:
            print(f"Error getting task by ID from Todoist: {e}")
            return None


class TodoistProjectRepository(ProjectRepository):
    """Concrete implementation of ProjectRepository using Todoist API"""

    def __init__(self, api_key: str) -> None:
        self.client = self._get_todoist_client()

    @lru_cache
    def _get_todoist_client(self) -> TodoistAPI:
        """Get cached Todoist client"""
        return TodoistAPI(os.environ["TODOIST_TOKEN"])

    def _convert_todoist_project(self, todoist_project) -> Project:
        """Convert Todoist project to domain Project entity"""
        return Project(
            id=str(todoist_project.id),
            name=todoist_project.name,
            description=todoist_project.comment_count if hasattr(todoist_project, 'comment_count') else None
        )

    def get_all_projects(self) -> list[Project]:
        """Get all projects from Todoist"""
        try:
            projects = self.client.get_projects()
            return [self._convert_todoist_project(project) for project in projects]
        except Exception as e:
            print(f"Error getting projects from Todoist: {e}")
            return []

    def get_project_by_id(self, project_id: str) -> Project | None:
        """Get project by ID"""
        try:
            project = self.client.get_project(project_id=project_id)
            return self._convert_todoist_project(project)
        except Exception as e:
            print(f"Error getting project by ID from Todoist: {e}")
            return None

    def get_project_structure(self) -> dict:
        """Get the hierarchical structure of projects"""
        try:
            projects = self.client.get_projects()

            # Build project hierarchy
            project_map = {}
            root_projects = []

            for project in projects:
                project_data = {
                    "id": str(project.id),
                    "name": project.name,
                    "children": []
                }
                project_map[project.id] = project_data

                if project.parent_id:
                    if project.parent_id in project_map:
                        project_map[project.parent_id]["children"].append(project_data)
                else:
                    root_projects.append(project_data)

            return {"root": root_projects}
        except Exception as e:
            print(f"Error getting project structure from Todoist: {e}")
            return {"root": []}
