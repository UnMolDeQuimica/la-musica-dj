from django.forms import ModelForm
from .models import Group, FlatSheetMusic

class CreateFlatSheetMusicForm(ModelForm):
    class Meta:
        model = FlatSheetMusic
        exclude = ["uuid", "slug"]


class CreateGroupForm(ModelForm):
    class Meta:
        model = Group
        exclude = ["slug",]