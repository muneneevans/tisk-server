from colorfield.fields import ColorField
from django.db import models

from tisk.utils import get_image_path


class MemberType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    share_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    color = ColorField(null=True, blank=True)


    def __str__(self):
        return self.name