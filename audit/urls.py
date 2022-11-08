from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/clearcache',include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('installation/',include('installation.urls')),
    path('', include('panel.urls')),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

handler400 ='errors.views.error_400'
handler403 ='errors.views.error_403'
handler404 ='errors.views.error_404'
handler500='errors.views.error_500'