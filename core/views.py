from django.http import HttpRequest
from django.shortcuts import redirect


def index(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/register")
