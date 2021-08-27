from django import forms
from auth_app.models import Account


class EditProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = 'Date of Birth (YYYY/MM/DD)'

    class Meta:
        model = Account
        fields = [
            'bio',
            'date_of_birth',
        ]


class SearchProfile(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'username'
        ]


class ChangeProfileImage(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.fields['profile_image'].default = self.instance.profile_image

    class Meta:
        model = Account
        fields = [
            'profile_image',
        ]
