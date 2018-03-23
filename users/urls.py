from django.conf.urls import url, include

from .api import *

app_name = 'users'


api_urls = [

    url(r'^new/$', CreateUser.as_view(), name='new-user'),
]

urlpatterns = [
    # url(r'^', include(app_urls)),

    # url(r'^app/', include(app_urls)),

    url(r'^api/', include(api_urls)),
]
