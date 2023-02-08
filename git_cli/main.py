import configparser
import click
from .cmd import login, user
from .constants import CONFIG_FILE_PATH

config = configparser.ConfigParser()

access_token: str


@click.group()
def cli() -> None:
    """
    Entry point for the CLI.
    """
    pass


cli.add_command(login)
cli.add_command(user)







