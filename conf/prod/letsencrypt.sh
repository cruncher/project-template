./letsencrypt-auto certonly \
    --email marco@cruncher.ch \
    --fullchain-path /home/projects/{{project_name}}/{{project_name}}/conf/prod/ssl/fullchain.pem \
    --key-path /home/projects/{{project_name}}/{{project_name}}/conf/prod/ssl/privkey.pem \
    --webroot -w /home/projects/{{project_name}}/{{project_name}}/conf/prod/ssl/webroot/ \
    -d {{project_name}}.com -d www.{{project_name}}.com -d {{project_name}}.cruncher.ch
