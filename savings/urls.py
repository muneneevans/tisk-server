from django.conf.urls import url, include

from .api import *

app_name = 'savings'


api_urls = [    
    url(r'^deposits/$',  UserDepositsView.as_view(), name='user-deposits-view'),
]

urlpatterns = [
    url(r'^/', include(api_urls)),
]
