from tkinter import Widget
from django import forms  
from . models import Comment,rregister

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('review',)  
        Widgets={
            'review': forms.Textarea(attrs={'class':'form-control'}),

        }


class RestaurantRegisterForm(forms.ModelForm):
    class Meta:
        model = rregister
        fields = ('restaurant_name','restaurant_logo','phone','email','location',)  

# class CustomerRegisterForm(forms.ModelForm):
#     class Meta:
#         model = register
#         fields = ('customer_name','image','phone','email','location',)         
  