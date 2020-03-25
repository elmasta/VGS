from collection.forms import *
from collection.models import *
from collection.tokens import account_activation_token
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

class StatusCodeTestCase(TestCase):
    """Test if the views that must return a status_code 200 or 302 return that
    status_code"""

    def test_index_page(self):
        """Test if the '' path return the index page"""

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        """Test if the 'about' path return the about page"""

        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_toindex(self):
        """Test if the 'profile_page' path return the index page if user is
        not logged"""

        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 302)

    def test_user_photos_toindex(self):
        """Test if the 'user_photos' path return the index page if user is not
        logged"""

        response = self.client.get(reverse("user_photos"))
        self.assertEqual(response.status_code, 302)

    def test_add_item_toindex(self):
        """Test if the 'add_item' path return the index page if user is not
        logged"""

        response = self.client.get(reverse("add_item"))
        self.assertEqual(response.status_code, 302)

    def test_add_game_toindex(self):
        """Test if the 'add_game' path return the index page if user is not
        logged"""

        response = self.client.get(reverse("add_game"))
        self.assertEqual(response.status_code, 302)

    def test_add_dlc_toindex(self):
        """Test if the 'add_DLC' path return the index page if user is not
        logged"""

        response = self.client.get(reverse("add_DLC"))
        self.assertEqual(response.status_code, 302)

    def test_add_comp_toindex(self):
        """Test if the 'add_comp' path return the index page if user is not
        logged"""

        response = self.client.get(reverse("add_comp"))
        self.assertEqual(response.status_code, 302)

    def test_add_console_toindex(self):
        """Test if the 'add_console' path return the index page if user is not
        logged"""

        response = self.client.get(reverse("add_console"))
        self.assertEqual(response.status_code, 302)

    def test_add_addon_toindex(self):
        """Test if the 'add_addon' path return the index page if user is not
        logged"""

        response = self.client.get(reverse("add_addon"))
        self.assertEqual(response.status_code, 302)

    def test_user_collection_toindex(self):
        """Test if the 'user_collection' path return the index page if user is
        not logged"""

        response = self.client.get(reverse("user_collection",
                                           kwargs={"plateform_id": "0"}))
        self.assertEqual(response.status_code, 302)

    def test_user_game_page_toindex(self):
        """Test if the 'user_game_page' path return the index page if user is
        not logged"""

        response = self.client.get(reverse("user_game_page",
                                           kwargs={"game_id": "0"}))
        self.assertEqual(response.status_code, 302)

    def test_user_accessory_toindex(self):
        """Test if the 'user_accessory' path return the index page if user is
        not logged"""

        response = self.client.get(reverse("user_accessory"))
        self.assertEqual(response.status_code, 302)

    def test_user_accessory_page_toindex(self):
        """Test if the 'user_accessory_page' path return the index page if
        user is not logged"""

        response = self.client.get(reverse("user_accessory_page",
                                           kwargs={"accessory_id": "0"}))
        self.assertEqual(response.status_code, 302)

    def test_user_consoles_toindex(self):
        """Test if the 'user_consoles' path return the index page if
        user is not logged"""

        response = self.client.get(reverse("user_consoles"))
        self.assertEqual(response.status_code, 302)

    def test_user_consoles_page_toindex(self):
        """Test if the 'user_consoles_page' path return the index page if
        user is not logged"""

        response = self.client.get(reverse("user_consoles_page",
                                           kwargs={"consoles_id": "0"}))
        self.assertEqual(response.status_code, 302)

    def test_user_compilations_toindex(self):
        """Test if the 'user_compilations' path return the index page if
        user is not logged"""

        response = self.client.get(reverse("user_compilations"))
        self.assertEqual(response.status_code, 302)

    def test_user_compilations_page_toindex(self):
        """Test if the 'user_compilations_page' path return the index page if
        user is not logged"""

        response = self.client.get(reverse("user_compilations_page",
                                           kwargs={"compilations_id": "0"}))
        self.assertEqual(response.status_code, 302)

    def test_user_dlc_page_toindex(self):
        """Test if the 'user_dlc_page' path return the index page if
        user is not logged"""

        response = self.client.get(reverse("user_dlc_page",
                                           kwargs={"dlc_id": "0"}))
        self.assertEqual(response.status_code, 302)

