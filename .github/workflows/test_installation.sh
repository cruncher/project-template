#!/bin/sh

set -x  # Print each command before executing it


BASE_DIR=`pwd`

mkdir .test_tmp
cd .test_tmp
mkdir test_project
cd test_project

PROJECT_DIR=`pwd`

export NEW_PROJECT_NAME=test_create_from_project_template
export DJANGO_SETTINGS_MODULE=test_create_from_project_template.settings.test
export PGPASSWORD=postgres

pip install django
pip install pytest-cookies
test_installation() {
    pytest
}
test_installation