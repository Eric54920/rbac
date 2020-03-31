'''
@Author: your name
@Date: 2019-11-28 14:26:20
@LastEditTime: 2019-11-28 21:25:14
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /luffy_permission/rbac/views.py
'''
from django.shortcuts import render, redirect
from . import  models
from django.conf import settings
from . import service

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = models.User.objects.filter(username=username, password=password).first()
        if obj:
            service.service(request, obj)
            return redirect('/index/')
        return redirect('/login/')
    return render(request, 'login.html')