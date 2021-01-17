from django import forms
from django.forms import ModelForm
from .models import Profiles
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class ProfilesForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['country','date_of_birth','facebook_url', 'instagram_url','profile_pic','bio']

        widgets = {
            #'date_of_birth':forms.DateInput(format='readonly'),
            'facebook_url':forms.URLInput(attrs={'id':'facebook_url', 'placeholder': 'Facebook','autocomplete':'off'}),
            'instagram_url':forms.URLInput(attrs={'id':'instagram_url', 'placeholder': "Instagram",'autocomplete':'off'}),
            'bio':forms.Textarea(attrs={'id':'bio', 'placeholder': 'Bio','autocomplete':'off'}),

         }

class UserupdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username"]
