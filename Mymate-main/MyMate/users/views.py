from email import message
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import userregisterform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def register(request):
    if request.method=='POST':
        form=userregisterform(request.POST)
        if form.is_valid():
            messages.success(request,'hoorey!, You are registered successfully')
            form.save()
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            context={'username':username,'password':password}
            return render(request,'users/login.html',context)
        else:
            messages.error(request,'please enter the correct details')
    else:
        form=userregisterform()
    context={'form':form}
    return render(request,'users/register.html',context)


def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user= authenticate(request,username=username,password=password)
        if user is not None:
            
            login(request,user)
            
            messages.success(request,f'Welcome {username}')
            return redirect('home')
        else:
            messages.error(request,'Username or password is incorrect')
    return render(request,'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')