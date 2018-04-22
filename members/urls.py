from django.conf.urls import url

from .api import *

app_name = 'members'


urlpatterns = [

    url(r'^$',  UserMembershipView.as_view(), name='user-membership-view'),
]
