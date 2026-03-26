from src.agent.agent import Agent
from src.app import app
import dotenv
import click
import os
import uvicorn

dotenv.load_dotenv()

@click.group()
def cli():
    pass

@cli.command()
@click.option("-m", "--message", type=str)
def run(message: str) -> None:
    """Run the agent in CLI mode"""
    message = message or "I want to settle and work in Norway, I'm seeking a job there. According to my todo list and my job seeking notes, what should be the next steps?"
    agent = Agent(os.getenv("MISTRAL_API_KEY"))
    for response in agent.run(message):
        click.echo(response)

@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to listen on")
def serve(host: str, port: int) -> None:
    """Start the FastAPI server"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    cli()
