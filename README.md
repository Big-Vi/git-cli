Python CLI for interacting with GitHub using GraphQL API.


## To setup local development

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools
pip install -r requirements/dev.in && pip install -e .
pip install coverage
coverage run -m pytest
coverage html


```

Open ``htmlcov/index.html`` in your browser to explore the report.

`pip-compile-multi` -> to compile multiple requirements files to lock dependency version.

## How login with GitHub works

-   When you run `git-cli login`, an application sends an request to `https://github.com/login/device/code` to get the user verification code and sends the user to authorization URL(`https://github.com/login/device`) where the user will enter the verification code.
-   The app continuously polls this URL(`https://github.com/login/oauth/access_token`) to get an access token once the user authorized the device. An access token gets stored in `.git-cli` config file on your computer.
-   The app uses this access token to query(GraphQL) your GitHub repository.


## TODO:

-   Popular repositories(based on Stars/Fork/Clone)  
-   Add testing.  
-   Add Personal Access Token authentication.  
-   Add a web server(Flask) for browser-based Git operations.  
