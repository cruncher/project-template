#!/bin/sh

set -x  # Print each command before executing it


BASE_DIR=`pwd`

mkdir .test_tmp
cd .test_tmp
mkdir test_project
cd test_project

PROJECT_DIR=`pwd`


test_installation() {
    export NEW_PROJECT_NAME=test_create_from_project_template
    ~/.pyenv/versions/3.11.*/bin/django-admin startproject --template=https://github.com/cruncher/project-template/zipball/master --extension=conf,py,sh,py-template,toml  $NEW_PROJECT_NAME
    cd $NEW_PROJECT_NAME
    sed -i s/{{project_name}}/$NEW_PROJECT_NAME/g $NEW_PROJECT_NAME/templates/base.html
    return
}
test_create_virtualenv() {
    cd $PROJECT_DIR
    ~/.pyenv/versions/3.11.*/bin/python -m venv .venv
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
    if ! createdb $NEW_PROJECT_NAME; then
    dropdb $NEW_PROJECT_NAME
    createdb $NEW_PROJECT_NAME
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

if ! test_installation || ! test_create_virtualenv || ! test_activate_virtualenv || ! test_activate_virtualenv || ! test_pip || ! test_db  || ! test_cp_local || ! test_django_check || ! test_migrate; then
    dropdb $NEW_PROJECT_NAME
    cd $BASE_DIR
    rm -rf .test_tmp/
    return
fi

dropdb $NEW_PROJECT_NAME
cd $BASE_DIR
rm -rf .test_tmp/
