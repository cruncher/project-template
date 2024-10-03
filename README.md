# Getting started

```
export NEW_PROJECT_NAME=fancy_new_project
cookiecutter gh:cruncher/project-template
cd {{cookiecutter.project_slug}}
~/.pyenv/versions/3.11.*/bin/python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel pip-tools
pip-compile
pip-sync
cd {{cookiecutter.project_slug}}
createdb {{cookiecutter.project_slug}}


cp {{cookiecutter.project_slug}}/settings/local.py-template {{cookiecutter.project_slug}}/settings/local.py

python manage.py migrate
python manage.py createsuperuser

```

# Resources


# Local project setup
```
git clone git@github.com:cruncher/{{cookiecutter.project_slug}}.git
cd {{cookiecutter.project_slug}}
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel pip-tools
pip-compile
pip-sync
cd {{cookiecutter.project_slug}}
git submodule update --init
createdb {{cookiecutter.project_slug}}
python manage.py migrate
cp {{cookiecutter.project_slug}}/settings/local.py-template {{cookiecutter.project_slug}}/settings/local.py
python manage.py runserver
```

# {{cookiecutter.project_slug}}

`https://{{cookiecutter.project_slug}}.ch/` – prod

`https://{{cookiecutter.project_slug}}.cruncher.ch/` – staging
