import requests
import json
import time
import configparser
import os
import click
import typing as t
import webbrowser

config_file_path = os.path.expanduser("~/.git-cli")
config = configparser.ConfigParser()
access_token: str


@click.group()
@click.pass_context
def main(ctx: t.Any) -> None:
    if check_auth_status(config_file_path):
        config.read(config_file_path)
        global access_token
        access_token = config["DEFAULT"]["access_token"]
    pass

@main.group()
@click.pass_context
def auth(ctx: t.Any) -> None:
    pass

@auth.command()
def login() -> None:
    if check_auth_status(config_file_path):
        print("GitHub is already authenticated")
        return None

    # Define the device code URL
    verification_url = "https://github.com/login/device/code"

    # Define the parameters for the authorization URL
    verification_params = {
        "client_id": "41d4f6d801d4c40c9967",
        'scope': "read:org repo gist"
    }
    headers = {'Accept': 'application/json'}

    response = requests.post(
        verification_url, headers=headers, data=verification_params)

    try:
        print("Enter this code in the browser " + response.json()["user_code"])
    except Exception as e:
        print(e)

    # Open the authorization URL in the default web browser
    webbrowser.open(response.json()["verification_uri"])

    grant_type = "urn:ietf:params:oauth:grant-type:device_code"

    def store_config(data: t.Dict[str, t.Any]) -> None:
        config["DEFAULT"] = {"access_token": data["access_token"]}
        with open(config_file_path, "w") as configfile:
            config.write(configfile)

    def poll() -> None:
        start_time = time.time()
        access_token_url = "https://github.com/login/oauth/access_token"
        access_token_params = {"client_id": "41d4f6d801d4c40c9967", "device_code": response.json()[
            "device_code"], "grant_type": grant_type}
        access_token_headers = {'Accept': 'application/json'}
        while time.time() - start_time < 900:
            poll_response = requests.post(
                access_token_url, headers=access_token_headers, data=access_token_params)
            print(poll_response.json().get("access_token"))
            if poll_response.json().get("error") != "authorization_pending" or poll_response.json().get("access_token") != None:
                data = poll_response.json()
                store_config(data)
                break
            else:
                time.sleep(10)

    poll()


@main.command()
def user() -> None:
    headers = {
        "Authorization": f"Token {access_token}",
        "Accept": "application/json"
    }
    response = requests.get("https://api.github.com/user", headers=headers)
    print(response.json())


def check_auth_status(file_path: str) -> bool:
    if os.path.exists(file_path):
        return True
    else:
        return False


if __name__ == "__main__":
    main()