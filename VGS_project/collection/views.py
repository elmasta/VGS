from VGS_project.classes import *
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):

    template = loader.get_template('collection/index.html')
    return HttpResponse(template.render(request=request))

def login(request):

    template = loader.get_template('collection/login.html')
    return HttpResponse(template.render(request=request))

def register(request):

    template = loader.get_template('collection/register.html')
    return HttpResponse(template.render(request=request))
