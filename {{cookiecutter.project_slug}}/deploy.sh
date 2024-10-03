#!/bin/bash
virtualenv --no-site-packages --distribute .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
git submodule add --  https://github.com/stephband/bolt.git {{cookiecutter.project_slug}}/static/bolt
git submodule update --init --recursive
cd {{cookiecutter.project_slug}}
createdb {{cookiecutter.project_slug}}
python manage.py collectstatic --noinput
python manage.py syncdb
mkdir -p ../tmp/media
mkdir /var/tmp/letsencrypt-auto

cd
mkdir -p backup
(crontab -l ; echo "@daily ~/{{cookiecutter.project_slug}}/.venv/bin/python ~/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/manage.py clearsessions") | crontab -
(crontab -l ; echo "@daily pg_dump -f ~/backup/{{cookiecutter.project_slug}}.sql {{cookiecutter.project_slug}}") | crontab -

cd {{cookiecutter.project_slug}}/conf/prod
echo
echo "sudo ln -s $PWD/supervisord.gunicorn.conf /etc/supervisord.d/{{cookiecutter.project_slug}}.conf"
echo "sudo ln -s $PWD/nginx.conf /etc/nginx/sites-enabled/{{cookiecutter.project_slug}}.conf"
echo "sudo supervisorctl update"
echo "sudo service nginx configtest"
echo
cd
