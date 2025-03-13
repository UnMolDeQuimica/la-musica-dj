from django.contrib import admin

from .models import Group, User, FlatSheetMusic


@admin.register(User)
class UserAdmin(admin.ModelAdmin): ...


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin): ...


@admin.register(FlatSheetMusic)
class FlatSheetMusicAdmin(admin.ModelAdmin): ...
