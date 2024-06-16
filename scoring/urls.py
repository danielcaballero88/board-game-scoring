from django.urls import path

from . import views

app_name = "scoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("games/list/", views.games_list, name="games_list"),
    path("game/like/<int:game_pk>/", views.game_like, name="game_like"),
    path("game/<int:game_pk>/", views.game_detail, name="game_detail"),
    path("tables/list/", views.tables_list, name="tables_list"),
    path("table/create/<int:game_pk>/", views.table_create, name="table_create"),
    path("table/<int:table_pk>/", views.table_detail, name="table_detail"),
    path("score/create/<int:table_pk>/", views.score_create, name="score_create"),
]
