from  fastapi import FastAPI
import uvicorn
import click
from ..container import ControllerContainer
from dependency_injector.wiring import Provider, inject

from typer import Typer


def make_app() -> FastAPI:
    return FastAPI(
        title="organaizer",
    )


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to listen on")
@inject
def serve(config: dict = Provider[ControllerContainer.config]) -> None:
    pass