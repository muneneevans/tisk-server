from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import *
from .models import *


class MemberTypesListView(ListAPIView): 
    model = MemberType    
    queryset = MemberType.objects.all()
    serializer_class = MemberTypeInlineSerializer
    permission_classes = [AllowAny,]

