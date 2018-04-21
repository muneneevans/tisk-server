from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .serializers import *
from .models import *
from .permissions import isOwner


class CreateUser(ListCreateAPIView):
    permission_classes = [AllowAny, ]
    model = User
    serializer_class = UserCreateSerializer
    queryset = ''

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


class RetrieveUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    queryset = User.objects.all()
    model = User
    serializer_class = UserInlineSerializer
    lookup_field = 'email'


class ActivateUser(ListAPIView):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        if request.data:
            payload = request.data
            required_fields = [
                'token'
            ]
            for r_filter in required_fields:
                if not r_filter in payload.keys():
                    return JsonResponse(
                        {
                            'status': 'bad request',
                            'message': "missing attribute: " + r_filter
                        },
                        status=400)

            token = get_object_or_404(ActivationToken, token=payload['token'])

            if not token.is_expired:
                token.is_expired = True
                token.save()

                user = token.user
                user.is_active = True
                user.save()

                return JsonResponse({"message": "user activation successful"})
            else:
                return JsonResponse(
                    {
                        'status': 'invalid token',
                        'message': "expired token"
                    }, status=401)
