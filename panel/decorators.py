from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from installation.models import SiteModel
def unauthenticated_user(view_func):
    def wrapper_func(request, *args , **kwrags):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            return view_func(request, *args , **kwrags)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args , **kwrags):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args , **kwrags)
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'permission':True,'valid':False,'message':'Permission denied.'},content_type='application/json')
                else:
                    obj=SiteModel.objects.all()[0]
                    return render(request,'panel/403.html',{'title':'Access Forbidden','obj':obj})
        return wrapper_func
    return decorator


