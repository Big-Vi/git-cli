import os
import configparser
import requests
import typing as t

import git_cli.constants as constants

config = configparser.ConfigParser()

def check_auth_status() -> t.Union[str, bool]:
    """
    Get GitHub credentials stored in local file.
    If not return false.
    """
    if os.path.exists(constants.CONFIG_FILE_PATH):
        config.read(constants.CONFIG_FILE_PATH)
        return config["DEFAULT"]["access_token"]
    else:
        return False
