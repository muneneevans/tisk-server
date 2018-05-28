from colorfield.fields import ColorField
from django.db import models

from tisk.utils import get_image_path


class MembershipCategory(models.Model):
    slug = models.CharField(primary_key=True, max_length=20)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    display_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    share_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to=get_image_path, null=True, blank=True)
    color = ColorField(null=True, blank=True)
    order_number = models.IntegerField(null=True,default=1)