from django.urls import path

from . import views

app_name = "scoring"
urlpatterns = [
    path("", views.landing, name="landing"),
]
