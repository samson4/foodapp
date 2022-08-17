from tkinter import Widget
from tokenize import group
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from blog.models import rregister



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name=forms.CharField()

    class Meta:
        model = User
        fields = ['name','username', 'email', 'password1', 'password2']
        


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    location=forms.TextInput()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

     
