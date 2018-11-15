from fabric.api import run, cd, env, prefix, local

BASE_DIR = '/home/projects/{{project_name}}/{{project_name}}'
TEMPLATES_DIR = '%s/res' % BASE_DIR
CODE_DIR = BASE_DIR + '/{{project_name}}'

env.hosts = ['{{project_name}}@{{project_name}}.cruncher.ch']
env.activate = 'source %s/.venv/bin/activate' % BASE_DIR
env.remote_db = '{{project_name}}'
env.local_db = '{{project_name}}'
env.git_branch = 'master'
env.gunicorn_process = '{{project_name}}_gunicorn'
env.forward_agent = True


def migrate():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('python manage.py migrate')
    reload_server()


def collectstatic():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('python manage.py collectstatic --noinput')


def pull_code():
    with(cd(BASE_DIR)):
        run('git pull origin %s' % env.git_branch)
        run('git submodule update --init --recursive')


def commit_push():
    with(cd(BASE_DIR)):
        git_commit()
        git_push()


def git_commit():
    with(cd(BASE_DIR)):
        run('git commit -am "dunno"')


def git_push():
    with(cd(BASE_DIR)):
        run('git push origin %s' % env.git_branch)


def reload_server():
    run('sudo supervisorctl restart %s' % env.gunicorn_process)


def clear_cache():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('python manage.py clear_cache')


def load():
    run('w')


def compilemessages(do_reload=True):
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('python manage.py compilemessages')
    if do_reload:
        reload_server()


def requirements():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('pip install -r ../requirements.txt')


def deploy():
    pull_code()
    collectstatic()
    compilemessages(False)
    reload_server()


def crontab():
    with(cd(BASE_DIR)):
        run('crontab {}/conf/prod/crontab'.format(BASE_DIR))
        run('crontab -l')


def ssh():
    with(cd(CODE_DIR)):
        run('bash')


def version():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('python manage.py --version')


def sync_get():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('pg_dump -f ~/backup/%s.dmp %s' % (env.remote_db, env.remote_db))
    local('scp %s:backup/%s.dmp .' % (env.hosts[0], env.remote_db))
    local('rsync -avz -e ssh %s:%s/tmp/media/ ../tmp/media/' % (env.hosts[0], BASE_DIR))
    local('dropdb %s' % env.local_db)
    local('createdb -E utf8 %s' % env.local_db)
    local('psql -q -d %s -f %s.dmp' % (env.local_db, env.remote_db))
    local('rm -f %s.dmp %s.dmp.lst' % (env.remote_db, env.remote_db))
    local('python manage.py migrate')
    local('python manage.py set_fake_passwords --password="admin"')
