#!/bin/sh

set -x  # Print each command before executing it


BASE_DIR=`pwd`

mkdir .test_tmp
cd .test_tmp
mkdir test_project
cd test_project

PROJECT_DIR=`pwd`

export NEW_PROJECT_NAME=test_create_from_project_template
export DJANGO_SETTINGS_MODULE=$NEW_PROJECT_NAME.settings.test
export PGPASSWORD=postgres

pip install django

test_installation() {
    django-admin startproject --template=https://github.com/cruncher/project-template/zipball/2024/test-installation --extension=conf,py,sh,py-template,toml  $NEW_PROJECT_NAME
    cd $NEW_PROJECT_NAME
    sed -i s/{{project_name}}/$NEW_PROJECT_NAME/g $NEW_PROJECT_NAME/templates/base.html
    return
}
test_create_virtualenv() {
    cd $PROJECT_DIR
    python -m venv .venv
    ls -la | grep .venv
    return
}
test_activate_virtualenv() { 
    PWD=`pwd`
    . $PWD/.venv/bin/activate
    return
}

test_pip() {
    cd $NEW_PROJECT_NAME
    pip install --upgrade pip wheel pip-tools
    pip-compile
    pip-sync
    return
}
test_db() {
    cd $NEW_PROJECT_NAME
    if ! createdb -h localhost -p 5432 -U postgres -w $NEW_PROJECT_NAME; then
    dropdb -h localhost -p 5432 -U postgres -w $NEW_PROJECT_NAME
    createdb -h localhost -p 5432 -U postgres -w $NEW_PROJECT_NAME
    fi
}

test_cp_local() {
    cp $NEW_PROJECT_NAME/settings/local.py-template $NEW_PROJECT_NAME/settings/local.py
    return
}

test_django_check() {
    python manage.py check --fail-level WARNING
    return
}

test_migrate() {
    python manage.py migrate
    return
}

test_installation && test_create_virtualenv && test_activate_virtualenv && test_activate_virtualenv && test_pip && test_db  && test_cp_local && test_django_check && test_migrate
