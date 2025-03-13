from django.urls import path
from .views import *

urlpatterns = [
    path('sheet-music-list/', view=ListFlatSheetMusic.as_view(), name="sheet_music_list"),
    path('sheet-music-create/', view=CreateFlatSheetMusic.as_view(), name="sheet_music_create"),
    path('sheet-music-delete/<str:slug>', view=DeleteFlatSheetMusic.as_view(), name="sheet_music_delete"),
    path('sheet-music-update/<str:slug>', view=UpdateFlatSheetMusic.as_view(), name="sheet_music_update"),
    path('groups-list/', view=ListFlatSheetMusic.as_view(), name="groups_list"),
    path('groups-create/', view=CreateFlatSheetMusic.as_view(), name="groups_create"),
    path('groups-delete/<int:pk>', view=DeleteFlatSheetMusic.as_view(), name="groups_delete"),
    path('groups-update/<int:pk>', view=UpdateFlatSheetMusic.as_view(), name="groups_update"),
    path('home/<str:slug>', view=HomeView.as_view(), name="home"),
]
