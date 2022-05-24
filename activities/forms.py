from django import forms
from .models import Location

class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name',]


class ActivityCreateForm(forms.Form):
    SPORTS = [
        ('running', 'Running'),
        ('biking', 'Biking'),
        ('hiking', 'Hiking'),
    ]
    location = forms.ModelChoiceField(queryset = Location.objects.all())
    sport = forms.ChoiceField(choices=SPORTS)
    notes = forms.CharField(max_length = 255)
    file = forms.FileField()

