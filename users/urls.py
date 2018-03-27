from django.conf.urls import url, include

from .api import *

app_name = 'users'


api_urls = [

    url(r'^new/$', CreateUser.as_view(), name='new-user'),    
    url(r'^(?P<email>([\w+.]+)\@([\w+.]+))/$',
        RetrieveUserView.as_view(), name='user-view'),

]

urlpatterns = [
    # url(r'^', include(app_urls)),

    # url(r'^app/', include(app_urls)),

    url(r'^api/', include(api_urls)),
]
