"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework import routers

from config import settings
from newsportal import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewset)
router.register(r'articles', views.ArticlesViewset)


urlpatterns = [
    path('api/', include(router.urls)),
    path('i18n/', include('django.conf.urls.i18n')),

    path('admin/', admin.site.urls),
    path('', include('newsportal.urls')),
    path('accounts/', include('allauth.urls')),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]

