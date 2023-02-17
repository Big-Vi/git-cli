import click
from git_cli.utils import check_auth_status
import requests
import time
import configparser
import typing as t
import webbrowser
import sys
import logging
import git_cli.constants as constants

config = configparser.ConfigParser()
logger = logging.getLogger(__name__)

@click.command()
def login() -> None:
    access_token: t.Union[str, bool] = check_auth_status()
    if access_token:
        print("GitHub is already authenticated")
        return None

    try:
        # Define the parameters for the authorization URL
        verification_params = {
            "client_id": constants.CLIENT_ID,
            'scope': "read:org repo gist"
        }
        request_headers: t.Dict[str, str] = {'Accept': 'application/json'}

        response = requests.post(
            constants.VERIFICATION_URL, headers=request_headers, data=verification_params)

        print("Enter this code in the browser " + response.json()["user_code"])
        # Open the authorization URL in the default web browser
        click.pause()
        webbrowser.open(response.json()["verification_uri"])

    except Exception as e:
        logger.error(e)
        sys.exit()

    grant_type = "urn:ietf:params:oauth:grant-type:device_code"

    # Store the GitHub access token in configfile
    def store_config(data: t.Dict[str, t.Any]) -> None:
        config["DEFAULT"] = {"access_token": data["access_token"]}
        with open(constants.CONFIG_FILE_PATH, "w") as configfile:
            config.write(configfile)

    # Polling access token url to get the token
    def poll() -> None:
        start_time = time.time()
        access_token_params = {"client_id": "41d4f6d801d4c40c9967", "device_code": response.json()[
            "device_code"], "grant_type": grant_type}
        access_token_headers = {'Accept': 'application/json'}
        while time.time() - start_time < 900:
            poll_response = requests.post(
                constants.ACCESS_TOKEN_URL, headers=access_token_headers, data=access_token_params)
                
            if(poll_response.json().get("error")):
                print(poll_response.json().get("error"))
            else:
                print("Success")

            if poll_response.json().get("error") != "authorization_pending" or poll_response.json().get("access_token") != None:
                data = poll_response.json()
                store_config(data)
                break
            else:
                time.sleep(10)

    poll()

    
