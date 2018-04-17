from django.conf.urls import url, include

from .api import *

app_name = 'users'


api_urls = [

    url(r'^new/$', CreateUser.as_view(), name='new-user'),    
    url(r'^activate/$', ActivateUser.as_view(), name='activate-user'),
    url(r'^(?P<email>([\w+.]+)\@([\w+.]+))/$',
        RetrieveUserView.as_view(), name='user-view'),


    url(r'^(?P<email>([\w+.]+)\@([\w+.]+))/savings', include("savings.urls")),



]

urlpatterns = [
    # url(r'^', include(app_urls)),

    # url(r'^app/', include(app_urls)),

    url(r'^api/', include(api_urls)),
]
