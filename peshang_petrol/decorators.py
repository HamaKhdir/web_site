from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect


def unauthenticated_user(view_fun):
    def wrapper_fun(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_fun(request,*args,**kwargs)
    return wrapper_fun    

def allowed_users(allowed_roles=[]):
    def decorator(view_fun):
        def wrapper_fun(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_fun(request,*args,**kwargs)
            else:
                #return HttpResponse("<h1><center>You can't go to this page!</center></h1>")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return wrapper_fun
    return decorator        


def admin_only(view_fun):
    def wrapper_fun(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'peshang_user':
            return redirect('index')
            
        if group == 'peshang_admin':
            return view_fun(request,*args,**kwargs)
        else:
            return HttpResponse("Sorry you are fake user!")

    return wrapper_fun
   
