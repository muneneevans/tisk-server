from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.fields import EmailField
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .permissions import isOwner
from .serializers import *


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


class ResendActiationEmail(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = type('', (Serializer,),{'email': EmailField(required=True, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=serializer.validated_data['email'])

        if not user.is_active:
            user.send_activation_email()
            return JsonResponse({"message": "Activation email successfully sent"})
        else:
            return JsonResponse(
                {
                    'status': 'Invalid operation',
                    'message': "user is already activated"
                }, status=403)
