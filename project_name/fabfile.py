from fabric.api import run, cd, env, prefix, local

BASE_DIR = '/home/projects/{{project_name}}/{{project_name}}'
TEMPLATES_DIR = '%s/res' % BASE_DIR
CODE_DIR = BASE_DIR + '/{{project_name}}'

env.hosts = ['{{project_name}}@{{project_name}}.cruncher.ch']
env.activate = 'source %s/bin/activate' % BASE_DIR


def migrate():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('python manage.py migrate')


def collectstatic():
    with(cd(CODE_DIR)):
        with prefix(env.activate):
            run('python manage.py collectstatic --noinput')



def pull_code():
    with(cd(BASE_DIR)):
        run('git pull origin master')
        run('git submodule init')
        run('git submodule update')
        run('git submodule foreach git pull origin master')


def reload_server():
    run('sudo supervisorctl restart {{project_name}}_gunicorn')


def deploy():
    pull_code()
    collectstatic()
    reload_server()
