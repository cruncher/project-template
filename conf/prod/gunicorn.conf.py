import multiprocessing

backlog = 2048
daemon = False
debug = False
spew = False
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 500
bind = "unix:/home/projects/{{project_name}}/{{project_name}}/tmp/gunicorn.sock"
pidfile = "/home/projects/{{project_name}}/{{project_name}}/tmp/gunicorn.pid"
logfile = "/home/projects/{{project_name}}/{{project_name}}/logs/gunicorn.log"
loglevel = "error"
user = "{{project_name}}"
proc_name = "{{project_name}}"
timeout = 60
