import configparser
import click
from .cmd import login, overview

config = configparser.ConfigParser()


@click.group()
def cli() -> None:
    """
    Entry point for the CLI.
    """
    pass


cli.add_command(login)
cli.add_command(overview)







