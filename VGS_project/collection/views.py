from collection.classes import *
from collection.forms import UserCreationForm, ParagraphErrorList
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User

def index(request):

    return render(request, "collection/index.html")

def login_page(request):

    return render(request, "collection/login.html")

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
            if user.exists():
                #error
                pass
            else:
                User.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name)
            # todo context = {}
        else:
            context['errors'] = form.errors.items()
    else:
        form = UserCreationForm()
    context["form"] = form
    return render(request, 'collection/register.html', context)
