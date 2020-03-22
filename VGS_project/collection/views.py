from collection.classes import *
from collection.forms import *
from collection.tokens import account_activation_token
from collection.models import UserData, Games, UserOwnedGame, Plateform,\
    UserOwnedSubPlateform, CollectionPicture, ELEM
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from PIL import Image

def index(request):

    #Person.objects.values('optional_first_name').annotate(c=Count('optional_first_name')).order_by('-c')
    if request.user.is_authenticated:
        return render(request, "collection/index.html",
                      request.session["context"])
    else:
        return render(request, "collection/index.html")

def login_page(request):

    context = {}
    if request.user.is_authenticated:
        return return_index(request, render)
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username,
                                    password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    request.session['context'] = {
                        "username": request.user.username,
                        "email": request.user.email,
                        "name": request.user.first_name,
                    }
                    picture = None
                    if UserData.objects.filter(user=request.user.id).exists():
                        user_pic = UserData.objects.get(user=request.user.id)
                        request.session['context']["profil_pic"] =\
                            user_pic.profil_picture.path
                    else:
                        request.session['context']["profil_pic"] = picture
                    request.session["context"] = user_plateforms(
                        request, UserOwnedGame, Plateform, ELEM)
                    return redirect("index")
                context["errors"] = "Vous n'avez pas activé votre compte"
            else:
                context["errors"] = "Ce pseudo est inconnu"
    form = UserLoginForm()
    context["form"] = form
    return render(request, "collection/login.html", context)

def ask_email(request):

    context = {}
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                mail_subject = "Changez votre mot de passe VGS."
                template = "collection/acc_change_password.html"
                send_email(email, template, mail_subject, User)
                return redirect("login_page")
            context["errors"] = "Email inconnu"
    form = EmailForm()
    context["form"] = form
    return render(request, "collection/check_email.html", context)

def register_page(request):

    context = {}
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(email=email)
            if password == request.POST.get("CheckPassword") and\
                not user.exists():
                User.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name,
                    is_active=False)
                mail_subject = "Activez votre compte VGS."
                template = "collection/acc_active_email.html"
                send_email(email, template, mail_subject, User)
                return redirect("login_page")
            context["errors"] = "Email déjà utilisé ou mot de passe érroné"
    form = UserCreationForm()
    context["form"] = form
    return render(request, "collection/register.html", context)

def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Merci, vous pouvez maintenant vous connecter")
    return HttpResponse("Le lien n'est pas valide")

def forgotten_password(request, uidb64, token):

    if request.user.is_authenticated:
        return redirect("index")
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] ==\
                request.POST.get("CheckPassword"):
                user.set_password(form.cleaned_data["password"])
                user.save()
                return redirect("index")
    if user is not None and account_activation_token.check_token(user, token):
        form = ChangePasswordForm()
        return render(
            request, "collection/forgoten_password.html", {"form": form})
    return HttpResponse("Le lien n'est pas valide")

def user_logout(request):

    logout(request)
    return redirect("index")

