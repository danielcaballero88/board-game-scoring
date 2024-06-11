from django.urls import path

from . import views

app_name = "scoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("games/list/", views.games_list, name="games_list"),
    path("game/like/<int:game_pk>/", views.game_like, name="game_like"),
    path("tables/list/", views.tables_list, name="tables_list"),
]
