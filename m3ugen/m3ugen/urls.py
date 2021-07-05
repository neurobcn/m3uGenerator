"""m3ugen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from m3uservers.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('upload/', uploadM3U, name='uploadM3U'),
    path('list/', listM3U, name='listM3U'),
    #path('update/<str:id>/', updateM3U, name='updateM3U'),
    path('updateList/<str:id>/', updateList, name='updateList'),
    path('update_canal/<str:idm3u>/<str:idcanal>/', updateCanal, name='update_canal'),
    path('delete/<str:id>/', deleteM3U, name = 'delete'),
    path('reload/<str:id>/', reloadList, name = 'reloadList'),
    #path("canal/<str:id>/", updList, name = 'canal_list'),
    path("playlink/<str:idm3u>/<str:idCanal>", playLink, name = 'playLink'),

]
