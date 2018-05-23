from __future__ import unicode_literals

from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import get_random_string

import uuid

from tisk.settings import EMAIL_HOST_USER
from .UserManager import *


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account
    #
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Please provide a valid email address')
        account = self.model(email=self.normalize_email(email))
        account.set_password(password)
        account.save()

        return account


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def email_user(self, subject, message, from_email=EMAIL_HOST_USER, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_activation_email(self):
        try:
            user_activation_token = ActivationToken.objects.filter(user=self).order_by('-time_generated').first()
        except:
            user_activation_token = ActivationToken.objects.create(
                user=self, token=get_random_string(length=6))
            user_activation_token.save()
        # send the token to the user
        subject = 'Activation Code'
        text_content = 'Welcome, the activation code for your account is %s' % (
            user_activation_token.token)
        self.email_user(subject, text_content, fail_silently=False)


class ActivationToken(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, unique=True, blank=False )
    time_generated = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)
    time_activated = models.DateTimeField(auto_now=True)