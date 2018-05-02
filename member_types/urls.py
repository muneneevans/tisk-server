from django.conf.urls import url, include
from django.urls import path

from .api import *


app_name= "member_types"


api_urls = [
    path(r'',  MemberTypesListView.as_view(), name='member-types-list-view'),
]


urlpatterns = [
    url(r'^/', include(api_urls)),
]
