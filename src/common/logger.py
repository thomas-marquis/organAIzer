import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide

@inject
def get_logger(log_level: Annotated[str |int| None, Provide["config.app.log_level"]] = None) -> logging.Logger:
    if not log_level:
        log_level = logging.INFO
    logger = logging.getLogger("organaizer")
    logger.setLevel(log_level)
    return logger