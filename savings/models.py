from django.db import models
import uuid
from users.models import User
# Create your models here

class Deposit(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,related_name="user_deposit")
    time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    code = models.CharField(max_length=255, blank=True)