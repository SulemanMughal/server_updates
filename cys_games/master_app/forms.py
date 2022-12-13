from django import forms

from django.contrib.auth import get_user_model
User  = get_user_model()



# ? User Login Form
class loginForm(forms.Form):
    email = forms.EmailField(label='Email Address', widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
