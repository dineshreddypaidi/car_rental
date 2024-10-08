from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
    #admin's
    #path('admin/',include('admins.urls')),
    path('kmrwheels/default/admin/', admin.site.urls),
    ##--------##
    path('',include('main.urls')),
    #path('api/',include('api.urls')),
    path('user/',include('user.urls')),
    path('vechiles/',include('vechiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)