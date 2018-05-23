from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from membership_categories.api import MembershipCategoryViewSet

router = DefaultRouter()

router.register(r'', MembershipCategoryViewSet, base_name='membership-category-view-set')

api_urlpatterns = [
    # path('', include(router.urls)),
    re_path(r'^(?P<pk>[\w-]+)', MembershipCategoryViewSet.as_view({'get': 'retrieve'})),
    path('', MembershipCategoryViewSet.as_view({'get': 'list'})),
]

urlpatterns = [

]