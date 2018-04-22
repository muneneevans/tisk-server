from django.db import models
from users.models import User
from member_types.models import MemberType

# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="user_member")
    member_type = models.OneToOneField(MemberType, on_delete=models.DO_NOTHING)
    is_msf_active = models.BooleanField(blank=True, default=False)
    msf_account = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.__str__()