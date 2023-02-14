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

TODO:
-   Popular repositories(based on Stars/Fork/Clone)  
-   Add testing.  
-   Add Personal Access Token authentication.  
-   Add a web server(Flask) for browser-based Git operations.  
