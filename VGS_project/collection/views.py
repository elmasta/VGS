from collection.classes import *
from collection.forms import *
from collection.tokens import account_activation_token
from collection.models import UserData
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from PIL import Image

def index(request):

    return return_index(request, render)

def login_page(request):

    context = {}
    if request.method == "POST":
        form = UserLoginForm(request.POST, error_class=ParagraphErrorList)
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
                    picture = "https://source.unsplash.com/QAB-WJcbgJk/60x60"
                    #utilisé 2 fois à refactoriser
                    if UserData.objects.filter(user=request.user.id).exists():
                        user_pic = UserData.objects.get(user=request.user.id)
                        request.session['context']["profil_pic"] = user_pic.profil_picture.path
                    else:
                        request.session['context']["profil_pic"] = picture
                    return return_index(request, render)
                else:
                    #todo error message
                    form = UserLoginForm()
            else:
                context["errors"] = form.errors.items()
        else:
            context["errors"] = form.errors.items()
    else:
        form = UserLoginForm()
    context["form"] = form
    return render(request, "collection/login.html", context)

def register_page(request):

    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST, error_class=ParagraphErrorList)
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
                user = User.objects.get(email=email)
                current_site = get_current_site(request)
                mail_subject = "Activez votre compte VGS."
                message = render_to_string(
                    "collection/acc_active_email.html", {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.id)),
                        "token":account_activation_token.make_token(user)
                    })
                to_email = EmailMessage(
                    mail_subject, message, to=[email]
                )
                to_email.send()
                return return_index(request, render)
            else:
                context["inv_errors"] = "Email déjà utilisé"
        else:
            context["form_errors"] = form.errors.items()
    else:
        form = UserCreationForm()
    context["form"] = form
    return render(request, "collection/register.html", context)

def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        print("test")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print("test2")
    print(account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse("Thank you for your email confirmation. Now you can login your account.")
    else:
        return HttpResponse("Activation link is invalid!")

def user_logout(request):

    logout(request)
    return return_index(request, render)

def profile_page(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangeAvatarForm(request.POST, request.FILES)
            if form.is_valid():
                new_avatar = form.cleaned_data["profil_picture"]
                #utilisé deux fois à refactoriser
                if UserData.objects.filter(user=request.user).exists():
                    avatar = UserData.objects.get(user=request.user)
                    avatar.profil_picture = new_avatar
                    avatar.save()
                else:
                    avatar = UserData(profil_picture=new_avatar, user=request.user)
                    avatar.save()
            user_pic = UserData.objects.get(user=request.user)
            request.session['context']["profil_pic"] = user_pic.profil_picture.path
        context = request.session['context']
        form = ChangeAvatarForm()
        context["form"] = form
        context["date_joined"] = request.user.date_joined
        return render(request, "collection/profile.html", context)
    else:
        return login_page(request)

def add_game(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            pass
        else:
            context = request.session['context']
            form = GameCreationForm()
            context["form"] = form
            return render(request, "collection/add_item.html", context)
    else:
        return return_index(request, render)

def user_collection(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            pass
        else:
            return render(request, "collection/collection.html",
                          request.session['context'])
    else:
        return return_index(request, render)
