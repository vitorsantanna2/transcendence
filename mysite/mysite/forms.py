# forms.py
from django import forms
from .models import UserPong

class UserPongForm(forms.ModelForm):
    class Meta:
        model = UserPong
        fields = ['profile_image']  # or other fields you want to include
