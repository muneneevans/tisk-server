from django.conf.urls import url, include

from .api import *


app_name= "member_types"


api_urls = [
    url(r'^$',  MemberTypesListView.as_view(), name='member-types-list-view'),
]


urlpatterns = [
    url(r'^/', include(api_urls)),
]
