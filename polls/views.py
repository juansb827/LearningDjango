# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Imagen, ImageForm, UserForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
import json

# Create your views here.
@csrf_exempt
def index(request):
    if request.user.is_authenticated():
        lista_imagenes=Imagen.objects.filter(user=request.user)
    else:
        lista_imagenes=Imagen.objects.all()
    return HttpResponse(serializers.serialize("json", lista_imagenes))


@csrf_exempt
def add_image(request):
    if request.method=='POST':
        new_imagen=Imagen(url=request.POST['url'],
                          title=request.POST['title'],
                          description=request.POST.get('description'),
                          type=request.POST.get('type'),
                          imageFile=request.FILES.get('imageFile'),
                          user=request.user)
        new_imagen.save()
    return HttpResponse(serializers.serialize("json", [new_imagen]))


@csrf_exempt
def add_user(request):
    if request.method == "POST":
        jsonUser = json.loads(request.body)
        username = jsonUser.get('username')
        first_name = jsonUser.get('first_name')
        last_name = jsonUser.get('last_name')
        password = jsonUser.get('password')
        email = jsonUser.get('email')

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()

    return HttpResponse(serializers.serialize("json", [user_model]))


@csrf_exempt
def login_view(request):
    print "LOGIN attemp"
    if request.method=="POST":

        jsonUser= json.loads(request.body)

        username = jsonUser['username']
        password = jsonUser['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            mensaje = "ok"
        else:
            mensaje = "Invalido"


    return JsonResponse({"mensaje":mensaje})


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"mensaje": "ok"})


@csrf_exempt
def isLoggedView_view(request):
    if request.user.is_authenticated():
        mensaje="ok"
    else:
        mensaje="no"

    return JsonResponse({"mensaje":mensaje})

def ver_imagenes(request):
    return render(request,"polls/index.html")

def agregar_imagen(request):
    return render(request,"polls/image_form.html")

def agregar_usuario(request):
    return render(request,"polls/registro.html")

def ingresar(request):
    return render(request,"polls/login.html")






















