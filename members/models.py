from django.db import models
from users.models import User
from member_types.models import MemberType
import socket
import datetime

# Create your models here.
class Member(models.Model):
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

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    member_type = models.ForeignKey(MemberType, on_delete=models.DO_NOTHING)
    is_msf_active = models.BooleanField(blank=True, default=False)
    msf_account = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        sa = socket.create_connection("")

        return self.user.__str__()