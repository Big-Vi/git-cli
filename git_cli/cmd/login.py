import click
from git_cli.utils import check_auth_status
import requests
import time
import configparser
import typing as t
import webbrowser
import git_cli.constants as constants

config = configparser.ConfigParser()

@click.command()
def login() -> None:
    access_token: t.Union[str, bool] = check_auth_status()
    if access_token:
        print("GitHub is already authenticated")
        return None

    # Define the parameters for the authorization URL
    verification_params = {
        "client_id": "41d4f6d801d4c40c9967",
        'scope': "read:org repo gist"
    }
    headers = {'Accept': 'application/json'}

    response = requests.post(
        constants.VERIFICATION_URL, headers=headers, data=verification_params)

    try:
        print("Enter this code in the browser " + response.json()["user_code"])
    except Exception as e:
        print(e)

    # Open the authorization URL in the default web browser
    webbrowser.open(response.json()["verification_uri"])

    grant_type = "urn:ietf:params:oauth:grant-type:device_code"

    def store_config(data: t.Dict[str, t.Any]) -> None:
        config["DEFAULT"] = {"access_token": data["access_token"]}
        with open(constants.CONFIG_FILE_PATH, "w") as configfile:
            config.write(configfile)

    def poll() -> None:
        start_time = time.time()
        access_token_params = {"client_id": "41d4f6d801d4c40c9967", "device_code": response.json()[
            "device_code"], "grant_type": grant_type}
        access_token_headers = {'Accept': 'application/json'}
        while time.time() - start_time < 900:
            poll_response = requests.post(
                constants.ACCESS_TOKEN_URL, headers=access_token_headers, data=access_token_params)
            print(poll_response.json())
            if poll_response.json().get("error") != "authorization_pending" or poll_response.json().get("access_token") != None:
                data = poll_response.json()
                store_config(data)
                break
            else:
                time.sleep(10)

    poll()
