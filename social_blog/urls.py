"""social_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.views.static import serve 
from django.urls import re_path

urlpatterns = [
    path('admin-dj/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('social.urls',namespace='posts')),
    path('', include('profiles.urls',namespace='profile')),
]

# if settings.DEBUG:
#     urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,}),]
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,}),]

# handler404 = 'social.views.error_404'
# handler403 = 'social.views.error_403'
# handler400 = 'social.views.error_400'

# handler404 = 'profiles.views.error_404'
# handler403 = 'profiles.views.error_403'
# handler400 = 'profiles.views.error_400'

