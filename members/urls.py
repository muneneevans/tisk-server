from django.conf.urls import url, include
from members.api import ActivateMFS
app_name = 'members'


api_urls = [
    url(r'activate_mfs/?', ActivateMFS.as_view()),
]