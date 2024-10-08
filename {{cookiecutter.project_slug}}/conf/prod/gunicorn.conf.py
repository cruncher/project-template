import multiprocessing

backlog = 2048
daemon = False
debug = False
spew = False
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 450
max_requests_jitter = 50
bind = "unix:/home/projects/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/tmp/gunicorn.sock"
pidfile = "/home/projects/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/tmp/gunicorn.pid"
logfile = "/home/projects/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/logs/gunicorn.log"
loglevel = "error"
user = "{{cookiecutter.project_slug}}"
proc_name = "{{cookiecutter.project_slug}}"
timeout = 60
