import random
import string

from fabric.api import cd, env, local, prefix, settings
from fabric.operations import run


BASE_DIR = "/home/projects/{{project_name}}/{{project_name}}"
CODE_DIR = BASE_DIR + "/{{project_name}}"

env.hosts = ["{{project_name}}@{{project_name}}.cruncher.ch"]
env.activate = f"source {BASE_DIR}/.venv/bin/activate"
env.remote_db = "{{project_name}}"
env.local_db = "{{project_name}}"
env.git_branch = "master"
env.gunicorn_process = "{{project_name}}_gunicorn"
env.forward_agent = True


def migrate(do_reload=True):
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run("python manage.py migrate")
    if do_reload:
        reload_server()


def collectstatic():
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run("python manage.py collectstatic --noinput")


def pull_code():
    with (cd(BASE_DIR)):
        run(f"git pull origin {env.git_branch}")
        run("git submodule update --init --recursive")


def commit_push():
    with (cd(BASE_DIR)):
        git_commit()
        git_push()


def git_commit():
    with (cd(BASE_DIR)):
        run('git commit -am "dunno"')


def git_push():
    with (cd(BASE_DIR)):
        run(f"git push origin {env.git_branch}")


def reload_server():
    run(f"sudo supervisorctl restart {env.gunicorn_process}")


def clear_cache():
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run("python manage.py clear_cache")


def load():
    run("w")
    run("df -h")


def compilemessages(do_reload=True):
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run("python manage.py compilemessages")
    if do_reload:
        reload_server()


def requirements():
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run("pip install -q -r ../requirements.txt")


def local_git_pull():
    local(f"git pull origin {env.git_branch}")


def local_git_push():
    local(f"git push origin {env.git_branch}")


def fix_cms():
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run("python manage.py cms fix-tree")


def build_static():
    local("rm -f static/build/*.js")
    with settings(warn_only=True):
        # local("node --experimental-json-modules ./build.js")
        local("make literal site")
        local(f"rsync -avz -e ssh static/build {env.hosts[0]}:{BASE_DIR}/tmp/static/")


def deploy():
    local_git_pull()
    cache_buster = generate_cache_buster()
    build_static()
    pull_code()
    requirements()
    migrate(False)
    crontab()
    # build_styleguide(False)
    collectstatic()
    clear_cache_buster(cache_buster)
    compilemessages(False)
    reload_server()
    # fix_cms()


def crontab():
    with (cd(BASE_DIR)):
        run("crontab {}/conf/prod/crontab".format(BASE_DIR))
        run("crontab -l")


def ssh():
    with (cd(CODE_DIR)):
        run("bash")


def version():
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run("python manage.py --version")


def clear_cache_buster(cache_buster):
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run(f"python manage.py clear_cache_buster --buster={cache_buster}")


def generate_cache_buster():
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(9)
    )


def get_remote_db():
    with (cd(CODE_DIR)):
        with prefix(env.activate):
            run(f"pg_dump -f ~/backup/{env.remote_db}.dmp {env.remote_db}")
    local(f"rsync -avz -e ssh {env.hosts[0]}:backup/{env.remote_db}.dmp .")


def sync_get():
    get_remote_db()
    local(f"dropdb {env.local_db}")
    local(f"createdb -E utf8 {env.local_db}")
    local(f"psql -q -d {env.local_db} -f {env.remote_db}.dmp")
    local(f'rm {env.remote_db}.dmp')
    local("python manage.py migrate")
    local('python manage.py set_fake_passwords --password="admin"')
    local(
        "echo \"Site.objects.all().update(domain='127.0.0.1:8000')\" "
        "| python manage.py shell_plus"
    )
