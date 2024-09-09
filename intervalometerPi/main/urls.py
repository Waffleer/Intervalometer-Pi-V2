from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("running", views.running, name="running"),
    path("clicking", views.clicking, name="clicking")
]
