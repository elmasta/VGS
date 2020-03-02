import os
from django.db import models
from django.contrib.auth.models import User

def get_adminpic_path(instance, filename):
    """Used for the admin to save pictures on the site"""

    return os.path.join("collection/admin_picture", filename)

def get_userpic_path(instance, filename):
    """Used for any registered user to save pictures on the site"""

    return os.path.join("collection/user_picture", str(instance.id), filename)

class Condition(models.IntegerChoices):

    MANQUANT = 1
    MAUVAIS = 2
    MOYEN = 3
    BON = 4
    TRES_BON = 5
    NEUF = 6

class Owning(models.IntegerChoices):

    POSSEDE = 1
    VENDU = 2
    DONNEE = 3
    PRET_DUN_AMI = 4
    ABONEMENT = 5
    AUTRE = 6


class UserData(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profil_picture = models.ImageField(upload_to=get_userpic_path, blank=True,
                                       null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Plateform(models.Model):

    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=get_adminpic_path)
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
    region = models.IntegerField(choices=Region.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CollectionPicture(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_picture = models.ImageField(upload_to=get_userpic_path,
                                           blank=True,
                                           null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubPlateform(models.Model):

    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PlateformAddon(models.Model):

    plateform = models.ForeignKey(Plateform, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Compilation(models.Model):

    name = models.CharField(max_length=100)
    plateform = models.ForeignKey(SubPlateform, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Games(models.Model):

    name = models.CharField(max_length=100)
    plateform = models.ForeignKey(SubPlateform, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path)
    compilation = models.ManyToManyField(Compilation, blank=True,
                                         related_name="games_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GameDLC(models.Model):

    name = models.CharField(max_length=100)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_adminpic_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserOwnedCompilation(models.Model):

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
    compilation = models.ManyToManyField(UserOwnedCompilation, blank=True,
                                         related_name="userownedgame_id")
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
    rating = models.IntegerField(blank=True, null=True)
    rating_precision = models.TextField(blank=True, null=True)
    never_played = models.BooleanField()
    class Completion(models.IntegerChoices):

        PAS_FINI = 1
        FINI = 2
        FINI_CENT_POUR_CENT = 3
        SANS_FIN = 4
        ABANDONNE = 5
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
    rating = models.IntegerField(blank=True, null=True)
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
    covers_condition = models.IntegerField(choices=Condition.choices,
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
    covers_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    manual_condition = models.IntegerField(choices=Condition.choices,
                                           blank=True, null=True)
    plateformaddon_condition = models.IntegerField(choices=Condition.choices,
                                                   blank=True, null=True)
    condition_precision = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
