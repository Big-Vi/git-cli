import requests
import click
import typing as t
import sys

from requests.models import Response

from git_cli.graphql.queries import repo_overview
from git_cli.utils import check_auth_status
import git_cli.constants as constants

# Custom Error Class.
class NoToken(Exception):
    pass


@click.command()
def overview() -> Response:
    access_token: t.Union[str, bool] = check_auth_status()
        
    try:
        if not access_token:
            raise NoToken()
        else:
            headers = {"Authorization": f"Token {access_token}"}
            response: Response = requests.post(
                constants.GITHUB_GRAPHQL_ENDPOINT, json={"query": repo_overview}, headers=headers)
            print(response.json())
    except NoToken:
        print("Please use `git-cli login` to authenticate.")
        sys.exit()
    except:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            response.status_code, repo_overview))
        sys.exit()
        
    
    return response
