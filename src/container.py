from dependency_injector import containers, providers
from dependency_injector.providers import Container

from src.agents import AgentContainer
from src.controller import ControllerContainer
from src.domain import DomainContainer
from src.infrastructure import InfrastructureContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "src.common.logger",
        "src.controller.rest.routes",
        "src.controller.cli.chat",
    ])

    config = providers.Configuration()

    infrastructure = Container(
        InfrastructureContainer,
        config=config.infrastructure.required(),
    )

    domain = Container(
        DomainContainer,
        task_repository=infrastructure.todoist,
    )

    agent = Container(
        AgentContainer,
        llm=infrastructure.mistral_llm,
        task_service=domain.task_service,
        task_repository=infrastructure.todoist,
        note_repository=infrastructure.notion,
    )

    controller = Container(
        ControllerContainer,
        config=config.controller.required(),
        general_purpose_agent=agent.general_purpose_agent,
    )
