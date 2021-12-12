from django import forms
from auth_app.models import Account
from django_countries.fields import CountryField


class EditProfile(forms.Form):
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'width:50%;height:100px;'}), label="")
    header = forms.CharField(max_length=80)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            format='%m/%d/%Y', attrs={'class': 'datepicker'}),
        input_formats=('%m/%d/%Y', )
    )
    location = forms.CharField(max_length=40)

###############################################################################
    # class PersonForm(forms.ModelForm):

    # class Meta:
    #     model = models.Person
    #     fields = ('name', 'country')
    #     widgets = {'country': CountrySelectWidget()}

# class for searching for users
# class SearchProfile(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = [
#             'username'
#         ]
###############################################################################


class ChangeProfileImage(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChangeProfileImage, self).__init__(*args, **kwargs)
        self.fields['profile_image'].default = self.instance.profile_image

    class Meta:
        model = Account
        fields = [
            'profile_image',
        ]
