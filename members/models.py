from django.conf import settings
from django.db import models
from member_types.models import MemberType
import socket
import datetime


class Individual(models.Model):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    other_names = models.CharField(max_length=255)
    national_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50)
    phone_number = models.EmailField(max_length=50)


class Business(models.Model):
    class Meta:
        abstract = True

    business_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255)
    business_email = models.CharField(max_length=100)
    business_phone_number = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=50)
    contact_position = models.CharField(max_length=255)
    contact_email = models.EmailField(max_length=100)


class Member(Individual, Business):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    SUSPENDED = 'Suspended'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (SUSPENDED, 'Suspended'),
    )
    class Meta:
        unique_together = (("user", "member_type"), )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_member")
    member_type = models.ForeignKey(MemberType, on_delete=models.DO_NOTHING)
    is_msf_active = models.BooleanField(blank=True, default=False)
    msf_account = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.__str__()
