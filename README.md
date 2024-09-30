# Getting started

```
export NEW_PROJECT_NAME=fancy_new_project
django-admin startproject --template=https://github.com/halitcelik/project-template/zipball/master --extension=conf,py,sh,py-template,toml  $NEW_PROJECT_NAME
cd $NEW_PROJECT_NAME
sed -i s/{{cookiecutter.project_slug}}/$NEW_PROJECT_NAME/g $NEW_PROJECT_NAME/templates/base.html
git init
~/.pyenv/versions/3.11.*/bin/python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel pip-tools
pip-compile
pip-sync
cd $NEW_PROJECT_NAME
createdb $NEW_PROJECT_NAME
git submodule add   git@github.com:stephband/bolt-2.git static/bolt
git submodule add   git@github.com:stephband/Fn.git static/fn
git submodule add   git@github.com:stephband/dom.git static/dom

cp $NEW_PROJECT_NAME/settings/local.py-template $NEW_PROJECT_NAME/settings/local.py

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
