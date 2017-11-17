# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    result = User.objects.validateregistration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Sucessfully registered!")
    return redirect('/success')

def login(request):
    result = User.objects.validatelogin(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def show(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'first_app/show.html', context)