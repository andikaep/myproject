# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']

class PlaceOfBirthForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['provinsi', 'kabupaten', 'kecamatan', 'kelurahan']

    provinsi = forms.ChoiceField(choices=[], required=True)
    kabupaten = forms.ChoiceField(choices=[], required=False)
    kecamatan = forms.ChoiceField(choices=[], required=False)
    kelurahan = forms.ChoiceField(choices=[], required=False)