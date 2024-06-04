from django.contrib import admin

from .models import Game, Genre, Player, Score, ScoringCategory, Table


class ScoringCategoryInLine(admin.TabularInline):
    model = ScoringCategory
    extra = 1


class GameGenreRelationshipInline(admin.TabularInline):
    model = Game.genres.through
    extra = 1


class GenreAdmin(admin.ModelAdmin):
    inlines = [GameGenreRelationshipInline]


class GameAdmin(admin.ModelAdmin):
    inlines = [ScoringCategoryInLine, GameGenreRelationshipInline]
    exclude = ["genres"]


admin.site.register(Game, GameAdmin)
admin.site.register(Genre, GenreAdmin)


class TablePlayersInLine(admin.TabularInline):
    model = Table.players.through
    extra = 3
    verbose_name = "Player"
    verbose_name_plural = "Players"


class TableWinnerInline(admin.TabularInline):
    model = Player


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 10


class TableAdmin(admin.ModelAdmin):
    inlines = [TablePlayersInLine, ScoreInline]
    exclude = ["players"]


admin.site.register(Table, TableAdmin)


class FavoriteGamesInline(admin.TabularInline):
    model = Player.favorite_games.through
    extra = 1
    verbose_name = "Favorite Game"
    verbose_name_plural = "Favorite Games"


class PlayerAdmin(admin.ModelAdmin):
    inlines = [FavoriteGamesInline]
    exclude = ["favorite_games"]


admin.site.register(Player, PlayerAdmin)