def profile_page(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            #add avatar deletion
            form = ChangeAvatarForm(request.POST, request.FILES)
            if form.is_valid():
                new_avatar = form.cleaned_data["profil_picture"]
                if UserData.objects.filter(user=request.user).exists():
                    avatar = UserData.objects.get(user=request.user)
                    avatar.profil_picture = new_avatar
                    avatar.save()
                else:
                    avatar = UserData(profil_picture=new_avatar,
                                      user=request.user)
                    avatar.save()
                user_pic = UserData.objects.get(user=request.user)
                context = request.session["context"]
                context["profil_pic"] = user_pic.profil_picture.path
                request.session["context"] = context
            elif authenticate(username=request.user.username,
                              password=request.POST.get("CheckPassword"))\
                is not None:
                User.objects.get(id=request.user.id).delete()
                return redirect("index")
        addprofpicform = ChangeAvatarForm()
        if request.session["context"]["profil_pic"] is not None:
            user_pic = UserData.objects.get(user=request.user)
        context = {
            "username": request.session["context"]["username"],
            "email": request.session["context"]["email"],
            "name": request.session["context"]["name"],
            "addprofpicform": addprofpicform,
            "date_joined": request.user.date_joined,
            "profil_pic": request.session["context"]["profil_pic"],
            "platfor_user": request.session["context"]["platfor_user"]
        }
        return render(request, "collection/profile.html", context)
    return redirect("login_page")

def user_photos(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("photos") is None:
                form = AddPhotosForm(request.POST, request.FILES)
                if form.is_valid():
                    collection_picture = form.cleaned_data[
                        "collection_picture"]
                    private = form.cleaned_data["private"]
                    new_userpicture = CollectionPicture(
                        user=request.user,
                        collection_picture=collection_picture,
                        private=private
                    )
                    new_userpicture.save()
            else:
                CollectionPicture.objects.get(
                    id=request.POST.get("photos")).delete()
        addcollpicform = AddPhotosForm()
        photos = CollectionPicture.objects.filter(user=request.user)
        context = {
            "username": request.session["context"]["username"],
            "addcollpicform": addcollpicform,
            "photos": photos,
            "profil_pic": request.session["context"]["profil_pic"],
            "platfor_user": request.session["context"]["platfor_user"]
        }
        return render(request, "collection/photo.html", context)
    return redirect("index")

def add_item(request):

    if request.user.is_authenticated:
        return render(request, "collection/add_item.html",
                      request.session['context'])
    return redirect("index")

def add_game(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = GameCreationForm(
                request.POST, request.FILES, current_user=request.user)
            if form.is_valid():
                game_id = form.cleaned_data["game_id"]
                game_name = form.cleaned_data["game_name"]
                if game_id is None:
                    plateform_id = form.cleaned_data["plateform_id"]
                else:
                    game_item = get_object_or_404(
                        Games.objects.filter(id=game_id.id))
                    plateform_id = game_item.plateform
                compilation = form.cleaned_data["compilation"]
                physical = form.cleaned_data["physical"]
                picture = form.cleaned_data["picture"]
                box_condition = form.cleaned_data["box_condition"]
                covers_condition = form.cleaned_data["covers_condition"]
                manual_condition = form.cleaned_data["manual_condition"]
                game_condition = form.cleaned_data["game_condition"]
                condition_precision = form.cleaned_data["condition_precision"]
                rating = form.cleaned_data["rating"]
                rating_precision = form.cleaned_data["rating_precision"]
                never_played = form.cleaned_data["never_played"]
                completion_status = form.cleaned_data["completion_status"]
                completion_precision = form.cleaned_data[
                    "completion_precision"]
                achievements_earned = form.cleaned_data["achievements_earned"]
                achievements_to_be_earned = form.cleaned_data[
                    "achievements_to_be_earned"]
                owning_status = form.cleaned_data["owning_status"]
                new_game = UserOwnedGame(
                    user=request.user,
                    game_id=game_id,
                    game_name=game_name,
                    plateform_id=plateform_id,
                    compilation=compilation,
                    physical=physical,
                    picture=picture,
                    box_condition=box_condition,
                    covers_condition=covers_condition,
                    manual_condition=manual_condition,
                    game_condition=game_condition,
                    condition_precision=condition_precision,
                    rating=rating,
                    rating_precision=rating_precision,
                    never_played=never_played,
                    completion_status=completion_status,
                    completion_precision=completion_precision,
                    achievements_earned=achievements_earned,
                    achievements_to_be_earned=achievements_to_be_earned,
                    owning_status=owning_status
                    )
                new_game.save()
                request.session["context"] = user_plateforms(
                    request, UserOwnedGame, Plateform, ELEM
                )
                return redirect("add_game")
        else:
            context = request.session['context']
            form = GameCreationForm()
            context["form"] = form
            return render(request, "collection/add_game.html", context)
    return redirect("index")

def add_DLC(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = DLCCreationForm(
                request.POST, request.FILES, current_user=request.user)
            if form.is_valid():
                gameowned_id = form.cleaned_data["gameowned_id"]
                gamedlc_id = form.cleaned_data["gamedlc_id"]
                gamedlc_name = form.cleaned_data["gamedlc_name"]
                physical = form.cleaned_data["physical"]
                picture = form.cleaned_data["picture"]
                box_condition = form.cleaned_data["box_condition"]
                covers_condition = form.cleaned_data["covers_condition"]
                manual_condition = form.cleaned_data["manual_condition"]
                gamedlc_condition = form.cleaned_data["gamedlc_condition"]
                condition_precision = form.cleaned_data["condition_precision"]
                rating = form.cleaned_data["rating"]
                rating_precision = form.cleaned_data["rating_precision"]
                owning_status = form.cleaned_data["owning_status"]
                new_dlc = UserOwnedGameDLC(
                    user=request.user,
                    gameowned_id=gameowned_id,
                    gamedlc_id=gamedlc_id,
                    gamedlc_name=gamedlc_name,
                    physical=physical,
                    picture=picture,
                    box_condition=box_condition,
                    covers_condition=covers_condition,
                    manual_condition=manual_condition,
                    gamedlc_condition=gamedlc_condition,
                    condition_precision=condition_precision,
                    rating=rating,
                    rating_precision=rating_precision,
                    owning_status=owning_status
                    )
                new_dlc.save()
                request.session["context"] = user_plateforms(
                    request, UserOwnedGame, Plateform, ELEM
                )
                return render(request, "collection/collection.html", request.session["context"])
        else:
            context = request.session['context']
            form = DLCCreationForm(current_user=request.user)
            context["form"] = form
            return render(request, "collection/add_DLC.html", context)
    return redirect("index")

def add_comp(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = CompilCreationForm(request.POST, request.FILES)
            if form.is_valid():
                compilation_id = form.cleaned_data["compilation_id"]
                compilation_name = form.cleaned_data["compilation_name"]
                if compilation_id is None:
                    plateform_id = form.cleaned_data["plateform_id"]
                else:
                    plateform_id = get_object_or_404(
                        Compilation.objects.filter(id=compilation_id.id))
                    plateform_id = plateform_id.plateform
                physical = form.cleaned_data["physical"]
                picture = form.cleaned_data["picture"]
                box_condition = form.cleaned_data["box_condition"]
                covers_condition = form.cleaned_data["covers_condition"]
                manual_condition = form.cleaned_data["manual_condition"]
                game_condition = form.cleaned_data["game_condition"]
                condition_precision = form.cleaned_data["condition_precision"]
                owning_status = form.cleaned_data["owning_status"]
                new_comp = UserOwnedCompilation(
                    user=request.user,
                    compilation_id=compilation_id,
                    compilation_name=compilation_name,
                    plateform_id=plateform_id,
                    physical=physical,
                    picture=picture,
                    box_condition=box_condition,
                    covers_condition=covers_condition,
                    manual_condition=manual_condition,
                    game_condition=game_condition,
                    condition_precision=condition_precision,
                    owning_status=owning_status
                    )
                new_comp.save()
                #todo return to comp page
                return return_index(request, render)
        else:
            context = request.session['context']
            form = CompilCreationForm()
            context["form"] = form
            return render(request, "collection/add_comp.html", context)
    return redirect("index")

def add_console(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = PlateformCreationForm(request.POST, request.FILES)
            if form.is_valid():
                subplateform = form.cleaned_data["subplateform"]
                picture = form.cleaned_data["picture"]
                box_condition = form.cleaned_data["box_condition"]
                manual_condition = form.cleaned_data["manual_condition"]
                subplateform_condition = form.cleaned_data[
                    "subplateform_condition"]
                condition_precision = form.cleaned_data["condition_precision"]
                new_plat = UserOwnedSubPlateform(
                    user=request.user,
                    subplateform=subplateform,
                    picture=picture,
                    box_condition=box_condition,
                    manual_condition=manual_condition,
                    subplateform_condition=subplateform_condition,
                    condition_precision=condition_precision
                    )
                new_plat.save()
                #todo return to plateform list page
                return return_index(request, render)
        else:
            context = request.session['context']
            form = PlateformCreationForm()
            context["form"] = form
            return render(request, "collection/add_console.html", context)
    return redirect("index")

def add_addon(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = PlateformAddonCreationForm(request.POST, request.FILES)
            if form.is_valid():
                plateformaddon = form.cleaned_data["plateformaddon"]
                picture = form.cleaned_data["picture"]
                box_condition = form.cleaned_data["box_condition"]
                manual_condition = form.cleaned_data["manual_condition"]
                plateformaddon_condition = form.cleaned_data[
                    "plateformaddon_condition"]
                condition_precision = form.cleaned_data["condition_precision"]
                new_addon = UserOwnedPlateformAddon(
                    user=request.user,
                    plateformaddon=plateformaddon,
                    picture=picture,
                    box_condition=box_condition,
                    manual_condition=manual_condition,
                    plateformaddon_condition=plateformaddon_condition,
                    condition_precision=condition_precision
                    )
                new_addon.save()
                #todo return to accessory list page
                return return_index(request, render)
        else:
            context = request.session['context']
            form = PlateformAddonCreationForm()
            context["form"] = form
            return render(request, "collection/add_addon.html", context)
    return redirect("index")

def user_collection(request, plateform_id):

    if request.user.is_authenticated:
        if plateform_id == "0" or plateform_id.isdigit() is False:
            user_games = UserOwnedGame.objects.filter(user=request.user)
        else:
            user_games = UserOwnedGame.objects.filter(
                plateform_id=plateform_id,
                user=request.user
                )
        finished_litteral = ["Pas fini", "Fini", "Fini à 100%",
                             "N'a pas de fin", "Abandonné"]
        game_set = []
        for item in user_games:
            item.completion_status = finished_litteral[item.completion_status
                 - 1]
            game_set.append(item)
        context = request.session['context']
        context["game_set"] = game_set
        return render(request, "collection/collection.html", context)
    return redirect("index")

def user_accessory(request, plateform_id):

    #to be done
    if request.user.is_authenticated:
        if plateform_id == "0" or plateform_id.isdigit() is False:
            user_games = UserOwnedGame.objects.filter(user=request.user)
        else:
            user_games = UserOwnedGame.objects.filter(
                plateform_id=plateform_id,
                user=request.user
                )
        finished_litteral = ["Pas fini", "Fini", "Fini à 100%",
                             "N'a pas de fin", "Abandonné"]
        game_set = []
        for item in user_games:
            item.completion_status = finished_litteral[item.completion_status
                 - 1]
            game_set.append(item)
        context = request.session['context']
        context["game_set"] = game_set
        return render(request, "collection/collection.html", context)
    return redirect("index")

def user_consoles(request, plateform_id):

    #to be done
    if request.user.is_authenticated:
        if plateform_id == "0" or plateform_id.isdigit() is False:
            user_games = UserOwnedGame.objects.filter(user=request.user)
        else:
            user_games = UserOwnedGame.objects.filter(
                plateform_id=plateform_id,
                user=request.user
                )
        finished_litteral = ["Pas fini", "Fini", "Fini à 100%",
                             "N'a pas de fin", "Abandonné"]
        game_set = []
        for item in user_games:
            item.completion_status = finished_litteral[item.completion_status
                 - 1]
            game_set.append(item)
        context = request.session['context']
        context["game_set"] = game_set
        return render(request, "collection/collection.html", context)
    return redirect("index")

def user_compilations(request, plateform_id):

    #to be done
    if request.user.is_authenticated:
        if plateform_id == "0" or plateform_id.isdigit() is False:
            user_games = UserOwnedGame.objects.filter(user=request.user)
        else:
            user_games = UserOwnedGame.objects.filter(
                plateform_id=plateform_id,
                user=request.user
                )
        finished_litteral = ["Pas fini", "Fini", "Fini à 100%",
                             "N'a pas de fin", "Abandonné"]
        game_set = []
        for item in user_games:
            item.completion_status = finished_litteral[item.completion_status
                 - 1]
            game_set.append(item)
        context = request.session['context']
        context["game_set"] = game_set
        return render(request, "collection/collection.html", context)
    return redirect("index")

def user_game_page(request, game_id):

    #to be done
    if request.user.is_authenticated:
        if request.method == "POST":
            user_game = get_object_or_404(UserOwnedGame.objects.filter(
                id=game_id, user=request.user))
            form = GameModificationForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data["game_id"] is not None:
                    if user_game.game_id is None:
                        user_game.plateform_id = form.cleaned_data[
                            "plateform_id"]
                else:
                    user_game.game_id = form.cleaned_data["game_id"]
                    plateform_id = get_object_or_404(
                        Games.objects.filter(id=user_game.game_id.id))
                    user_game.plateform_id = plateform_id.plateform
                user_game.game_name = form.cleaned_data["game_name"]
                user_game.compilation = form.cleaned_data["compilation"]
                user_game.physical = form.cleaned_data["physical"]
                user_game.picture = form.cleaned_data["picture"]
                user_game.box_condition = form.cleaned_data[
                    "box_condition"]
                user_game.covers_condition = form.cleaned_data[
                    "covers_condition"]
                user_game.manual_condition = form.cleaned_data[
                    "manual_condition"]
                user_game.game_condition = form.cleaned_data[
                    "game_condition"]
                user_game.condition_precision = form.cleaned_data[
                    "condition_precision"]
                user_game.rating = form.cleaned_data["rating"]
                user_game.rating_precision = form.cleaned_data[
                    "rating_precision"]
                user_game.never_played = form.cleaned_data["never_played"]
                user_game.completion_status = form.cleaned_data[
                    "completion_status"]
                user_game.completion_precision = form.cleaned_data[
                    "completion_precision"]
                user_game.achievements_earned = form.cleaned_data[
                    "achievements_earned"]
                user_game.achievements_to_be_earned = form.cleaned_data[
                    "achievements_to_be_earned"]
                user_game.owning_status = form.cleaned_data[
                    "owning_status"]
                user_game.save()
        user_game = get_object_or_404(UserOwnedGame.objects.filter(
            id=game_id, user=request.user))
        form = GameModificationForm()
        context = {
            "username": request.session["context"]["username"],
            "email": request.session["context"]["email"],
            "name": request.session["context"]["name"],
            "form": form,
            "user_game": user_game,
            "profil_pic": request.session["context"]["profil_pic"],
            "platfor_user": request.session["context"]["platfor_user"]
        }
        return render(request, "collection/game_page.html", context)
    else:
        return return_index(request, render)
