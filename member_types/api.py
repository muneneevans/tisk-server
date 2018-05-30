from rest_framework import mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .serializers import *
from .models import *


class MemberTypeViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,GenericViewSet):
    model = MemberType    
    queryset = MemberType.objects.all()
    serializer_class = MemberTypeInlineSerializer
    permission_classes = [AllowAny,]

