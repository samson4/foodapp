from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from . models import Comment,rregister,Address

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('review','rating',)
        Widgets={
            'review': forms.Textarea(attrs={'class':'form-control'}),
            'rating': forms.Textarea(attrs={'class':'form-control'}),
        }


class RestaurantRegisterForm(forms.Form):

    # class Meta:
    #     model = User
        choice=(
        ('OPEN','OPEN'),
        ('CLOSED','CLOSED')
        )

        restaurant_name=forms.CharField()
        password=forms.CharField(widget=forms.PasswordInput())
        phone=forms.IntegerField()
        Bio=forms.CharField(max_length=100000)
        email= forms.EmailField()
        location=forms.CharField(label='Accurate Location')
        status=forms.ChoiceField(choices=choice)
        
        # fields = ('restaurant_name','restaurant_logo','phone','email','status')  

