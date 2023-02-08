import os
import configparser

import typing as t
from git_cli.constants import CONFIG_FILE_PATH

config = configparser.ConfigParser()

def check_auth_status() -> t.Union[str, bool]:
    """
    Get GitHub credentials stored in local file.
    If not return false.
    """
    if os.path.exists(CONFIG_FILE_PATH):
        config.read(CONFIG_FILE_PATH)
        return config["DEFAULT"]["access_token"]
    else:
        return False

