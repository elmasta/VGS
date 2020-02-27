from collection.classes import *
from collection.forms import UserCreationForm, ParagraphErrorList
from collection.tokens import account_activation_token
from django.http import HttpResponse
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

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
            if password == request.POST.get('CheckPassword') and not user.exists():
                User.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name)
                user = User.objects.get(email=email)
                user.is_active = False
                #current_site = get_current_site(request)
                mail_subject = "Activez votre compte VGS."
                message = render_to_string('collection/acc_active_email.html', {
                    'user': user,
                    #'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.id)),
                    'token':account_activation_token.make_token(user)
                })
                to_email = EmailMessage(
                    mail_subject, message, to=[email]
                )
                to_email.send()
                return render(request, "collection/login.html")
            else:
                context['errors'] = form.errors.items()
        else:
            context['errors'] = form.errors.items()
    else:
        form = UserCreationForm()
    context["form"] = form
    return render(request, 'collection/register.html', context)

def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
