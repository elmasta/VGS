import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.translation import gettext_lazy

def get_adminpic_path(instance, filename):
    """Used for the admin to save pictures on the site"""

    return os.path.join("admin_picture", filename)

def get_userpic_path(instance, filename):
    """Used for any registered user to save pictures on the site"""

    return os.path.join("user_picture", str(instance.user.id), filename)

class Condition(models.IntegerChoices):

    MANQUANT = 1, gettext_lazy("Manquant")
    MAUVAIS = 2, gettext_lazy("Mauvais")
    MOYEN = 3, gettext_lazy("Moyen")
    BON = 4, gettext_lazy("Bon")
    TRES_BON = 5, gettext_lazy("Très Bon")
    NEUF = 6, gettext_lazy("Neuf")

class Owning(models.IntegerChoices):

    POSSEDE = 1, gettext_lazy("Possédé")
    VENDU = 2, gettext_lazy("Vendu")
    DONNE = 3, gettext_lazy("Donné")
    PRET_D_UN_AMI = 4, gettext_lazy("Pret d'un ami")
    ABONNEMENT = 5, gettext_lazy("Abonnement")
    AUTRE = 6, gettext_lazy("Autre")

RATING = models.IntegerChoices("RATING", "0 1 2 3 4 5 6 7 8 9 10")

ELEM = [
    "Europe",
    "Amérique du Nord",
    "Japon",
    "Amérique central",
    "Emérique du Sud",
    "Asie",
    "Russie",
    "Moyen Orient",
    "Afrique",
    "Monde"
]

class UserData(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profil_picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                       null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(models.signals.post_delete, sender=UserData)
def submission_delete(sender, instance, **kwargs):
    instance.profil_picture.delete(False)

class Plateform(models.Model):

    class Meta:

        ordering = ('name',)

    def __str__(self):

        for num in range(len(ELEM)):
            if self.region == (num + 1):
                ret_region = ELEM[self.region - 1]
        return self.name + " - " + str(ret_region)

    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=get_adminpic_path)
    class Region(models.IntegerChoices):

        EUROPE = 1, gettext_lazy("Europe")
        AMERIQUE_DU_NORD = 2, gettext_lazy("Amérique du Nord")
        JAPON = 3, gettext_lazy("Japon")
        AMERIQUE_CENTRAL = 4, gettext_lazy("Amérique Central")
        AMERIQUE_DU_SUD = 5, gettext_lazy("Amérique du Sud")
        ASIE = 6, gettext_lazy("Asie")
        RUSSIE = 7, gettext_lazy("Russie")
        MOYEN_ORIENT = 8, gettext_lazy("Moyen Orient")
        AFRIQUE = 9, gettext_lazy("Afrique")
        MONDE = 10, gettext_lazy("Monde")

    region = models.IntegerField(choices=Region.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CollectionPicture(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_picture = models.ImageField(upload_to=get_userpic_path,
                                           blank=True,
                                           null=True)
    private = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubPlateform(models.Model):

    class Meta:

        ordering = ('name',)

    def __str__(self):

        for num in range(len(ELEM)):
            if self.plateform.region == (num + 1):
                ret_region = ELEM[self.plateform.region - 1]
        return self.name + " - " + str(ret_region)

    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PlateformAddon(models.Model):

    class Meta:

        ordering = ('name',)

    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Compilation(models.Model):

    class Meta:

        ordering = ('name',)

    def __str__(self):

        return self.name + " - " + str(self.plateform)

    name = models.CharField(max_length=100)
    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Games(models.Model):

    class Meta:

        ordering = ('name',)

    def __str__(self):

        return self.name + " - " + str(self.plateform)

    name = models.CharField(max_length=100)
    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GameDLC(models.Model):

    class Meta:

        ordering = ('name',)

    def __str__(self):

        return self.name + " - " + str(self.plateform)

    name = models.CharField(max_length=100)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserOwnedCompilation(models.Model):

    class Meta:

        ordering = ('compilation_name',)

    def __str__(self):

        return self.compilation_name + " - " + str(self.plateform_id)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #id from Compilation table (compilation_id) only if user link his
    #compilation to the compilation database
    compilation_id = models.ForeignKey(Compilation, blank=True, null=True,
                                       on_delete=models.CASCADE)
    compilation_name = models.CharField(max_length=200)
    plateform_id = models.ForeignKey(Plateform, blank=True, null=True,
                                     on_delete=models.CASCADE)
    physical = models.BooleanField()
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True)
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    game_condition = models.IntegerField(choices=Condition.choices,
                                         blank=True, null=True)
    condition_precision = models.TextField(blank=True, null=True)
    owning_status = models.IntegerField(choices=Owning.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserOwnedGame(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #id from Games table (game_id) only if user link his game to the game
    #database
    game_id = models.ForeignKey(Games, blank=True, null=True,
                                on_delete=models.CASCADE)
    game_name = models.CharField(max_length=200)
    plateform_id = models.ForeignKey(Plateform, blank=True, null=True,
                                     on_delete=models.CASCADE)
    compilation = models.ForeignKey(UserOwnedCompilation, blank=True,
                                    null=True, on_delete=models.CASCADE)
    physical = models.BooleanField()
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True)
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    game_condition = models.IntegerField(choices=Condition.choices,
                                         blank=True, null=True)
    condition_precision = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING.choices,
                                 blank=True, null=True)
    rating_precision = models.TextField(blank=True, null=True)
    never_played = models.BooleanField()
    class Completion(models.IntegerChoices):

        PAS_FINI = 1, gettext_lazy("Pas fini")
        FINI = 2, gettext_lazy("Fini")
        FINI_CENT_POUR_CENT = 3, gettext_lazy("Fini à 100%")
        SANS_FIN = 4, gettext_lazy("N'a pas de fin")
        ABANDONNE = 5, gettext_lazy("Abandonné")

    completion_status = models.IntegerField(choices=Completion.choices)
    completion_precision = models.TextField(blank=True, null=True)
    achievements_earned = models.IntegerField(blank=True, null=True)
    achievements_to_be_earned = models.IntegerField(blank=True, null=True)
    owning_status = models.IntegerField(choices=Owning.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserOwnedGameDLC(models.Model):

    gameowned_id = models.ForeignKey(UserOwnedGame, on_delete=models.CASCADE)
    #either id from Games table (game_id) or name if it's a made up game from
    #the user
    gamedlc_id = models.ForeignKey(GameDLC, blank=True, null=True,
                                   on_delete=models.CASCADE)
    gamedlc_name = models.CharField(max_length=200)
    physical = models.BooleanField()
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True)
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    gamedlc_condition = models.IntegerField(choices=Condition.choices,
                                            blank=True, null=True)
    condition_precision = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING.choices,
                                 blank=True, null=True)
    rating_precision = models.TextField(blank=True, null=True)
    owning_status = models.IntegerField(choices=Owning.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserOwnedSubPlateform(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subplateform = models.ForeignKey(SubPlateform, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    subplateform_condition = models.IntegerField(choices=Condition.choices,
                                                 blank=True, null=True)
    condition_precision = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserOwnedPlateformAddon(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plateformaddon = models.ForeignKey(PlateformAddon,
                                       on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    plateformaddon_condition = models.IntegerField(choices=Condition.choices,
                                                   blank=True, null=True)
    condition_precision = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
