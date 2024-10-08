
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
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "apps", "news-djangocms"))


def remove_wagtail_apps():
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "apps", "home"))
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "apps", "search"))
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "apps", "news-wagtail"))


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
    apps_dir = os.path.join("{{cookiecutter.project_slug}}", "apps")
    if "{{ cookiecutter.cms }}" == "Wagtail":
        remove_django_cms_apps()
        set_wagtail_base_template()
        if {{cookiecutter.include_news_app}}:
            os.rename(os.path.join(apps_dir, "news-wagtail"), os.path.join(apps_dir, "news"))
    if "{{ cookiecutter.cms }}" == "DjangoCMS":
        remove_wagtail_apps()
        set_djangocms_base_template()
        if {{cookiecutter.include_news_app}}:
            os.rename(os.path.join(apps_dir, "news-djangocms"), os.path.join(apps_dir, "news"))
    if "{{ cookiecutter.cms }}" == "None":
        remove_wagtail_apps()
        remove_django_cms_apps()
        shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "templates", "cms"))
    static_path = os.path.join("{{cookiecutter.project_slug}}", "static")
    os.system("git init")
    if {{cookiecutter.add_submodule_bolt}}:
        os.system(f"git submodule add https://github.com/stephband/bolt-2.git {os.path.join(static_path, 'bolt')}")
    if {{cookiecutter.add_submodule_fn}}:
        os.system(f"git submodule add https://github.com/stephband/Fn.git {os.path.join(static_path, 'fn')}")
    if {{cookiecutter.add_submodule_dom}}:
        os.system(f"git submodule add https://github.com/stephband/dom.git {os.path.join(static_path, 'dom')}")
    if {{cookiecutter.add_submodule_slideshow}}:
        os.system(f"git submodule add https://github.com/stephband/slide-show.git {os.path.join(static_path, 'slide-show')}")
    settings_dir = os.path.join("{{cookiecutter.project_slug}}","{{cookiecutter.project_slug}}", "settings")
    shutil.move(os.path.join(settings_dir, "local.py-template"), os.path.join(settings_dir, "local.py"))
    exit_code = os.system("cd {{cookiecutter.project_slug}}")
    if exit_code:
        print("Project generation failed. Cannot cd in {{cookiecutter.project_slug}}")
        return exit_code
    exit_code = os.system("python3.12 -m venv .venv")
    if exit_code:
        print("Project generation failed. Cannot create virtualenv")
        return exit_code
    exit_code = os.system(".venv/bin/python -m pip install --upgrade pip wheel pip-tools")
    if exit_code:
        print("Project generation failed. Cannot install pip-tools")
        return exit_code
    exit_code = os.system(".venv/bin/pip-compile")
    if exit_code:
        print("Project generation failed. Cannot run pip-compile")
        return exit_code
    exit_code = os.system(".venv/bin/pip-sync")
    if exit_code:
        print("Project generation failed. Cannot run pip-sync")
        return exit_code
    exit_code = os.system("cd {{cookiecutter.project_slug}}")
    if exit_code:
        print("Project generation failed. Cannot cd in {{cookiecutter.project_slug}}")
        return exit_code
    exit_code = os.system("createdb {{cookiecutter.project_slug}}")
    if exit_code:
        print("Project generation failed. Cannot create db with name {{cookiecutter.project_slug}}")
        return exit_code
    if exit_code:
        print("Project generation failed. Cannot set domain name in shell_plus")
        return exit_code
    exit_code = os.system(".venv/bin/python {{cookiecutter.project_slug}}/manage.py migrate")
    if exit_code:
        print("Project generation failed. Cannot run migrate")
        return exit_code
    exit_code = os.system("echo \"Site.objects.all().update(domain='{{cookiecutter.domain_name}}')\" | .venv/bin/python {{cookiecutter.project_slug}}/manage.py shell_plus")
    if exit_code:
        print("Project generation failed. Cannot set domain name in shell_plus")
        return exit_code
    exit_code = os.system("echo \"User.objects.create_superuser('info@cruncher.ch','admin' )\" | .venv/bin/python {{cookiecutter.project_slug}}/manage.py shell_plus")
    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)

if __name__ == "__main__":
    main()
