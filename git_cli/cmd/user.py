import click
import requests
from .utils import check_auth_status
from git_cli.constants import CONFIG_FILE_PATH
import typing as t

@click.command()
def user() -> None:
    access_token: t.Union[str, bool] = check_auth_status()

    if access_token:
        headers = {
            "Authorization": f"Token {access_token}",
            "Accept": "application/json"
        }
        response = requests.get("https://api.github.com/user", headers=headers)
        print(response.json())
    else:
        print("Please use `git-cli login` to authenticate.")
