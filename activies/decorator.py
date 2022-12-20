from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_fun):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_fun(request, *args, **kwargs)
    return wrapper_func
def allowed_users(allowed_roles = []):
    def decorator(view_fun):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_fun(request, *args, **kwargs)
            else:
                return redirect('vente')
        return wrapper_func
    return decorator
def only_admin(view_fun):
    
    def wrapper_funci(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'user':
            return redirect('vente')
        if group == 'admin':
            return view_fun(request, *args, **kwargs)
        
    return wrapper_funci

