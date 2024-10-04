
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
    static_path = os.path.join("{{cookiecutter.project_slug}}", "static")
    os.system("git init")
    if {{cookiecutter.add_submodule_bolt}}:
        
        os.system(f"git submodule add git@github.com:stephband/bolt-2.git {os.path.join(static_path, 'bolt')}")
    if {{cookiecutter.add_submodule_fn}}:
        os.system(f"git submodule add git@github.com:stephband/Fn.git {os.path.join(static_path, 'fn')}")
    if {{cookiecutter.add_submodule_dom}}:
        os.system(f"git submodule add git@github.com:stephband/dom.git {os.path.join(static_path, 'dom')}")
    if {{cookiecutter.add_submodule_slideshow}}:
        os.system(f"git submodule add git@github.com:stephband/slide-show.git {os.path.join(static_path, 'slide-show')}")
    settings_dir = os.path.join("{{cookiecutter.project_slug}}","{{cookiecutter.project_slug}}", "settings")

    shutil.move(os.path.join(settings_dir, "local.py-template"), os.path.join(settings_dir, "local.py"))

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)
    print(HINT + "A git repository is already created. You can continue with:" + TERMINATOR)
    print(HINT + "- Creating a virtual environment" + TERMINATOR)
    print(HINT + "- Installing requirements" + TERMINATOR)
    print(HINT + "- Creating a database" + TERMINATOR)
    print("cd {{cookiecutter.project_slug}}")
    print("~/.pyenv/versions/3.11.*/bin/python -m venv .venv")
    print("source .venv/bin/activate")
    print("pip install --upgrade pip wheel pip-tools")
    print("pip-compile")
    print("pip-sync")
    print("cd {{cookiecutter.project_slug}}")
    print("createdb {{cookiecutter.project_slug}}")
    print("python manage.py migrate")
    print("python manage.py createsuperuser")


if __name__ == "__main__":
    main()
