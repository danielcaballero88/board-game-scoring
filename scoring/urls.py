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
    path("table/close/<int:table_pk>/", views.table_close, name="table_close"),
    path("table/reopen/<int:table_pk>/", views.table_reopen, name="table_reopen"),
    path(
        "score/create/<int:table_pk>/",
        views.score_create_ot_player,
        name="score_create_ot_player",
    ),
    path(
        "score/delete/<int:table_pk>/<str:playername>/",
        views.score_delete,
        name="score_delete",
    ),
    path(
        "score/edit/<int:table_pk>/<str:playername>/",
        views.score_edit,
        name="score_edit",
    ),
    path(
        "score/create-self/<int:table_pk>/",
        views.score_create_self,
        name="score_create_self",
    ),
]
