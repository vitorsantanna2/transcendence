"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.shortcuts import render
import os

def home_view(request):
    return render(request, 'chat/index.html')

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]

# Configuração para servir arquivos estáticos durante o desenvolvimento
urlpatterns += [
    re_path(r'^images/(?P<path>.*)$', serve, {
        'document_root': os.path.join('/Users/pedrosydenstricker/Desktop/42/42Cursus/em_andamento/trans_phil/front/bootstrap/mysite/chat/templates', 'images'),
    }),
    re_path(r'^styles/(?P<path>.*)$', serve, {
        'document_root': '/Users/pedrosydenstricker/Desktop/42/42Cursus/em_andamento/trans_phil/front/bootstrap/mysite/chat/templates/chat',
    }),
    re_path(r'^scripts/(?P<path>.*)$', serve, {
        'document_root': '/Users/pedrosydenstricker/Desktop/42/42Cursus/em_andamento/trans_phil/front/bootstrap/mysite/chat/templates/chat',
    }),
]
