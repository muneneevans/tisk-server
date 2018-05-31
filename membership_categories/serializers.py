import rest_framework.serializers
from membership_categories.models import MembershipCategory


class MembershipCategoryInlineSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = MembershipCategory
        fields = "__all__"


class MembershipCategorySerializer(MembershipCategoryInlineSerializer):
    from member_types.serializers import MemberTypeInlineSerializer
    member_types = MemberTypeInlineSerializer(source='membertype_set', many=True)