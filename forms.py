from django import forms
from .models import Station


class StationDatesForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'mindate', 'maxdate']
