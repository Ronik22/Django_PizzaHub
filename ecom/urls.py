from django.contrib import admin
from django.urls import path, include
from .views import home, menu

urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu, name="menu"),
]