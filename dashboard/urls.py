from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.index),
    path('server/account/create', views.server_account_create)
]
