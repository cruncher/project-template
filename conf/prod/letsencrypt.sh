./letsencrypt-auto certonly \
    --email marco@cruncher.ch \
    --fullchain-path /home/projects/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/conf/prod/ssl/fullchain.pem \
    --key-path /home/projects/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/conf/prod/ssl/privkey.pem \
    --webroot -w /home/projects/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/conf/prod/ssl/webroot/ \
    -d {{cookiecutter.project_slug}}.com -d www.{{cookiecutter.project_slug}}.com -d {{cookiecutter.project_slug}}.cruncher.ch
