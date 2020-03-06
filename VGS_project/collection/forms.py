from collection.models import UserData
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django import forms

class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

class UserLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class ChangeAvatarForm(forms.ModelForm):

    class Meta:
        model = UserData
        fields = ["profil_picture"]
        widgets = {
            "profil_picture": forms.FileInput(attrs={"class": "form-control"}),
        }

class ParagraphErrorList(ErrorList):

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ""
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])
