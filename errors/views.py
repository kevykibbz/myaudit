from django.shortcuts import render
from installation.models import SiteModel



def error_400(request,exception):
    obj=SiteModel.objects.all()[0]
    data={
            'title':'Error | Bad Request',
            'obj':obj
    }
    return render(request,'panel/400.html',context=data,status=400)

def error_403(request,exception):
    obj=SiteModel.objects.all()[0]
    data={
            'title':'Error | Access Forbidden',
            'obj':obj
    }
    return render(request,'panel/403.html',context=data,status=403)

def error_404(request,exception):
    obj=SiteModel.objects.all()[0]
    data={
            'title':'Error | Page Not Found',
            'obj':obj
    }
    return render(request,'panel/404.html',context=data,status=404)

def error_500(request,*args,**argv):
    obj=SiteModel.objects.all()[0]
    data={
            'title':'Error | Internal Server Error',
            'obj':obj
    }
    return render(request,'panel/500.html',context=data,status=500)

