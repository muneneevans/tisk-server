from django.db import models


# Create your models here.
class MembershipCategory(models.Model):
    slug = models.CharField(primary_key=True, max_length=20)