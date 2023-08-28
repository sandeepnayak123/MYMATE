from django.http import HttpResponse
from django.shortcuts import redirect,render

def login_required(view_func):
    def wrapper_func(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('/users/register')
        else:
            return view_func(request,*args,*kwargs)
    return wrapper_func