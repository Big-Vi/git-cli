import requests
import click
import typing as t
import sys

from requests.models import Response
from tabulate import tabulate
import datetime

from git_cli.graphql.queries import repo_overview
from git_cli.utils import check_auth_status
import git_cli.constants as constants

# Custom Error Class.
class NoToken(Exception):
    pass


@click.command()
def overview() -> None:
    variables: t.Dict[str, t.Any] = dict()
    access_token: t.Union[str, bool] = check_auth_status()
        
    try:
        if not access_token:
            raise NoToken()
        else:
            headers = {"Authorization": f"Token {access_token}"}
            variables["year"] = f"{datetime.date.today().year}-01-01T00:00:00"
            response: Response = requests.post(
                constants.GITHUB_GRAPHQL_ENDPOINT, json={"query": repo_overview, "variables": variables}, headers=headers)
            # print(response.json())
    except NoToken:
        print("Please use `git-cli login` to authenticate.")
        sys.exit()
    except:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            response.status_code, repo_overview))
        
    response_data = response.json()["data"]["viewer"]
    overview = [
        ["Followers", response_data["followers"]["totalCount"]], 
        ["Follwing", response_data["following"]["totalCount"]],
        ["Starred Repo", response_data["starredRepositories"]["totalCount"]],
        ["Pinned Items", response_data["pinnedItems"]["totalCount"]],
        ["Repositories", response_data["repositories"]["totalCount"]],
        ["Total Contributions(Current year)", response_data["contributionsCollection"]["contributionCalendar"]["totalContributions"]]
    ]
    print(tabulate(overview, headers=["Title", "Numbers"]))
