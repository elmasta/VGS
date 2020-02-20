import os
from django.db import models
from django.contrib.auth.models import User

#todo: game compilation

def get_adminpic_path(filename):
    """Used for the admin to save pictures on the site"""

    return os.path.join('admin_picture', filename)

def get_userpic_path(instance, filename):
    """Used for any registered user to save pictures on the site"""

    return os.path.join('user_picture', str(instance.id), filename)

class Condition(models.IntegerChoices):

    MANQUANT = 1
    MAUVAIS = 2
    MOYEN = 3
    BON = 4
    TRES_BON = 5
    NEUF = 6


class UserData(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profil_picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                       null=True, on_delete=models.CASCADE)

class Plateform(models.Model):

    name = models.CharField(max_length=100, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path,
                                on_delete=models.CASCADE)
    class Region(models.IntegerChoices):

        EUROPE = 1
        AMERIQUE_DU_NORD = 2
        JAPON = 3
        AMERIQUE_CENTRAL = 4
        AMERIQUE_DU_SUD = 5
        ASIE = 6
        RUSSIE = 7
        MOYEN_ORIENT = 8
        AFRIQUE = 9
    region = models.IntegerField(choices=Region.choices,
                                 on_delete=models.CASCADE)

class CollectionPicture(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_picture = models.ImageField(upload_to=get_userpic_path,
                                           blank=True,
                                           null=True,
                                           on_delete=models.CASCADE)

class SubPlateform(models.Model):

    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path,
                                on_delete=models.CASCADE)

class PlateformAddon(models.Model):

    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path,
                                on_delete=models.CASCADE)

class Games(models.Model):

    name = models.CharField(max_length=100, on_delete=models.CASCADE)
    subplateform = models.ForeignKey(SubPlateform, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path,
                                on_delete=models.CASCADE)

class GameDLC(models.Model):

    name = models.CharField(max_length=100, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path,
                                on_delete=models.CASCADE)

class UserOwnedGame(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #either id from Games table (game_id) or name if it's a made up game from
    #the user
    game_id = models.ForeignKey(Games, blank=True, null=True,
                                on_delete=models.CASCADE)
    game_name = models.CharField(max_length=200, blank=True, null=True,
                                 on_delete=models.CASCADE)
    #subplateform_id only when it's a made up game from the user
    subplateform_id = models.ForeignKey(SubPlateform, blank=True, null=True,
                                        on_delete=models.CASCADE)
    physical = models.BooleanField(on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True, on_delete=models.CASCADE)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True,
                                        on_delete=models.CASCADE)
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    game_condition = models.IntegerField(choices=Condition.choices,
                                         blank=True, null=True,
                                         on_delete=models.CASCADE)
    condition_precision = models.TextField(blank=True, null=True,
                                           on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True,
                                 on_delete=models.CASCADE)
    rating_precision = models.TextField(blank=True, null=True,
                                        on_delete=models.CASCADE)
    never_played = models.BooleanField(on_delete=models.CASCADE)
    class Completion(models.IntegerChoices):

        PAS_FINI = 1
        FINI = 2
        FINI_CENT_POUR_CENT = 3
        SANS_FIN = 4
        ABANDONNE = 5
    completion_status = models.IntegerField(choices=Completion.choices,
                                            on_delete=models.CASCADE)
    completion_precision = models.TextField(blank=True, null=True,
                                            on_delete=models.CASCADE)
    achievements_earned = models.IntegerField(blank=True, null=True,
                                              on_delete=models.CASCADE)
    achievements_to_be_earned = models.IntegerField(blank=True, null=True,
                                                    on_delete=models.CASCADE)

class UserOwnedGameDLC(models.Model):

    gameowned_id = models.ForeignKey(UserOwnedGame, on_delete=models.CASCADE)
    #either id from Games table (game_id) or name if it's a made up game from
    #the user
    gamedlc_id = models.ForeignKey(GameDLC, blank=True, null=True,
                                   on_delete=models.CASCADE)
    gamedlc_name = models.CharField(max_length=200, blank=True, null=True,
                                    on_delete=models.CASCADE)
    physical = models.BooleanField(on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True, on_delete=models.CASCADE)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True,
                                        on_delete=models.CASCADE)
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    gamedlc_condition = models.IntegerField(choices=Condition.choices,
                                            blank=True, null=True,
                                            on_delete=models.CASCADE)
    condition_precision = models.TextField(blank=True, null=True,
                                           on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True,
                                 on_delete=models.CASCADE)
    rating_precision = models.TextField(blank=True, null=True,
                                        on_delete=models.CASCADE)

class UserOwnedSubPlateform(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subplateform = models.ForeignKey(SubPlateform, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True, on_delete=models.CASCADE)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True,
                                        on_delete=models.CASCADE)
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    subplateform_condition = models.IntegerField(choices=Condition.choices,
                                                 blank=True, null=True,
                                                 on_delete=models.CASCADE)
    condition_precision = models.TextField(blank=True, null=True,
                                           on_delete=models.CASCADE)

class UserOwnedPlateformAddon(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plateformaddon = models.ForeignKey(PlateformAddon,
                                       on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                null=True, on_delete=models.CASCADE)
    box_condition = models.IntegerField(choices=Condition.choices,
                                        blank=True, null=True,
                                        on_delete=models.CASCADE)
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    plateformaddon_condition = models.IntegerField(choices=Condition.choices,
                                                   blank=True, null=True,
                                                   on_delete=models.CASCADE)
    condition_precision = models.TextField(blank=True, null=True,
                                           on_delete=models.CASCADE)
