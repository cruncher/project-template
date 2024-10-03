
import os
import random
import shutil

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


def set_wagtail_base_template():
    cms_template_dir = os.path.join("{{cookiecutter.project_slug}}", "templates", "cms")
    shutil.move(
            os.path.join(cms_template_dir, "wagtail_base.html"),
            os.path.join(cms_template_dir, "base.html")
        )
    os.remove(os.path.join(cms_template_dir, "djangocms_base.html"))
    shutil.rmtree(os.path.join(cms_template_dir, "plugins"))
    shutil.rmtree(os.path.join(cms_template_dir, "snippets"))


def set_djangocms_base_template():
    cms_template_dir = os.path.join("{{cookiecutter.project_slug}}", "templates", "cms")
    shutil.move(
        os.path.join(cms_template_dir, "djangocms_base.html"),
        os.path.join(cms_template_dir, "base.html")
    )
    os.remove(os.path.join(cms_template_dir, "wagtail_base.html"))



def main():
    if "{{ cookiecutter.cms }}" == "Wagtail":
        remove_django_cms_apps()
        set_wagtail_base_template()
    if "{{ cookiecutter.cms }}" == "DjangoCMS":
        remove_wagtail_apps()
        set_djangocms_base_template()
    if "{{ cookiecutter.cms }}" == "None":
        remove_wagtail_apps()
        remove_django_cms_apps()
        shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "templates", "cms"))


    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
