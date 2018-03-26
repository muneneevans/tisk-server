from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *


class CreateUser(ListCreateAPIView):
    permission_classes = [AllowAny, ]
    model = User
    serializer_class = UserCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserInlineSerializer
        return UserCreateSerializer


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

class RetrieveUserView( RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    model = User
    serializer_class = UserInlineSerializer
    lookup_field = 'phone_number'
