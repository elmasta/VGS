from collection.func import *
from collection.forms import *
from collection.tokens import account_activation_token
from collection.models import UserData, Games, UserOwnedGame, Plateform,\
    UserOwnedSubPlateform, CollectionPicture, ELEM, Compilation
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

def index(request):

    user_games = UserOwnedGame.objects.values("game_id_id").annotate(
        c=Count("game_id")).order_by('-c')[:10]
    games_name = []
    for item in user_games:
        if item["game_id_id"] is not None:
            game = Games.objects.get(id=item["game_id_id"])
            games_name.append({"name": game.name,
                               "plateform": game.plateform,
                               "count": item["c"]})
    if request.user.is_authenticated:
        context = request.session["context"]
        context["games_name"] = games_name
        return render(request, "collection/index.html", context)
    return render(
        request, "collection/index.html", {"games_name": games_name})

def about(request):

    if request.user.is_authenticated:
        return render(
            request, "collection/about.html", request.session["context"])
    return render(request, "collection/about.html")

def login_page(request):

    context = {}
    if request.user.is_authenticated:
        return redirect("index")
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
                context["errors"] = "Compte non actif ou mot de passe invalide"
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

    if request.user.is_authenticated:
        logout(request)
    return redirect("index")

def profile_page(request):

    if request.user.is_authenticated:
        if request.method == "POST":
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
            elif request.POST.get("NewPassword") and\
                request.POST.get("CheckPasswordChange") and\
                request.POST.get("NewPassword") ==\
                request.POST.get("CheckPasswordChange"):
                user = User.objects.get(id=request.user.id)
                user.set_password(request.POST.get("NewPassword"))
                user.save()
                return redirect("user_logout")
        addprofpicform = ChangeAvatarForm()
        if request.session["context"]["profil_pic"] is not None:
            user_pic = UserData.objects.get(user=request.user)
        context = {
            "username": request.session["context"]["username"],
            "email": request.session["context"]["email"],
            "name": request.session["context"]["name"],
            "addprofpicform": addprofpicform,
            "date_joined": request.user.date_joined,
            "staff": request.user.is_staff,
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
                if game_id is None:
                    plateform_id = form.cleaned_data["plateform_id"]
                else:
                    game_item = get_object_or_404(
                        Games.objects.filter(id=game_id.id))
                    plateform_id = game_item.plateform
                new_game = UserOwnedGame(
                    user=request.user,
                    game_id=game_id,
                    game_name=form.cleaned_data["game_name"],
                    plateform_id=plateform_id,
                    compilation=form.cleaned_data["compilation"],
                    physical=form.cleaned_data["physical"],
                    picture=form.cleaned_data["picture"],
                    box_condition=form.cleaned_data["box_condition"],
                    covers_condition=form.cleaned_data["covers_condition"],
                    manual_condition=form.cleaned_data["manual_condition"],
                    game_condition=form.cleaned_data["game_condition"],
                    condition_precision=form.cleaned_data[
                        "condition_precision"],
                    rating=form.cleaned_data["rating"],
                    rating_precision=form.cleaned_data["rating_precision"],
                    never_played=form.cleaned_data["never_played"],
                    completion_status=form.cleaned_data["completion_status"],
                    completion_precision=form.cleaned_data[
                        "completion_precision"],
                    achievements_earned=form.cleaned_data[
                        "achievements_earned"],
                    achievements_to_be_earned=form.cleaned_data[
                        "achievements_to_be_earned"],
                    owning_status=form.cleaned_data["owning_status"]
                    )
                new_game.save()
                request.session["context"] = user_plateforms(
                    request, UserOwnedGame, Plateform, ELEM
                )
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
                new_dlc = UserOwnedGameDLC(
                    user=request.user,
                    gameowned_id=form.cleaned_data["gameowned_id"],
                    gamedlc_id=form.cleaned_data["gamedlc_id"],
                    gamedlc_name=form.cleaned_data["gamedlc_name"],
                    physical=form.cleaned_data["physical"],
                    picture=form.cleaned_data["picture"],
                    box_condition=form.cleaned_data["box_condition"],
                    covers_condition=form.cleaned_data["covers_condition"],
                    manual_condition=form.cleaned_data["manual_condition"],
                    gamedlc_condition=form.cleaned_data["gamedlc_condition"],
                    condition_precision=form.cleaned_data[
                        "condition_precision"],
                    rating=form.cleaned_data["rating"],
                    rating_precision=form.cleaned_data["rating_precision"],
                    owning_status=form.cleaned_data["owning_status"]
                    )
                new_dlc.save()
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
                if compilation_id is None:
                    plateform_id = form.cleaned_data["plateform_id"]
                else:
                    plateform_id = get_object_or_404(
                        Compilation.objects.filter(id=compilation_id.id))
                    plateform_id = plateform_id.plateform
                new_comp = UserOwnedCompilation(
                    user=request.user,
                    compilation_id=compilation_id,
                    compilation_name=form.cleaned_data["compilation_name"],
                    plateform_id=plateform_id,
                    physical=form.cleaned_data["physical"],
                    picture=form.cleaned_data["picture"],
                    box_condition=form.cleaned_data["box_condition"],
                    covers_condition=form.cleaned_data["covers_condition"],
                    manual_condition=form.cleaned_data["manual_condition"],
                    game_condition=form.cleaned_data["game_condition"],
                    condition_precision=form.cleaned_data[
                        "condition_precision"],
                    owning_status=form.cleaned_data["owning_status"]
                    )
                new_comp.save()
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
                new_plat = UserOwnedSubPlateform(
                    user=request.user,
                    subplateform=form.cleaned_data["subplateform"],
                    picture=form.cleaned_data["picture"],
                    box_condition=form.cleaned_data["box_condition"],
                    manual_condition=form.cleaned_data["manual_condition"],
                    subplateform_condition=form.cleaned_data[
                        "subplateform_condition"],
                    condition_precision=form.cleaned_data[
                        "condition_precision"]
                    )
                new_plat.save()
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
                new_addon = UserOwnedPlateformAddon(
                    user=request.user,
                    plateformaddon=form.cleaned_data["plateformaddon"],
                    picture=form.cleaned_data["picture"],
                    box_condition=form.cleaned_data["box_condition"],
                    manual_condition=form.cleaned_data["manual_condition"],
                    plateformaddon_condition=form.cleaned_data[
                        "plateformaddon_condition"],
                    condition_precision=form.cleaned_data[
                        "condition_precision"]
                    )
                new_addon.save()
        context = request.session['context']
        form = PlateformAddonCreationForm()
        context["form"] = form
        return render(request, "collection/add_addon.html", context)
    return redirect("index")

def user_collection(request, plateform_id):

    if request.user.is_authenticated:
        if plateform_id.isdecimal():
            if plateform_id == "0" or plateform_id.isdecimal() is False:
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
                item.completion_status =\
                    finished_litteral[item.completion_status - 1]
                game_set.append(item)
            context = request.session['context']
            context["game_set"] = game_set
            return render(request, "collection/collection.html", context)
    return redirect("index")

def user_game_page(request, game_id):

    if request.user.is_authenticated:
        if game_id.isdecimal():
            user_game = get_object_or_404(UserOwnedGame.objects.filter(
                id=game_id, user=request.user))
            if request.method == "POST":
                if request.POST.get("delete") is None:
                    form = GameCreationForm(
                        request.POST,
                        request.FILES,
                        current_user=request.user)
                    if form.is_valid():
                        user_game.game_id = form.cleaned_data["game_id"]
                        user_game.game_name = form.cleaned_data["game_name"]
                        if game_id is None:
                            user_game.plateform_id = form.cleaned_data[
                                "plateform_id"]
                        else:
                            game_item = get_object_or_404(
                                Games.objects.filter(id=user_game.game_id.id))
                            user_game.plateform_id = game_item.plateform
                        user_game.compilation = form.cleaned_data[
                            "compilation"]
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
                        user_game.never_played = form.cleaned_data[
                            "never_played"]
                        user_game.completion_status = form.cleaned_data[
                            "completion_status"]
                        user_game.completion_precision = form.cleaned_data[
                            "completion_precision"]
                        user_game.achievements_earned = form.cleaned_data[
                            "achievements_earned"]
                        user_game.achievements_to_be_earned =\
                            form.cleaned_data["achievements_to_be_earned"]
                        user_game.owning_status = form.cleaned_data[
                            "owning_status"]
                        user_game.save()
                        request.session["context"] = user_plateforms(
                            request, UserOwnedGame, Plateform, ELEM
                        )
                else:
                    UserOwnedGame.objects.get(
                        id=request.POST.get("delete")).delete()
                    request.session["context"] = user_plateforms(
                        request, UserOwnedGame, Plateform, ELEM
                    )
                    return redirect("user_collection", plateform_id=0)
            user_dlc = UserOwnedGameDLC.objects.filter(
                gameowned_id=user_game.id
            )
            form = GameCreationForm(instance=user_game)
            context = {
                "username": request.session["context"]["username"],
                "email": request.session["context"]["email"],
                "name": request.session["context"]["name"],
                "form": form,
                "modify": True,
                "user_game": user_game,
                "user_dlc": user_dlc,
                "profil_pic": request.session["context"]["profil_pic"],
                "platfor_user": request.session["context"]["platfor_user"]
            }
            return render(request, "collection/add_game.html", context)
    return redirect("index")

def user_accessory(request):

    if request.user.is_authenticated:
        user_plateform_addon = UserOwnedPlateformAddon.objects.filter(
            user=request.user
        )
        context = request.session['context']
        context["user_plateform_addon"] = user_plateform_addon
        return render(
            request, "collection/accessory_collection.html", context)
    return redirect("index")

def user_accessory_page(request, accessory_id):

    if request.user.is_authenticated:
        if accessory_id.isdecimal():
            user_access = get_object_or_404(
                UserOwnedPlateformAddon.objects.filter(
                    id=accessory_id, user=request.user))
            if request.method == "POST":
                if request.POST.get("delete") is None:
                    form = PlateformAddonCreationForm(
                        request.POST, request.FILES)
                    if form.is_valid():
                        user_access.plateformaddon =\
                            form.cleaned_data["plateformaddon"]
                        user_access.picture = form.cleaned_data["picture"]
                        user_access.box_condition =\
                            form.cleaned_data["box_condition"]
                        user_access.manual_condition =\
                            form.cleaned_data["manual_condition"]
                        user_access.plateformaddon_condition =\
                            form.cleaned_data["plateformaddon_condition"]
                        user_access.condition_precision =\
                            form.cleaned_data["condition_precision"]
                        user_access.save()
                else:
                    UserOwnedPlateformAddon.objects.get(
                        id=request.POST.get("delete")).delete()
                    return redirect("user_accessory")
            form = PlateformAddonCreationForm(instance=user_access)
            context = {
                "username": request.session["context"]["username"],
                "email": request.session["context"]["email"],
                "name": request.session["context"]["name"],
                "form": form,
                "modify": True,
                "user_access": user_access,
                "profil_pic": request.session["context"]["profil_pic"],
                "platfor_user": request.session["context"]["platfor_user"]
            }
            return render(request, "collection/add_addon.html", context)
    return redirect("index")

def user_consoles(request):

    if request.user.is_authenticated:
        user_subplateform = UserOwnedSubPlateform.objects.filter(
            user=request.user
        )
        context = request.session['context']
        context["user_subplateform"] = user_subplateform
        return render(
            request, "collection/subplateform_collection.html", context)
    return redirect("index")

def user_consoles_page(request, consoles_id):

    if request.user.is_authenticated:
        if consoles_id.isdecimal():
            user_plat = get_object_or_404(
                UserOwnedSubPlateform.objects.filter(
                    id=consoles_id, user=request.user))
            if request.method == "POST":
                if request.POST.get("delete") is None:
                    form = PlateformCreationForm(
                        request.POST, request.FILES)
                    if form.is_valid():
                        picture = form.cleaned_data["picture"]
                        user_plat.subplateform =\
                            form.cleaned_data["subplateform"]
                        user_plat.picture = picture
                        user_plat.box_condition =\
                            form.cleaned_data["box_condition"]
                        user_plat.manual_condition =\
                            form.cleaned_data["manual_condition"]
                        user_plat.subplateform_condition =\
                            form.cleaned_data["subplateform_condition"]
                        user_plat.condition_precision =\
                            form.cleaned_data["condition_precision"]
                        user_plat.save()
                else:
                    UserOwnedSubPlateform.objects.get(
                        id=request.POST.get("delete")).delete()
                    return redirect("user_consoles")
            form = PlateformCreationForm(instance=user_plat)
            context = {
                "username": request.session["context"]["username"],
                "email": request.session["context"]["email"],
                "name": request.session["context"]["name"],
                "form": form,
                "modify": True,
                "user_plat": user_plat,
                "profil_pic": request.session["context"]["profil_pic"],
                "platfor_user": request.session["context"]["platfor_user"]
            }
            return render(request, "collection/add_console.html", context)
    return redirect("index")

def user_compilations(request):

    if request.user.is_authenticated:
        user_comp = UserOwnedCompilation.objects.filter(
            user=request.user
        )
        context = request.session['context']
        context["user_comp"] = user_comp
        return render(request, "collection/comp_collection.html", context)
    return redirect("index")

def user_compilations_page(request, compilations_id):

    if request.user.is_authenticated:
        if compilations_id.isdecimal():
            user_comp = get_object_or_404(
                UserOwnedCompilation.objects.filter(
                    id=compilations_id))
            if request.method == "POST":
                if request.POST.get("delete") is None:
                    form = CompilCreationForm(
                        request.POST, request.FILES)
                    if form.is_valid():
                        user_comp.compilation_id = form.cleaned_data[
                            "compilation_id"]
                        user_comp.compilation_name = form.cleaned_data[
                            "compilation_name"]
                        if user_comp.compilation_id is None:
                            user_comp.plateform_id = form.cleaned_data[
                                "plateform_id"]
                        else:
                            plateform_id = get_object_or_404(
                                Compilation.objects.filter(
                                    id=user_comp.compilation_id.id))
                            user_comp.plateform_id = plateform_id.plateform
                        user_comp.physical = form.cleaned_data["physical"]
                        user_comp.picture = form.cleaned_data["picture"]
                        user_comp.box_condition = form.cleaned_data[
                            "box_condition"]
                        user_comp.covers_condition = form.cleaned_data[
                            "covers_condition"]
                        user_comp.manual_condition = form.cleaned_data[
                            "manual_condition"]
                        user_comp.game_condition = form.cleaned_data[
                            "game_condition"]
                        user_comp.condition_precision = form.cleaned_data[
                            "condition_precision"]
                        user_comp.owning_status = form.cleaned_data[
                            "owning_status"]
                        user_comp.save()
                else:
                    UserOwnedCompilation.objects.get(
                        id=request.POST.get("delete")).delete()
                    return redirect("user_compilations")
            form = CompilCreationForm(instance=user_comp)
            context = {
                "username": request.session["context"]["username"],
                "email": request.session["context"]["email"],
                "name": request.session["context"]["name"],
                "form": form,
                "modify": True,
                "user_comp": user_comp,
                "profil_pic": request.session["context"]["profil_pic"],
                "platfor_user": request.session["context"]["platfor_user"]
            }
            return render(request, "collection/add_comp.html", context)
    return redirect("index")

def user_dlc_page(request, dlc_id):

    if request.user.is_authenticated:
        if dlc_id.isdecimal():
            user_dlc = get_object_or_404(
                UserOwnedGameDLC.objects.filter(
                    id=dlc_id))
            if request.method == "POST":
                if request.POST.get("delete") is None:
                    form = DLCCreationForm(
                        request.POST, request.FILES)
                    if form.is_valid():
                        user_dlc.gameowned_id = form.cleaned_data[
                            "gameowned_id"]
                        user_dlc.gamedlc_id = form.cleaned_data[
                            "gamedlc_id"]
                        user_dlc.gamedlc_name = form.cleaned_data[
                            "gamedlc_name"]
                        user_dlc.physical = form.cleaned_data["physical"]
                        user_dlc.picture = form.cleaned_data["picture"]
                        user_dlc.box_condition = form.cleaned_data[
                            "box_condition"]
                        user_dlc.covers_condition = form.cleaned_data[
                            "covers_condition"]
                        user_dlc.manual_condition = form.cleaned_data[
                            "manual_condition"]
                        user_dlc.gamedlc_condition = form.cleaned_data[
                            "gamedlc_condition"]
                        user_dlc.condition_precision = form.cleaned_data[
                            "condition_precision"]
                        user_dlc.rating = form.cleaned_data["rating"]
                        user_dlc.rating_precision = form.cleaned_data[
                            "rating_precision"]
                        user_dlc.owning_status = form.cleaned_data[
                            "owning_status"]
                        user_dlc.save()
                else:
                    UserOwnedGameDLC.objects.get(
                        id=request.POST.get("delete")).delete()
                    return redirect("user_game_page",
                                    game_id=form.cleaned_data["gameowned_id"])
            form = DLCCreationForm(instance=user_dlc)
            context = {
                "username": request.session["context"]["username"],
                "email": request.session["context"]["email"],
                "name": request.session["context"]["name"],
                "form": form,
                "modify": True,
                "user_dlc": user_dlc,
                "profil_pic": request.session["context"]["profil_pic"],
                "platfor_user": request.session["context"]["platfor_user"]
            }
            return render(request, "collection/add_DLC.html", context)
    return redirect("index")
