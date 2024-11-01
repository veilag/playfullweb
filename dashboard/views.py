from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required
def index(request: HttpRequest):
    return render(request, "dashboard/index.html")


@login_required
def server_account_create(request: HttpRequest):
    return render(request, "dashboard/server_user_create.html")
