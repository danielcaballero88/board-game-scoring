from django.urls import path

from . import views

app_name = "static_pages"
urlpatterns = [
    path("", views.landing, name="landing"),
]
