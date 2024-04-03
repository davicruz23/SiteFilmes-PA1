from django import forms
from .models import MyProfile

class MyProfileForm(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = ['description', 'dataDeNascimento', 'fotoPerfil']
