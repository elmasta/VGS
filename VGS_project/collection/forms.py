from collection.models import UserData, UserOwnedGame, Games, Compilation,\
    UserOwnedCompilation
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

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}))

class SearchGameForm(forms.ModelForm):

    class Meta:
        model = Games
        fields = ["name"]
        labels = {"name": "Choisissez un jeu"}
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "list": "games",
                "placeholder": "Recherche de jeux",
                "size": "200"
            }),
        }

class SearchCompilationForm(forms.ModelForm):

    class Meta:
        model = Compilation
        fields = ["name"]
        labels = {"name": "Choisissez une compilation"}
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "list": "compil",
                "placeholder": "Recherche de compilation",
                "size": "200"
            }),
        }

class ChangeAvatarForm(forms.ModelForm):

    class Meta:
        model = UserData
        fields = ["profil_picture"]
        widgets = {
            "profil_picture": forms.FileInput(attrs={
                "class": "form-control"}),
        }

class GameCreationForm(forms.ModelForm):

    class Meta:
        model = UserOwnedGame
        fields = [
            "game_id",
            "game_name",
            "plateform_id",
            "compilation",
            "physical",
            "picture",
            "box_condition",
            "covers_condition",
            "manual_condition",
            "game_condition",
            "condition_precision",
            "rating",
            "rating_precision",
            "never_played",
            "completion_status",
            "completion_precision",
            "achievements_earned",
            "achievements_to_be_earned",
            "owning_status"
        ]
        widgets = {
            "game_id": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "game_name": forms.TextInput(attrs={"class": "form-control"}),
            "plateform_id": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "compilation": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "physical": forms.CheckboxInput(attrs={"class": "form-control"}),
            "picture": forms.FileInput(attrs={
                "class": "form-control", "required": False}),
            "box_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "covers_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "manual_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "game_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "condition_precision": forms.TextInput(attrs={
                "class": "form-control h-100 d-inline-block",
                "required": False}),
            "rating": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "rating_precision": forms.TextInput(attrs={
                "class": "form-control h-100 d-inline-block",
                "required": False}),
            "never_played": forms.CheckboxInput(attrs={
                "class": "form-control"}),
            "completion_status": forms.Select(attrs={
                "class": "form-control"}),
            "completion_precision": forms.TextInput(attrs={
                "class": "form-control", "required": False}),
            "achievements_earned": forms.NumberInput(attrs={
                "class": "form-control", "required": False}),
            "achievements_to_be_earned": forms.NumberInput(attrs={
                "class": "form-control", "required": False}),
            "owning_status": forms.Select(attrs={"class": "form-control"}),
        }

class DLCCreationForm(forms.ModelForm):

    class Meta:
        model = UserOwnedCompilation
        fields = [
            "compilation_id",
            "compilation_name",
            "plateform_id",
            "physical",
            "picture",
            "box_condition",
            "covers_condition",
            "manual_condition",
            "game_condition",
            "condition_precision",
            "owning_status"
        ]
        widgets = {
            "compilation_id": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "compilation_name": forms.TextInput(attrs={
                "class": "form-control"}),
            "plateform_id": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "physical": forms.CheckboxInput(attrs={"class": "form-control"}),
            "picture": forms.FileInput(attrs={
                "class": "form-control", "required": False}),
            "box_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "covers_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "manual_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "game_condition": forms.Select(attrs={
                "class": "form-control", "required": False}),
            "condition_precision": forms.TextInput(attrs={
                "class": "form-control h-100 d-inline-block",
                "required": False}),
            "owning_status": forms.Select(attrs={"class": "form-control"}),
        }

class ParagraphErrorList(ErrorList):

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ""
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])
