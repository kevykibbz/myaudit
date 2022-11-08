from django.shortcuts import render
from .forms import *
from  .models import SiteModel
from django.views.generic import View
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from panel.tokens import create_token
from django.contrib.sites.shortcuts import get_current_site
from  django.contrib.auth.models import Group
from django.core.cache import cache
from django.contrib.sites.models import Site


# Create your views here.
def installation(request):
	data={'title':'Site Installation | Powered By DevMe'}
	return render(request,'installation/installation.html',context=data)

class InstallationView(View):
	def get(self,request, *args, **kwargs):
		userform=AdminRegisterForm()
		extendedForm=ExtendedAdminRegisterForm()
		siteconstantform=SiteConfigForm()
		count=SiteModel.objects.count()
		data={
				'title':'Site Installation | Powered By DevMe',
				'userform':userform,
				'extendedForm':extendedForm,
				'siteconstantform':siteconstantform,
				'count':count
				}	
		return render(request,'installation/installation.html',context=data)
	def post(self,request):
		userform=AdminRegisterForm(request.POST or None)
		extendedForm=ExtendedAdminRegisterForm(request.POST or None)
		siteconstantform=SiteConfigForm(request.POST or None)
		if userform.is_valid() and extendedForm.is_valid() and siteconstantform.is_valid():
			user=userform.save(commit=False)
			user.is_superuser=True
			user.is_staff=True
			user.save()
			if not Group.objects.filter(name='admins').exists():
				group=Group.objects.create(name='admins')
				group.user_set.add(user)
				group.save()
			else:
				group=Group.objects.get(name__icontains='admins')
				group.user_set.add(user)
				group.save()
			extended=extendedForm.save(commit=False)
			extended.user=user
			extended.category='Admin'
			extended.initials=userform.cleaned_data.get('first_name')[0].upper()+userform.cleaned_data.get('last_name')[0].upper()
			extended.role='Admin'
			extended.save()
			lastdata=siteconstantform.save(commit=False)
			lastdata.is_installed=True
			lastdata.user=user
			lastdata.save()
			obj=Site.objects.create(name=siteconstantform.cleaned_data.get('site_name'),domain=siteconstantform.cleaned_data.get('site_url'))
			obj.save()
			return JsonResponse({'valid':True,'message':'Site Installed Successfully.'},content_type='application/json')
		else:
			return JsonResponse({'valid':False,'userform_errors':userform.errors,'extendedForm_errors':extendedForm.errors,'siteconstantform_errors':siteconstantform.errors},content_type='application/json')
