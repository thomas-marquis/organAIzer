from dependency_injector import containers, providers
from dependency_injector.providers import Container

from src.agent import AgentContainer
from src.controller import ControllerContainer
from src.infrastructure import InfrastructureContainer

class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".rest.routes", "..common.logger"])

    config = providers.Configuration()

    infrastructure = Container(
        InfrastructureContainer,
        config=config.infrastructure.required(),
    )

    agent = Container(
        AgentContainer,
        config=config.agent,
        llm=infrastructure.mistral_llm.required(),
    )

    controller = Container(
        ControllerContainer,
        config=config.controller.required(),
        agent=agent,
    )
    
