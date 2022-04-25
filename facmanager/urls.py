"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

"""facmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, reverse_lazy, include, re_path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView
import django_cas_ng.views

from facusers import views

urlpatterns = [
    path('su/', include('django_su.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('facusers.urls')),
    path('api/', include('faccore.urls')),
    re_path('^$', ensure_csrf_cookie(TemplateView.as_view(template_name="index.html"))),
    path('cas/login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('cas/logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
