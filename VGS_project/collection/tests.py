from collection.forms import *
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.files.uploadedfile import SimpleUploadedFile
from collection.models import UserData, Games, UserOwnedGame, Plateform,\
    UserOwnedSubPlateform, CollectionPicture, ELEM, Compilation

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
    """User related testing class"""

    def setUp(self):

        self.account = User.objects.create_user(
            email="test@b.com", username="testb", password="0000")
        self.client.login(username="testb", password="0000")
        self.session = self.client.session
        self.session["context"] = {"profil_pic": None,
                                   "username": "testb",
                                   "platfor_user": None}
        self.session.save()
        self.plat = Plateform.objects.create(
            name="Megadrive",
            region=1)
        self.game = Games.objects.create(
            name="Tails",
            plateform=self.plat)
        UserOwnedGame.objects.create(
            user=self.account,
            game_id=self.game,
            game_name="Sonic",
            plateform_id=self.plat,
            #compilation="null",
            physical=True,
            #picture="null",
            #box_condition="null",
            #covers_condition="null",
            #manual_condition="null",
            #game_condition ="null",
            #condition_precision="null",
            #rating="null",
            #rating_precision="null",
            never_played=True,
            completion_status=1,
            #completion_precision="null",
            #achievements_earned="null",
            #achievements_to_be_earned="null",
            owning_status=1)

    def test_index_logged_user_page(self):
        """check if the context on the index page is correct when the user is
        logged"""

        response = self.client.get(reverse("index"))
        self.assertEqual(response.context["games_name"][0]["name"], "Tails")

    def test_about_logged_user_page(self):
        """check if the context on the index page is correct when the user is
        logged"""

        response = self.client.get(reverse("about"))
        self.assertEqual(response.context["username"], "testb")

    def test_logout_login_page(self):
        """check the logout and login views"""

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

    def test_ask_email_page(self):
        """check the ask_email views"""

        response = self.client.get(reverse("ask_email"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("user_logout"))
        response = self.client.post(reverse("ask_email"), data={
            'email':'tes@b.com',
            })
        self.assertEqual(response.context["errors"], "Email inconnu")
