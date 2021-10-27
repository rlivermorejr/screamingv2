from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth_app.models import Account


class CreateUserForm(UserCreationForm):
    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        username = cleaned_data.get('username')
        if username and Account.objects.filter(username__iexact=username).exists():
            self.add_error(
                'username', 'A user with that username already exists.')
        return cleaned_data

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
