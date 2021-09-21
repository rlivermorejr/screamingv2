from django import forms
from auth_app.models import Account
from django_countries.fields import CountryField
from django.conf import settings

DATE_INPUT_FORMATS = ['%m/%d/%Y']


class EditProfile(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(EditProfile, self).__init__(*args, **kwargs)
    #     self.fields['date_of_birth'].label = 'Date of Birth (YYYY/MM/DD)'
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:50%;height:100px;'}), label="")
    header = forms.CharField(max_length=80)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            format='%m/%d/%Y', attrs={'class': 'datepicker'}),
        input_formats=('%m/%d/%Y', )
    )
    country = CountryField().formfield()

    # class Meta:
    #     model = Account
    #     fields = [
    #         'bio',
    #         'date_of_birth',
    #         'country'
    #     ]

    # class PersonForm(forms.ModelForm):

    # class Meta:
    #     model = models.Person
    #     fields = ('name', 'country')
    #     widgets = {'country': CountrySelectWidget()}


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
