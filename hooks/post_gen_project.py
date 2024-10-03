
import json
import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_django_cms_apps():
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "apps", "news"))


def remove_wagtail_apps():
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "apps", "home"))
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "apps", "search"))

def main():
    if "{{ cookiecutter.cms }}" == "Wagtail":
        remove_django_cms_apps()
    if "{{ cookiecutter.cms }}" == "DjangoCMS":
        remove_wagtail_apps()
    if "{{ cookiecutter.cms }}" == "None":
        remove_wagtail_apps()
        remove_django_cms_apps()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
