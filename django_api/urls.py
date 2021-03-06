"""api_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from asw_api import views
from .views import *
from django.contrib.auth.views import logout
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Issue Tracker API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/logout/$', logout, {'next_page':'/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(settings.API_BASE_URL, include('asw_api.urls')),
    url(r'^$', schema_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

