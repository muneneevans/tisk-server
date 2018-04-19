from django.db import models

class MemberType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)