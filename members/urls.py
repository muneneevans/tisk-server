from django.conf.urls import url, include
from members.api import ActivateMFS, RequestMFS

app_name = 'members'


api_urls = [
    url(r'request_mfs/', RequestMFS.as_view()),
    url(r'activate_mfs/', ActivateMFS.as_view()),
]