class UserTestCase(TestCase):
    """User logged related testing class"""

    def setUp(self):

        im_io = BytesIO() # BytesIO has to be used, StrinIO isn't working
        im = Image.new(mode='RGB', size=(200, 200))
        im.save(im_io, 'JPEG')
        self.image_data = {
            'image_field': InMemoryUploadedFile(
                im_io,
                None,
                'random.jpg',
                'image/jpeg',
                len(im_io.getvalue()),
                None)
        }
        self.account = User.objects.create_user(
            email="test@b.com", username="testb", password="0000")
        self.client.login(username="testb", password="0000")
        self.session = self.client.session
        self.session["context"] = {"profil_pic": None,
                                   "username": "testb",
                                   "platfor_user": None,
                                   "email": "test@b.com",
                                   "name": "John"}
        self.session.save()
        self.plat = Plateform.objects.create(
            name="Megadrive",
            region=1,
            picture=self.image_data['image_field'])
        self.game = Games.objects.create(
            name="Tails",
            plateform=self.plat)
        self.user_game = UserOwnedGame.objects.create(
            picture=self.image_data['image_field'],
            user=self.account,
            game_id=self.game,
            game_name="Sonic",
            plateform_id=self.plat,
            physical=True,
            never_played=True,
            completion_status=1,
            owning_status=1)

    def test_index_logged_user_page(self):
        """test the index view when the user is logged"""

        response = self.client.get(reverse("index"))
        self.assertEqual(response.context["games_name"][0]["name"], "Tails")

    def test_about_logged_user_page(self):
        """test the about view"""

        response = self.client.get(reverse("about"))
        self.assertEqual(response.context["username"], "testb")

    def test_logout_login_page(self):
        """test the logout_login view"""

        response = self.client.get(reverse("login_page"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("user_logout"), follow=True)
        self.assertEqual(response.context['user'].is_authenticated, False)

        response = self.client.post(reverse("login_page"), data={
            'username':'test',
            'password':'0000'
            })
        self.assertEqual(response.context["errors"], "Ce pseudo est inconnu")

        response = self.client.post(reverse("login_page"), data={
            'username':'testb',
            'password':'000'
            })
        self.assertEqual(response.context["errors"],
                         "Compte non actif ou mot de passe invalide")

        response = self.client.post(reverse("login_page"), data={
            'username':'testb',
            'password':'0000'
            }, follow=True)
        self.assertEqual(response.context["username"], "testb")

        response = self.client.get(reverse("user_logout"), follow=True)

        userdata = UserData.objects.create(
            user=self.account,
            profil_picture=self.image_data['image_field'])
        response = self.client.post(reverse("login_page"), data={
            'username':'testb',
            'password':'0000'
            }, follow=True)
        self.assertEqual(response.context["username"], "testb")

    def test_ask_email_page(self):
        """test the ask_email view"""

        response = self.client.get(reverse("ask_email"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("user_logout"))
        response = self.client.post(reverse("ask_email"), data={
            'email':'tes@b.com',
            })
        self.assertEqual(response.context["errors"], "Email inconnu")

        response = self.client.post(reverse("ask_email"), data={
            'email':'test@b.com',
            })
        self.assertEqual(len(mail.outbox), 1)

    def test_register_page(self):
        """test the register view"""

        response = self.client.get(reverse("register_page"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("user_logout"))
        response = self.client.post(reverse("register_page"), data={
            "username":"testa",
            "email":"test@b.com",
            "first_name":"john",
            "password":"0000",
            "CheckPassword":"0000",
            }, follow=True)
        self.assertEqual(response.context["errors"],
                         "Email déjà utilisé ou mot de passe érroné")

        response = self.client.post(reverse("register_page"), data={
            "username":"testa",
            "email":"test@c.com",
            "first_name":"john",
            "password":"0000",
            "CheckPassword":"0000",
            }, follow=True)
        self.assertEqual(len(mail.outbox), 1)

    def test_activate_page(self):
        """test the activate view"""

        uidb64 = urlsafe_base64_encode(force_bytes(self.account.id))
        token = account_activation_token.make_token(self.account)
        response = self.client.get(reverse("activate",
                                           args=(uidb64, token)))
        self.assertEqual(response.content,
                         b"Merci, vous pouvez maintenant vous connecter")

        uidb64 = "null"
        response = self.client.get(reverse("activate",
                                           args=(uidb64, token)), follow=True)
        self.assertEqual(response.content, b"Le lien n'est pas valide")

    def test_forgotten_password_page(self):
        """test the forgotten_password view"""

        uidb64 = urlsafe_base64_encode(force_bytes(self.account.id))
        token = account_activation_token.make_token(self.account)
        response = self.client.get(reverse("forgotten_password",
                                           args=(uidb64, token)))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("user_logout"))
        response = self.client.get(reverse("forgotten_password",
                                           args=(uidb64, token)),
                                   follow=True)
        if response.context["form"]:
            ok = True
        else:
            ok = False
        self.assertEqual(ok, True)

        response = self.client.post(reverse("forgotten_password",
                                            args=(uidb64, token)), data={
                                                "password":"2222",
                                                "CheckPassword":"2222",},
                                    follow=True)
        user = authenticate(username="testb", password="2222")
        self.assertEqual(user is not None, True)

        uidb64 = "null"
        response = self.client.get(reverse("forgotten_password",
                                           args=(uidb64, token)), follow=True)
        self.assertEqual(response.content, b"Le lien n'est pas valide")

    def test_profile_page(self):
        """test the profile_page view"""

        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 200)

        #user_pic = UserData.objects.create(
        #    user=self.account,
        #    profil_picture=self.image_data['image_field'])
        #response = self.client.post(reverse("profile_page"), data={
        #    "profil_picture": self.image_data}, follow=True)
        #self.assertEqual(response.context["profil_pic"], self.image_data)

        response = self.client.post(reverse("profile_page"), data={
            "NewPassword": "2222",
            "CheckPasswordChange": "2222"}, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, False)

        response = self.client.post(reverse("login_page"), data={
            'username':'testb',
            'password':'2222'
            }, follow=True)
        response = self.client.post(reverse("profile_page"), data={
            "CheckPassword": "2222",}, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, False)

    def test_user_photos_page(self):
        """test the user_photos view"""

        response = self.client.get(reverse("user_photos"))
        self.assertEqual(response.status_code, 200)

    #    #user_pic = UserData.objects.create(
    #    #    user=self.account,
    #    #    profil_picture=self.image_data['image_field'])
    #    response = self.client.post(reverse("user_photos"), data={
    #        "collection_picture": self.image_data,
    #        "private": False}, follow=True)
    #    self.assertEqual(response.context["profil_pic"], self.image_data)

    def test_add_item_page(self):
        """check the add_item view"""

        response = self.client.get(reverse("add_item"))
        self.assertEqual(response.status_code, 200)

    def test_add_game_page(self):
        """test the views related to the user game"""

        self.client.post(reverse("add_game"), data={
            "game_name": "Knuckles",
            "plateform_id": self.plat.id,
            "never_played": "1",
            "completion_status": "1",
            "owning_status": "1"}, follow=True)
        test = "bad"
        game = UserOwnedGame.objects.get(game_name="Knuckles")
        if game is not None:
            test = "ok"
        self.assertEqual(test, "ok")

        self.client.post(reverse("add_game"), data={
            "game_id": self.game.id,
            "game_name": "Robotnick",
            "never_played": "1",
            "completion_status": "1",
            "owning_status": "1"}, follow=True)
        test = "bad"
        game = UserOwnedGame.objects.get(game_name="Robotnick")
        if game is not None:
            test = "ok"
        self.assertEqual(test, "ok")

        response = self.client.get(reverse("user_game_page",
                                           args=(self.user_game.id,)))
        self.assertEqual(response.context["modify"], True)

        response = self.client.post(
            reverse("user_game_page",
                    args=(self.user_game.id,)),
            data={
                "game_id": "",
                "picture": self.image_data,
                "game_name": "Mario",
                "never_played": "1",
                "completion_status": "1",
                "owning_status": "1"},
            follow=True)
        try:
            UserOwnedGame.objects.get(game_name="Mario")
            test = "ok"
        except:
            test = "bad"
        self.assertEqual(test, "ok")

        response = self.client.post(
            reverse("user_game_page",
                    args=(self.user_game.id,)),
            data={
                "game_id": self.game.id,
                "picture": self.image_data,
                "game_name": "Mario",
                "never_played": "1",
                "completion_status": "1",
                "owning_status": "1"},
            follow=True)
        try:
            UserOwnedGame.objects.get(game_name="Mario")
            test = "ok"
        except:
            test = "bad"
        self.assertEqual(test, "ok")

        response = self.client.post(
            reverse("user_game_page", args=(self.user_game.id,)),
            data={"delete": self.user_game.id},
            follow=True)
        try:
            UserOwnedGame.objects.get(id=self.user_game.id)
            test = "bad"
        except:
            test = "ok"
        self.assertEqual(test, "ok")

    def test_add_dlc_page(self):
        """test the views related to the user DLC"""

        dlc = GameDLC.objects.create(
            name="Badnicks",
            game=self.game,
            picture=self.image_data['image_field'])
        self.client.post(reverse("add_DLC"), data={
            "gameowned_id": self.user_game.id,
            "gamedlc_name": "Shitty Friends",
            "owning_status": "1"}, follow=True)
        test = "bad"
        user_dlc = UserOwnedGameDLC.objects.get(gamedlc_name="Shitty Friends")
        if user_dlc is not None:
            test = "ok"
        self.assertEqual(test, "ok")

        response = self.client.post(
            reverse("user_dlc_page",
                    args=(user_dlc.id,)),
            data={
                "gamedlc_id": dlc.id,
                "gameowned_id": self.user_game.id,
                "gamedlc_name": "Flickys",
                "picture": self.image_data,
                "owning_status": "1"
                },
            follow=True)
        try:
            UserOwnedGameDLC.objects.get(gamedlc_id=dlc.id)
            test = "ok"
        except:
            test = "bad"
        self.assertEqual(test, "ok")

        response = self.client.post(
            reverse("user_dlc_page", args=(user_dlc.id,)),
            data={"delete": user_dlc.id},
            follow=True)
        try:
            UserOwnedGameDLC.objects.get(id=user_dlc.id)
            test = "bad"
        except:
            test = "ok"
        self.assertEqual(test, "ok")

    def test_add_comp_page(self):
        """test the views related to the user compilations"""

        comp = Compilation.objects.create(
            name="Sonic Compilation",
            plateform=self.plat,
            picture=self.image_data['image_field'])
        self.client.post(reverse("add_comp"), data={
            "compilation_name": "Sonic Mega Collection +",
            "plateform_id": self.plat.id,
            "owning_status": "1"}, follow=True)
        test = "bad"
        user_comp = UserOwnedCompilation.objects.get(
            compilation_name="Sonic Mega Collection +")
        if user_comp is not None:
            test = "ok"
        self.assertEqual(test, "ok")

        self.client.post(reverse("add_comp"), data={
            "compilation_id": comp.id,
            "compilation_name": "Tails Compilation",
            "owning_status": "1"}, follow=True)
        test = "bad"
        user_comp = UserOwnedCompilation.objects.get(
            compilation_name="Tails Compilation")
        if user_comp is not None:
            test = "ok"
        self.assertEqual(test, "ok")

        response = self.client.get(reverse("user_compilations_page",
                                           args=(user_comp.id,)))
        self.assertEqual(response.context["modify"], True)

        response = self.client.post(
            reverse("user_compilations_page",
                    args=(user_comp.id,)),
            data={
                "compilation_id": comp.id,
                "compilation_name": "Sonic Mega Collection -",
                "picture": self.image_data,
                "owning_status": "1"
                },
            follow=True)
        try:
            UserOwnedCompilation.objects.get(compilation_id=comp.id)
            test = "ok"
        except:
            test = "bad"
        self.assertEqual(test, "ok")

        response = self.client.post(
            reverse("user_compilations_page",
                    args=(user_comp.id,)),
            data={
                "plateform_id": self.plat.id,
                "compilation_name": "Sonic Mega Collection z",
                "picture": self.image_data,
                "owning_status": "1"
                },
            follow=True)
        try:
            UserOwnedCompilation.objects.get(
                compilation_name="Sonic Mega Collection z")
            test = "ok"
        except:
            test = "bad"
        self.assertEqual(test, "ok")

        response = self.client.get(reverse("user_compilations"))
        test = UserOwnedCompilation.objects.all()
        self.assertEqual(response.context["user_comp"][0], test[0])

        response = self.client.post(
            reverse("user_compilations_page", args=(user_comp.id,)),
            data={"delete": user_comp.id},
            follow=True)
        try:
            UserOwnedSubPlateform.objects.get(id=user_comp.id)
            test = "bad"
        except:
            test = "ok"
        self.assertEqual(test, "ok")

    def test_add_console_page(self):
        """test the views related to the user plateforms"""

        subplat = SubPlateform.objects.create(
            plateform=self.plat,
            name="Megadrive 1",
            picture=self.image_data['image_field'])
        self.client.post(reverse("add_console"), data={
            "subplateform": subplat.id})
        test = "bad"
        test_subplat = UserOwnedSubPlateform.objects.get(
            subplateform=subplat.id)
        if test_subplat is not None:
            test = "ok"
        self.assertEqual(test, "ok")

        response = self.client.get(reverse("user_consoles_page",
                                           args=(test_subplat.id,)))
        self.assertEqual(response.context["modify"], True)

        response = self.client.post(
            reverse("user_consoles_page",
                    args=(test_subplat.id,)),
            data={
                "subplateform": subplat.id,
                "picture": self.image_data,
                },
            follow=True)
        try:
            UserOwnedSubPlateform.objects.get(subplateform=subplat.id)
            test = "ok"
        except:
            test = "bad"
        self.assertEqual(test, "ok")

        response = self.client.get(reverse("user_consoles"))
        test = UserOwnedSubPlateform.objects.all()
        self.assertEqual(response.context["user_subplateform"][0], test[0])

        response = self.client.post(
            reverse("user_consoles_page", args=(test_subplat.id,)),
            data={"delete": test_subplat.id},
            follow=True)
        try:
            UserOwnedSubPlateform.objects.get(id=test_subplat.id)
            test = "bad"
        except:
            test = "ok"
        self.assertEqual(test, "ok")

    def test_add_addon_page(self):
        """test the views related to the user game accessories (addon)"""

        addon = PlateformAddon.objects.create(
            plateform=self.plat,
            name="Manette Megadrive 1",
            picture=self.image_data['image_field'])
        self.client.post(reverse("add_addon"), data={
            "plateformaddon": addon.id})
        test = "bad"
        test_addon = UserOwnedPlateformAddon.objects.get(
            plateformaddon=addon.id)
        if test_addon is not None:
            test = "ok"
        self.assertEqual(test, "ok")

        response = self.client.get(reverse("user_accessory_page",
                                           args=(test_addon.id,)))
        self.assertEqual(response.context["modify"], True)

        response = self.client.post(
            reverse("user_accessory_page",
                    args=(test_addon.id,)),
            data={
                "plateformaddon": addon.id,
                "picture": self.image_data,
                },
            follow=True)
        try:
            UserOwnedPlateformAddon.objects.get(plateformaddon=addon.id)
            test = "ok"
        except:
            test = "bad"
        self.assertEqual(test, "ok")

        response = self.client.get(reverse("user_accessory"))
        test = UserOwnedPlateformAddon.objects.all()
        self.assertEqual(response.context["user_plateform_addon"][0], test[0])

        response = self.client.post(
            reverse("user_accessory_page", args=(test_addon.id,)),
            data={"delete": test_addon.id},
            follow=True)
        try:
            UserOwnedPlateformAddon.objects.get(id=test_addon.id)
            test = "bad"
        except:
            test = "ok"
        self.assertEqual(test, "ok")

    def test_user_collection_page(self):
        """test the user_collection view"""

        response = self.client.get(reverse("user_collection", args=(0,)))
        test = UserOwnedGame.objects.all()
        self.assertEqual(response.context["game_set"][0], test[0])

        response = self.client.get(
            reverse("user_collection", args=(self.plat.id,)))
        test = UserOwnedGame.objects.all()
        self.assertEqual(response.context["game_set"][0], test[0])
