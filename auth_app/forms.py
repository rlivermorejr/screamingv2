from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth_app.models import Account


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            'username',
            'password1',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off'}), max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
