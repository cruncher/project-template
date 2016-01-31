#!/bin/bash
virtualenv --no-site-packages --distribute .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
git submodule add --  https://github.com/stephband/bolt.git {{project_name}}/static/bolt
git submodule update --init --recursive
cd {{project_name}}
createdb {{project_name}}
python manage.py collectstatic --noinput
python manage.py syncdb
mkdir -p ../tmp/media
mkdir /var/tmp/letsencrypt-auto

cd
mkdir -p backup
(crontab -l ; echo "@daily ~/{{project_name}}/.venv/bin/python ~/{{project_name}}/{{project_name}}/manage.py clearsessions") | crontab -
(crontab -l ; echo "@daily pg_dump -f ~/backup/{{project_name}}.sql {{project_name}}") | crontab -

cd {{project_name}}/conf/prod
echo
echo "sudo ln -s $PWD/supervisord.gunicorn.conf /etc/supervisord.d/{{project_name}}.conf"
echo "sudo ln -s $PWD/nginx.conf /etc/nginx/sites-enabled/{{project_name}}.conf"
echo "sudo supervisorctl update"
echo "sudo service nginx configtest"
echo
cd
