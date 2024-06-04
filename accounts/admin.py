from django.contrib import admin

from scoring.models import Player

from .models import AppUser


class PlayerInLine(admin.TabularInline):
    model = Player
    extra = 1


class AppUserAdmin(admin.ModelAdmin):
    inlines = [PlayerInLine]


admin.site.register(AppUser, AppUserAdmin)
