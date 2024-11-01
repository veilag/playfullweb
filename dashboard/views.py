import subprocess

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required
def index(request: HttpRequest):
    return render(request, "dashboard/index.html")


@login_required
def server_account_create(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pass1')

        create_linux_user(username, password)
        configure_nginx(username)

    return render(request, "dashboard/server_user_create.html")


def create_linux_user(username, password):
    subprocess.run(['sudo', 'adduser', username, '--gecos', '""', '--disabled-password'])
    subprocess.run(['sudo', 'chpasswd'], input=f'{username}:{password}'.encode())


def configure_nginx(username):
    nginx_conf = f"""
server {{
    listen 8000;
    server_name {username}.example.com;

    location = /favicon.ico {{ access_log off; log_not_found off; }}
    location / {{
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
}}
"""
    with open(f'/etc/nginx/sites-available/{username}.conf', 'w') as conf_file:
        conf_file.write(nginx_conf)
    subprocess.run(['sudo', 'ln', '-s', f'/etc/nginx/sites-available/{username}.conf', f'/etc/nginx/sites-enabled/{username}.conf'])
    subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])
