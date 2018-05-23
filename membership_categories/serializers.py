import rest_framework.serializers

from membership_categories.models import MembershipCategory


class MembershipCategorySerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = MembershipCategory
        fields = "__all__"