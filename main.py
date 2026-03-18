from src.agent.agent import  Agent
import dotenv
import click
import os

dotenv.load_dotenv()

@click.group()
def cli():
    pass

@cli.command()
@click.option("-m", "--message", type=str)
def run(message: str) -> None:
    message = "I want to settle and work in Norway, I'm seeking a job there. According to my todo list and my job seeking notes, what should be the next steps?"
    agent = Agent(os.getenv("MISTRAL_API_KEY"))
    for response in agent.run(message):
        click.echo(response)


if __name__ == "__main__":
    cli()
