from rest_framework import viewsets

from membership_categories.models import MembershipCategory
from membership_categories.serializers import MembershipCategorySerializer

class MembershipCategoryViewSet(viewsets.ModelViewSet):
    queryset = MembershipCategory.objects.all()
    serializer_class = MembershipCategorySerializer
    authentication_classes = []

    def get_permissions(self):
        return []