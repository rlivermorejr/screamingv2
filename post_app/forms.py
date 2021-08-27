from django import forms


class ScreamForm(forms.Form):
    content = forms.CharField(
        max_length=200, label='')


class CommentForm(forms.Form):
    content = forms.CharField(max_length=140)
