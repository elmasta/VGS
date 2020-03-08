from collection.models import UserData, UserOwnedGame
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
        labels = {
            "game_id": "Choisissez un jeu",
            "game_name": "Nom du jeu",
            "plateform_id": "Plateforme",
            "compilation": "Compilation",
            "physical": "Jeu physique?",
            "picture": "Image",
            "box_condition": "État de la boite",
            "covers_condition": "État des jaquettes",
            "manual_condition": "État du Manuel",
            "game_condition": "État du Jeu",
            "condition_precision": "Détail sur l'état de l'ensemble",
            "rating": "Note",
            "rating_precision": "Review",
            "never_played": "Déjà joué?",
            "completion_status": "Fini?",
            "completion_precision": "Où en êtes vous dans le jeu?",
            "achievements_earned": "Nombre de succès obtenus",
            "achievements_to_be_earned": "Nombre de succès total du jeu",
            "owning_status": "Status de possession"
        }
        widgets = {
            "game_id": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune",
                "required": "False"}),
            "game_name": forms.TextInput(attrs={"class": "form-control"}),
            "plateform_id": forms.Select(attrs={"class": "form-control"}),
            "compilation": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune",
                "required": "False"}),
            "physical": forms.CheckboxInput(attrs={"class": "form-control"}),
            "picture": forms.FileInput(attrs={"class": "form-control"}),
            "box_condition": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune",
                "required": "False"}),
            "covers_condition": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune",
                "required": "False"}),
            "manual_condition": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune",
                "required": "False"}),
            "game_condition": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune",
                "required": "False"}),
            "condition_precision": forms.TextInput(attrs={
                "class": "form-control", "required": "False"}),
            "rating": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune",
                "required": "False"}),
            "rating_precision": forms.TextInput(attrs={
                "class": "form-control", "required": "False"}),
            "never_played": forms.Select(attrs={
                "class": "form-control", "initial": "False",}),
            "completion_status": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune"}),
            "completion_precision": forms.TextInput(attrs={
                "class": "form-control", "required": "False"}),
            "achievements_earned": forms.NumberInput(attrs={
                "class": "form-control", "required": "False"}),
            "achievements_to_be_earned": forms.NumberInput(attrs={
                "class": "form-control", "required": "False"}),
            "owning_status": forms.Select(attrs={
                "class": "form-control", "initial": "Aucune"}),
        }

class ParagraphErrorList(ErrorList):

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ""
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])
