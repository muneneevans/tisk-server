from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.conf.global_settings import EMAIL_HOST_USER
from django.http import JsonResponse


from rest_framework import status
from rest_framework.fields import EmailField, CharField
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.views import ObtainJSONWebToken

from members.permissions import IsMFSInactive
from members.models import Member

from .permissions import isOwner, isActivated
from .serializers import *
from .models import User, PasswordRecoveryToken


class TiskObtainJSONWebToken(ObtainJSONWebToken):
    permission_classes = (isActivated,)


class CreateUser(ListCreateAPIView):
    permission_classes = [AllowAny, ]
    model = User
    serializer_class = UserCreateSerializer
    queryset = ''

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserInlineSerializer
        return self.serializer_class


class RetrieveUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, isOwner]
    queryset = User.objects.all()
    model = User
    serializer_class = UserInlineSerializer
    lookup_field = 'email'


class ActivateUser(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = type('', (Serializer,), {'token': CharField(
        required=True, max_length=50, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = get_object_or_404(
            ActivationToken, token=serializer.validated_data['token'])

        if not token.is_expired:
            token.is_expired = True
            token.save()

            user = token.user
            user.is_active = True
            user.save()

            member = Member.objects.filter(user=user)[0]

            name = ""
            if member:
                name = member.first_name

            # send welcome email
            subject = 'Welcome to Tisk'
            context = {
                'user': name,
            }
            html_content = render_to_string('welcome_message.html', context)
            text_content = strip_tags(html_content)
            message = EmailMultiAlternatives(
                subject, text_content, EMAIL_HOST_USER, [user.email])
            message.attach_alternative(html_content, "text/html")
            message.send()

            return Response({"message": "user activation successful"})
        else:
            return Response(
                {
                    'status': 'invalid token',
                    'message': "expired token"
                }, status=401)


class CreatePasswordRecoveryCode(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        # ensure email has been provided
        if request.data:
            parameters = request.data
            required_filters = [
                'email'
            ]
            for r_filter in required_filters:
                if not r_filter in parameters.keys():
                    return JsonResponse(
                        {
                            'status': 'bad request',
                            'message': "missing attribute: " + r_filter
                        },
                        status=400)


            requesting_user = User.objects.filter(
                email=request.data['email']).first()

            if requesting_user:
                # create the new reset token
                recovery_token = PasswordRecoveryToken.objects.create(
                    user=requesting_user, token=get_random_string(length=6))
                recovery_token.save()

                # send an email to the user with that token
                subject = 'Password recovery code'
                context = {
                    'email': requesting_user.email,
                    'code': recovery_token.token,
                }
                html_content = render_to_string('password_recovery.html', context)
                text_content = strip_tags(html_content)
                message = EmailMultiAlternatives(
                    subject, text_content, EMAIL_HOST_USER, [requesting_user.email])
                message.attach_alternative(html_content, "text/html")
                message.send()

                return JsonResponse(
                    {
                        'status': 'Success',
                        'message': "password recovery code sent"
                    },
                    status=200)
            else:
                return JsonResponse(
                    {
                        'status': 'missing user',
                        'message': "user not found"
                    },
                    status=404)


class ResendActivationEmail(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = type('', (Serializer,), {'email': EmailField(
        required=True, allow_blank=False, allow_null=False)})

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(
            User, email=serializer.validated_data['email'])

        if not user.is_active:
            user.send_activation_email()
            return Response({"message": "Activation email successfully sent"})
        else:
            return Response(
                {
                    'status': 'Invalid operation',
                    'message': "user is already activated"
                }, status=403)


class CreateIndividual(CreateUser):
    serializer_class = CreateIndividualSerializer


class CreateBusiness(CreateUser):
    serializer_class = CreateBusinessSerializer


class CreateFuture(CreateUser):
    serializer_class = CreateBusinessSerializer
