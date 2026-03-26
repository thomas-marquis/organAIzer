import logging
from dependency_injector.wiring import inject, Provide
from ..container import AppContainer

@inject
def get_logger(log_level: str |int| None = Provide[AppContainer.config.app.log_level]) -> logging.Logger:
    if not log_level:
        log_level = logging.INFO
    logger =logging.getLogger("organaizer")
    logger.setLevel(log_level)
    return logger