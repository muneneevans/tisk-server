from colorfield.fields import ColorField
from django.db import models

from membership_categories.models import MembershipCategory
from tisk.utils import get_image_path


class MemberType(models.Model):
    INDIVIDUAL = 'Individual'
    BUSINESS = 'Business'
    FUTURE = 'Future'

    TYPE_CHOICES = (
        (INDIVIDUAL, 'Individual'),
        (BUSINESS, 'Business'),
        (FUTURE, 'Future'),
    )

    name = models.CharField(max_length=30, unique=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    membership_category = models.ForeignKey(MembershipCategory, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    share_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to=get_image_path, null=True, blank=True)
    color = ColorField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name