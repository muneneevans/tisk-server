from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import *
from .api import MemberTypeViewSet

app_name= "member_types"

router = DefaultRouter()
router.register(r'', MemberTypeViewSet)


api_urls = [
    path(r'',  include(router.urls))
]


urlpatterns = [
    url(r'^/', include(api_urls)),
]
