from django import forms
from .models import Location, Shoe, Activity

class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude']


class ActivityCreateForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Activity
        fields = ['location', 'shoe', 'sport', 'notes']

class ShoeCreateForm(forms.ModelForm):
    class Meta:
        model = Shoe
        fields = ['manufacturer', 'brand']

