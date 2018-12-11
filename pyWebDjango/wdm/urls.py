"""pyWebDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.apps import apps
import public.ViewTemplates
from public.LogHelper import logger
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', public.ViewTemplates.index)
]

for apc in [x.strip('<>').split(':') for x in re.findall(re.compile('<.*?>'), str(apps.get_app_configs()))]:
    if apc[0].strip() == 'AppConfig':
        try:
            urlpatterns.append(path(apc[1].strip()+'/', include(apc[1].strip()+'.views'), name=apc[1].strip()))
        except Exception as e:
            logger().warning('[include failed]-[{0}.views]-[{1}]'.format(apc[1].strip(), e))