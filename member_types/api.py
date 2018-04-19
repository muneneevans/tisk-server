from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .serializers import *
from .models import *


class MemberTypesListView(ListAPIView):
    permission_class = [AllowAny,]
    model = MemberType
    serializer_class = MemberTypeInlineSerializer

