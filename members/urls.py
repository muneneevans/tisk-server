from django.conf.urls import url, include
from members.api import ActivateMFS, RequestMFS, UserMembershipView, UserMFSStatus

app_name = 'members'


api_urls = [
    url(r'request_mfs/', RequestMFS.as_view()),
    url(r'activate_mfs/', ActivateMFS.as_view()),
    # url(r'^$',  UserMembershipView.as_view(), name='user-membership-view'),
]

urlpatterns = [

    url(r'mfs_status/', UserMFSStatus.as_view(), name="user-mfs-status-view"),
    url(r'^$',  UserMembershipView.as_view(), name='user-membership-view'),
]
