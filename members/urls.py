from django.conf.urls import url, include

from .api import *


app_name = 'members'


api_urls = [
    url(r'^$',  UserMembershipView.as_view(), name='user-membership-view'),
    url(r'activate_mfs/?', ActivateMFS.as_view()),
]

urlpatterns = [

    url(r'^/',  include(api_urls)),
]




