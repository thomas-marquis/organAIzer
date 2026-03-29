import asyncio

import rich
import typer
from dependency_injector.wiring import inject, Provide
from rich.prompt import Prompt, Confirm

from src.agents.general_purpose import GPAgent

chat_app = typer.Typer()


@inject
async def _chat(prompt: str, gp_agent: GPAgent = Provide["agent.general_purpose_agent"]) -> str:
    async for event in gp_agent.run(prompt):
        rich.print(event)
    return "ok"


prompt = ""
"""for debug purposes"""


@chat_app.command()
def chat(
        # prompt: Annotated[str | None, typer.Option(None, "--message", "-m", help="The message to send to the agent")],
) -> None:
    loop = asyncio.get_event_loop()
    is_running = True
    global prompt
    while is_running:
        if not prompt:
            prompt = Prompt.ask("[bold yellow]>>> Me[/bold yellow]")
        else:
            # in debug mode, we want to exit right after the response
            is_running = False
        if prompt == "exit":
            if Confirm.ask("Are you sure you want to exit?"):
                break
        response = loop.run_until_complete(_chat(prompt))
        rich.print(f"[bold dark_orange]<<< Aizer:[/bold dark_orange] [dark_orange]{response}[/dark_orange]")
        prompt = ""
