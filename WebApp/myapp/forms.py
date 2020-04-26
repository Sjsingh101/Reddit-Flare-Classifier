from django import forms

class NameForm(forms.Form):
    url = forms.CharField(label='url')