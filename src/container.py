from dependency_injector import containers, providers
from dependency_injector.providers import Container

from src.domain import DomainContainer
from src.agents import AgentContainer
from src.controller import ControllerContainer
from src.infrastructure import InfrastructureContainer

class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.controller.rest.routes", "src.common.logger"])

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
    )

    controller = Container(
        ControllerContainer,
        config=config.controller.required(),
        general_purpose_agent=agent.general_purpose_agent,
    )
    
