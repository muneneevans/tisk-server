"""tisk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

import membership_categories.urls
import users.urls
import member_types.urls
import members.urls
from users.api import TiskObtainJSONWebToken

urlpatterns = [
    url( r'^(?P<version>(v1))/',include([
        path('users/', include(users.urls.api_urls)),
        path('auth/', include([
            url(r'^login/?', obtain_jwt_token),
            url(r'^refreshtoken/?', TiskObtainJSONWebToken.as_view()),
        ])),
        path('members/', include(members.urls.api_urls)),
        path('member_types/', include(member_types.urls.api_urls)),
        path('membership_categories/', include(membership_categories.urls.api_urlpatterns)),
    ]))
]
