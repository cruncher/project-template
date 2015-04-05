#!/bin/bash
virtualenv --no-site-packages --distribute .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
git submodule update --init --recursive
cd {{project_name}}
createdb {{project_name}}
python manage.py collectstatic --noinput
python manage.py syncdb
